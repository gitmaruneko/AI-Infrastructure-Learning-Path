# Week 2 — Neural Networks & Deep Learning（架構師視角筆記）

## 核心概念 / Core Concepts

### 神經網路 Neural Network
- **神經元 (Neuron)**：接收輸入，套用激活函數，輸出結果
- **層 (Layer)**：輸入層 → 隱藏層 × N → 輸出層
- **前向傳播 (Forward Propagation)**：由輸入到輸出逐層計算

### 激活函數 Activation Functions

| 函數 | 公式 | 適用場景 |
|------|------|---------|
| Sigmoid | σ(z) = 1 / (1 + e⁻ᶻ) | 二元分類輸出層 |
| ReLU | max(0, z) | 隱藏層（主流選擇） |
| Linear | z | 回歸輸出層 |
| Softmax | eᶻⁱ / Σeᶻʲ | 多元分類輸出層 |

### 反向傳播 Backpropagation
- 計算損失函數對每個參數的梯度
- 使用鏈式法則 (Chain Rule) 從輸出層往回傳遞誤差
- 更新公式同梯度下降

### 正規化 Regularisation
- **L2 / Weight Decay**：懲罰過大的權重，防止過擬合
- **Dropout**：訓練時隨機丟棄部分神經元
- **Batch Normalisation**：穩定訓練過程，加速收斂

---

## 架構師觀點 / Architect's Perspective

| 面向 | 工業應用類比 |
|------|------------|
| 隱藏層深度 | 特徵抽象層次（原始訊號 → 頻域特徵 → 故障模式） |
| ReLU | 設備狀態的非線性響應 |
| Dropout | 模擬感測器訊號遺失的魯棒性訓練 |
| 批次正規化 | 不同機台、不同操作條件下的資料標準化 |

> **重點心得**：神經網路的多層抽象能力，正是工業設備複雜故障模式識別的關鍵。

---

## 延伸應用 / Extension to Hardware

- 多感測器融合分類：輸入振動、溫度、壓力 → 輸出故障類型
- 時間序列預測：LSTM / GRU 處理設備退化序列

---

## 參考資源 / References
- [Andrew Ng — Neural Networks and Deep Learning](https://www.coursera.org/learn/neural-networks-deep-learning)
- [TensorFlow Keras Documentation](https://www.tensorflow.org/api_docs/python/tf/keras)
