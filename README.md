# AI-Infrastructure-Learning-Path

## 專案總結 / Project Summary

本專案記錄我從工業設備維護工程師轉型為 AI 基礎設施工程師的完整學習路徑。
結合 Andrew Ng 機器學習課程、硬體故障預測實戰案例（如 NASA 渦輪風扇資料集），以及自動化腳本的開發經驗。

This repository documents my full learning journey transitioning from an industrial equipment maintenance engineer to an AI Infrastructure Engineer. It integrates coursework from Andrew Ng's Machine Learning specialisation, hands-on hardware failure prediction case studies (e.g. NASA Turbofan dataset), and automation scripting leveraging my existing strengths.

---

## 個人職涯目標 / Career Goals

- 取得 AWS / GCP AI 相關認證，強化雲端 AI 部署能力
- 掌握 MLOps 實務：模型訓練、版本管理、自動化部署
- 結合硬體維護背景，建立工業 AI 預測性維護 (Predictive Maintenance) 解決方案
- 開發智慧化日誌分析與告警自動化工具，提升運維效率

---

## 目錄結構 / Repository Structure

```
AI-Infrastructure-Learning-Path/
├── README.md                    # 專案總結與個人職涯目標
├── requirements.txt             # Python 環境依賴
├── .gitignore                   # 忽略不需要上傳的檔案
│
├── 01-Andrew-Ng-ML/             # Andrew Ng ML 課程練習區
│   ├── Week1-Regression/
│   │   ├── notes.md             # 核心筆記（架構師視角）
│   │   └── lab_work.ipynb       # Jupyter Notebook 練習
│   └── Week2-Neural-Networks/
│       ├── notes.md
│       └── lab_work.ipynb
│
├── 02-Hardware-Case-Studies/    # 硬體實戰案例區
│   └── NASA-Turbofan-RUL/
│       ├── data/                # 公開資料集或下載腳本
│       ├── models/              # 訓練好的模型檔 (.pkl / .h5)
│       └── prediction.py        # 剩餘壽命預測主程式
│
└── 03-Automation-Scripts/       # 自動化串接工具
    ├── log_parser/              # AI 輔助的 Log 分析工具
    └── notification/            # Teams / Email 自動化通知腳本
```

---

## 快速開始 / Quick Start

```bash
# 建立虛擬環境
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate          # Windows

# 安裝依賴
pip install -r requirements.txt
```

---

## 學習進度 / Learning Progress

| 模組 | 主題 | 狀態 |
|------|------|------|
| 01-Andrew-Ng-ML | Week 1 – Linear Regression | 🔄 進行中 |
| 01-Andrew-Ng-ML | Week 2 – Neural Networks | 📝 規劃中 |
| 02-Hardware-Case-Studies | NASA Turbofan RUL | 📝 規劃中 |
| 03-Automation-Scripts | Log Parser | 📝 規劃中 |
| 03-Automation-Scripts | Notification | 📝 規劃中 |