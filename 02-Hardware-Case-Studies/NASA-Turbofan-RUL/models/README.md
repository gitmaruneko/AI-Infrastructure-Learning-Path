# NASA Turbofan RUL — Models Directory

Trained model artefacts are saved here by `prediction.py`.

| File | Description |
|------|-------------|
| `rul_rf.pkl` | Random Forest regressor (scikit-learn) |
| `rul_gb.pkl` | Gradient Boosting regressor (scikit-learn) |
| `scaler.pkl` | StandardScaler fitted on training features |

> **Note**: Model files (`.pkl`, `.h5`, `.joblib`) are excluded from version
> control via `.gitignore`. Re-train locally with:
> ```bash
> python prediction.py --mode train --data_path data/train_FD001.txt
> ```
