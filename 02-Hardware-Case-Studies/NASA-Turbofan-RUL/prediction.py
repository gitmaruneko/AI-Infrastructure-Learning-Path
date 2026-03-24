"""
NASA Turbofan Engine Degradation — Remaining Useful Life (RUL) Prediction
==========================================================================

資料集：CMAPSS (Commercial Modular Aero-Propulsion System Simulation)
來源：https://data.nasa.gov/Aerospace/CMAPSS-Jet-Engine-Simulated-Data/ff5v-kuh6

使用方式：
    python prediction.py --data_path data/train_FD001.txt --mode train
    python prediction.py --data_path data/test_FD001.txt  --mode predict

目錄結構：
    data/    — 存放 train_FD001.txt, test_FD001.txt, RUL_FD001.txt
    models/  — 儲存訓練好的模型 (.pkl)
"""

import argparse
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error

# ---------------------------------------------------------------------------
# 常數 / Constants
# ---------------------------------------------------------------------------

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# CMAPSS 資料欄位名稱
COLUMN_NAMES = (
    ["unit_id", "cycle"]
    + [f"op_setting_{i}" for i in range(1, 4)]
    + [f"sensor_{i}" for i in range(1, 22)]
)

# 低方差感測器（通常不具區分力，可排除）
DROP_SENSORS = ["sensor_1", "sensor_5", "sensor_10", "sensor_16", "sensor_18", "sensor_19"]

# ---------------------------------------------------------------------------
# 資料載入與前處理 / Data Loading & Preprocessing
# ---------------------------------------------------------------------------


def load_data(path: str) -> pd.DataFrame:
    """載入 CMAPSS 格式的文字檔（空白分隔，無表頭）。"""
    df = pd.read_csv(path, sep=r"\s+", header=None, names=COLUMN_NAMES)
    df.drop(columns=DROP_SENSORS, inplace=True, errors="ignore")
    return df


def add_rul(df: pd.DataFrame) -> pd.DataFrame:
    """為訓練資料計算剩餘壽命標籤 (RUL)。"""
    max_cycles = df.groupby("unit_id")["cycle"].max().rename("max_cycle")
    df = df.join(max_cycles, on="unit_id")
    df["rul"] = df["max_cycle"] - df["cycle"]
    df.drop(columns=["max_cycle"], inplace=True)
    return df


def get_features(df: pd.DataFrame) -> list[str]:
    """回傳用於訓練的特徵欄位清單。"""
    exclude = {"unit_id", "cycle", "rul"}
    return [c for c in df.columns if c not in exclude]


# ---------------------------------------------------------------------------
# 訓練 / Training
# ---------------------------------------------------------------------------


def train(data_path: str, model_type: str = "rf") -> None:
    """訓練 RUL 預測模型並儲存至 models/ 目錄。"""
    print(f"[INFO] Loading training data from: {data_path}")
    df = load_data(data_path)
    df = add_rul(df)

    features = get_features(df)
    X = df[features].values
    y = df["rul"].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    if model_type == "rf":
        model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    elif model_type == "gb":
        model = GradientBoostingRegressor(n_estimators=200, learning_rate=0.05, random_state=42)
    else:
        raise ValueError(f"Unsupported model_type: {model_type}")

    print(f"[INFO] Training {model_type.upper()} model on {len(df)} samples ...")
    model.fit(X_scaled, y)

    os.makedirs(MODELS_DIR, exist_ok=True)
    model_path = os.path.join(MODELS_DIR, f"rul_{model_type}.pkl")
    scaler_path = os.path.join(MODELS_DIR, "scaler.pkl")
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    print(f"[INFO] Model saved to: {model_path}")
    print(f"[INFO] Scaler saved to: {scaler_path}")

    # 訓練集評估
    y_pred = model.predict(X_scaled)
    mae = mean_absolute_error(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    print(f"[RESULT] Train MAE={mae:.2f} cycles, RMSE={rmse:.2f} cycles")


# ---------------------------------------------------------------------------
# 預測 / Prediction
# ---------------------------------------------------------------------------


def predict(data_path: str, model_type: str = "rf") -> pd.DataFrame:
    """載入測試資料並預測每台引擎的剩餘壽命。"""
    model_path = os.path.join(MODELS_DIR, f"rul_{model_type}.pkl")
    scaler_path = os.path.join(MODELS_DIR, "scaler.pkl")

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model not found at {model_path}. Please run with --mode train first."
        )

    print(f"[INFO] Loading model from: {model_path}")
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)

    df = load_data(data_path)
    # 取每台引擎最後一個時間點的感測器讀值作為預測輸入
    last_cycles = df.groupby("unit_id").last().reset_index()

    features = get_features(last_cycles)
    X = last_cycles[features].values
    X_scaled = scaler.transform(X)

    predictions = model.predict(X_scaled)
    result = pd.DataFrame({
        "unit_id": last_cycles["unit_id"].values,
        "predicted_rul_cycles": np.round(predictions).astype(int),
    })

    print("\n[RESULT] Predicted RUL per engine:")
    print(result.to_string(index=False))
    return result


# ---------------------------------------------------------------------------
# CLI 入口 / Entry Point
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="NASA Turbofan RUL Prediction"
    )
    parser.add_argument(
        "--data_path",
        default=os.path.join(DATA_DIR, "train_FD001.txt"),
        help="Path to CMAPSS data file",
    )
    parser.add_argument(
        "--mode",
        choices=["train", "predict"],
        default="train",
        help="Operation mode: train or predict",
    )
    parser.add_argument(
        "--model",
        choices=["rf", "gb"],
        default="rf",
        help="Model type: rf (Random Forest) or gb (Gradient Boosting)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.mode == "train":
        train(args.data_path, args.model)
    else:
        predict(args.data_path, args.model)
