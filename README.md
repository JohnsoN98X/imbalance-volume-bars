# 📊 Imbalance Volume Bars (IVB) – Python Implementation

## 📘 Project Description

This project provides a practical implementation of the Imbalance Volume Bars (IVB) method, originally introduced in *Advances in Financial Machine Learning* by Marcos López de Prado.

One key distinction from López de Prado’s original formulation is that this version **does not use the exponentially weighted average of bar lengths** to estimate the imbalance threshold.  
Instead, the threshold for forming a new bar is based purely on a **probabilistic exponential smoothing** of the absolute imbalance volume $\theta_t$.

### The project includes:

- A single Python class for IVB bar construction (`src/`)
- A Jupyter notebook demonstrating usage and a full comparative statistical analysis (`notebooks/`)

> **Note**: All results and analysis are based on a single financial time series and a fixed decay factor of $\alpha = 0.9$.  
> Explanations aim to showcase analytical approaches to interpreting sampling behavior — not to generalize across all assets.

---

## 📐 Mathematical Formulation – Imbalance Volume Bars (IVB)

At each time step $t$, the following calculations are performed:

### 1. Directional Sign:
$$
\beta_t =
\begin{cases}
+1, & \text{if } P_t - P_{t-1} > 0 \\
-1, & \text{otherwise}
\end{cases}
$$
Where $P_t$ is the closing price at time $t$.

---

### 2. Volume Imbalance:
$$
\theta_t = \beta_t \cdot V_t
$$
Where $V_t$ is the traded volume. $\theta_t$ captures signed trade pressure (buy/sell imbalance).

---

### 3. Cumulative Imbalance:
$$
\Theta_t = \sum_{i=s}^{t} \theta_i
$$
Where $s$ marks the start of the current bar.

---

### 4. Adaptive Threshold (Exponential Smoothing):
$$
\varepsilon_t = \alpha \cdot |\theta_t| + (1 - \alpha) \cdot \varepsilon_{t-1}
$$

Where:
- $\alpha \in (0, 1)$ is the smoothing parameter
- $\varepsilon_t$ is the dynamic imbalance threshold

---

### 5. Bar Formation Condition:
A new bar is formed when:
$$
|\Theta_t| > \varepsilon_t
$$

Once this condition is met:
- A new OHLCV bar is created from interval $[s, t]$
- $\Theta_t$ is reset to 0
- Bar count continues from $t + 1$

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
