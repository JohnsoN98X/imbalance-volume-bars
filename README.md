# 📊 Imbalance Volume Bars (IVB) – Python Implementation

## 📘 Project Description

This project provides a practical implementation of the Imbalance Volume Bars (IVB) method, originally introduced in *Advances in Financial Machine Learning* by Marcos López de Prado.

One key distinction from López de Prado’s original formulation is that this version **does not use the exponentially weighted average of bar lengths** to estimate the imbalance threshold.  
Instead, the threshold for forming a new bar is based purely on a **probabilistic exponential smoothing** of the absolute imbalance volume $\theta_t$.

### The project includes:

- A single Python class for IVB bar construction (`src/`)
- A Jupyter notebook demonstrating usage and a full comparative statistical analysis (`notebooks/Application Example`)
- A Jupyter notebook demonstrating the performance improvement of XGBoost with IVB sampling (`notebooks/XGB Regression Example.ipynb`)


> **Note**: All results and analysis are based on a single financial time series and a fixed decay factor of $\alpha = 0.9$.  
> Explanations aim to showcase analytical approaches to interpreting sampling behavior — not to generalize across all assets.

---

## 📐 Mathematical Formulation – Imbalance Volume Bars (IVB)

At each time step *t*, the following calculations are performed:

---

### 1. Directional Sign

βₜ = +1  if Pₜ − Pₜ₋₁ > 0  
βₜ = −1  otherwise

Where *Pₜ* is the closing price at time *t*.

---

### 2. Volume Imbalance

θₜ = βₜ × Vₜ

Where *Vₜ* is the traded volume. θₜ captures signed trade pressure.

---

### 3. Cumulative Imbalance

Θₜ = Σ₍ᵢ₌ₛ₎⁽ᵗ⁾ θᵢ

Where *s* marks the start of the current bar.

---

### 4. Adaptive Threshold (Exponential Smoothing)

εₜ = α × |θₜ| + (1 − α) × εₜ₋₁

Where:  
- *α* ∈ (0, 1) is the smoothing parameter  
- *εₜ* is the adaptive imbalance threshold

---

### 5. Bar Formation Condition

A new bar is formed when:  
  |Θₜ| > εₜ

Once this is true:  
- An OHLCV bar is created for [s, t]  
- Θₜ is reset  
- Next bar starts from t+1


---

### 📊 Each Completed Bar Contains:
- **Open**: $P_s$
- **High**: $\max \{P_s, ..., P_t\}$
- **Low**: $\min \{P_s, ..., P_t\}$
- **Close**: $P_t$
- **Volume**: $\sum_{i=s}^{t} V_i$

---

## 🚀 Getting Started

### 🔧 Requirements

| Purpose            | Libraries Needed                                      |
|--------------------|--------------------------------------------------------|
| Running the class  | `pandas`, `numpy`                                     |
| Running the notebook | `pandas`, `numpy`, `matplotlib`, `seaborn`, `statsmodels`, `scipy` |

> To install all dependencies (for the notebook), run:
```bash
pip install pandas numpy matplotlib seaborn statsmodels scipy
```

---

## 🔍 Usage Notes

- Input must be a `pandas.DataFrame` with columns: `['open', 'high', 'low', 'close', 'volume']`
- Output is a resampled OHLCV DataFrame indexed by Datetime
- Core logic is optimized using NumPy for high-frequency scalability

---

## 🔬 Applied Experiment – Model Performance with IVB

To empirically assess the impact of IVB sampling on model accuracy, this project includes a controlled regression experiment using `XGBoostRegressor`.  
The notebook demonstrates how data sampled using Imbalance Volume Bars improves predictive performance over time-based sampling.

### 🧪 Setup:
- Model: `XGBoostRegressor` with Bollinger Bands and ATR features.
- Tuning: `optuna`, with a time limit of 300 seconds per optimization.
- Metrics: R², MSE, and cross-validation consistency.

> 🔍 See: [`notebooks/XGB_Regression Example.ipynb`](03_XGB_Regression_Example.ipynb)

---

## 🔬 Applied Experiment: LSTM on Time and Imbalance Volume Bars

This experiment investigates the predictive capabilities of Long Short-Term Memory (LSTM) networks applied to two types of financial bar data:

- **Time Bars (TIME):** Fixed-interval sampling of the price data.
- **Imbalance Volume Bars (IVB):** Event-driven sampling based on volume imbalances, hypothesized to better capture market dynamics.

### Methodology

- **Data preparation:** Sliding windows of sequences generated from both bar types.
- **Modeling:** LSTM architectures optimized using Optuna, with hyperparameters including number of layers, units per layer, kernel initializers, learning rate, and optimizer choice.
- **Training:** Early stopping and checkpoint callbacks employed to mitigate overfitting.
- **Evaluation:** Models assessed via Mean Squared Error (MSE), Mean Absolute Error (MAE), and \( R^2 \), alongside detailed residual diagnostics and statistical hypothesis testing.
- **Baseline comparison:** Results contrasted with a naive martingale model (previous value prediction).

### Key Findings

- The IVB LSTM model **significantly outperformed** both the Time Bar LSTM and the martingale baseline, achieving multiple orders of magnitude improvement in error metrics.
- Residual analysis showed that IVB LSTM residuals were more consistent with white noise assumptions, while Time Bar LSTM residuals exhibited autocorrelation and structure, indicating model misspecification.
- Negative \( R^2 \) values highlighted the inherent difficulty of forecasting noisy, low-variance financial data, reinforcing the importance of complementary metrics and residual diagnostics.

### Hardware and Computational Notes

- Experiments were conducted on a consumer-grade Intel i9 CPU with RTX 4070 GPU.
- Resource constraints limited training duration and hyperparameter search breadth, suggesting potential for further improvement with industrial-scale hardware.

---

This applied experiment underscores the importance of data representation in financial time series modeling and demonstrates the superior utility of volume-based bars in LSTM forecasting frameworks.

---

## 📡 Data Source & Usage

The dataset was retrieved using the `ib_insync` library connected to Interactive Brokers (IB).  
Due to IB’s licensing policy, **raw market data is excluded** from this repository.

To reproduce results:
- Acquire your own OHLCV data (from public APIs or CSVs)
- Only timestamped OHLCV values are required — no proprietary metadata.

---

## ⚠️ Disclaimer

All tools and methods in this project are provided **strictly for educational and research purposes**.  
They do **not** constitute trading advice or recommendations.

The author assumes **no liability** for any actions taken based on this code or its analysis.
