# Week 1 — Linear Regression（架構師視角筆記）

## 核心概念 / Core Concepts

### 監督式學習 Supervised Learning
- **輸入 (Input, X)**：特徵向量，例如房屋面積、臥室數量
- **輸出 (Output, Y)**：標籤，例如房屋售價
- **目標**：學習一個函數 f，使得 f(X) ≈ Y

### 線性回歸 Linear Regression
模型假設：

```
f(x) = wx + b
```

其中 w 為權重 (weight)，b 為偏差 (bias)。

### 損失函數 Cost Function (MSE)

```
J(w, b) = (1 / 2m) * Σ (f(x⁽ⁱ⁾) - y⁽ⁱ⁾)²
```

目標：最小化 J(w, b)。

### 梯度下降 Gradient Descent

```
w := w - α * (∂J/∂w)
b := b - α * (∂J/∂b)
```

- **學習率 α (Learning Rate)**：控制每步更新幅度，過大會發散，過小收斂慢
- **同步更新**：w 與 b 需同時更新，不可依序

---

## 架構師觀點 / Architect's Perspective

| 面向 | 工業應用類比 |
|------|------------|
| 特徵工程 | 感測器訊號前處理（濾波、正規化） |
| 損失函數 | 設備異常偵測的誤差指標 |
| 梯度下降 | PID 控制器的自動調參過程 |
| 過擬合風險 | 模型過度擬合歷史故障模式，無法泛化 |

> **重點心得**：線性回歸是一切預測性維護模型的基礎。理解梯度下降有助於後續理解神經網路反向傳播。

---

## 延伸應用 / Extension to Hardware

- 預測設備壽命 (RUL)：以感測器讀值為 X，剩餘壽命（小時）為 Y
- 振動幅度 → 軸承磨損預測
- 電流消耗 → 馬達退化評估

---

## 參考資源 / References
- [Andrew Ng — Machine Learning Specialisation (Coursera)](https://www.coursera.org/specializations/machine-learning-introduction)
- [scikit-learn: Linear Models](https://scikit-learn.org/stable/modules/linear_model.html)
