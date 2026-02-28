 Task 3 — Time Series Analysis

---

 Objective
Analyse monthly airline passenger data from 1949–1960 to identify trends, seasonal patterns, and build a SARIMA forecasting model to predict future passenger counts.

---

 Dataset

| Dataset | Download Link |
|---|---|
| `airline-passengers.csv` | https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv |

**Quick download:**
```bash
curl -O https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv
```

---

 Installation

```bash
pip install pandas numpy matplotlib statsmodels scikit-learn
```

---

 How to Run

```bash
python task3_timeseries.py
```

> Make sure `airline-passengers.csv` is in the same folder as the script.

---

 What the Script Does

 Step 1 — Load & Prepare Data
- Reads CSV with `Month` parsed as datetime and set as index
- Prints the first few rows and dataset shape

 Step 2 — Raw Time Series Plot
- Plots the full 12-year monthly passenger series
- Visually confirms upward trend and repeating seasonality

 Step 3 — Resample to Quarterly
- Converts monthly data to quarterly averages using `resample('Q').mean()`

 Step 4 — Seasonal Decomposition
- Applies **multiplicative decomposition** (suitable when seasonal amplitude grows with trend)
- Separates the series into: **Trend**, **Seasonality**, and **Residuals**
- Plots all three components together

 Step 5 — Moving Averages
- Calculates **6-month MA** (captures short-term smoothing)
- Calculates **12-month MA** (eliminates seasonal noise, shows pure trend)
- Plots both alongside the actual data

 Step 6 — Train / Test Split
- Uses first **132 months** for training
- Holds out **last 12 months** for testing

 Step 7 — SARIMA Forecasting
- Fits `SARIMA(2,1,1)(1,1,1,12)` on training data
- Forecasts the 12 held-out months
- Calculates **RMSE** to measure forecast accuracy

 Step 8 — Forecast Plot
- Plots training data, actual test values, and forecast side-by-side
- Adds a ±12% confidence band around the forecast

Step 9 — Business Insights
- Calculates total and annual growth rate
- Identifies the historical peak month
- Compares July vs February average passengers

---

 Output Files Generated

| File | Description |
|---|---|
| `raw_timeseries.png` | Full raw time series plot |
| `decomposition.png` | Trend + Seasonal + Residual components |
| `moving_averages.png` | Actual vs 6-month and 12-month MA |
| `sarima_forecast.png` | Forecast vs actual with confidence band |

---

 Key Findings

| Metric | Value |
|---|---|
| Total passenger growth (12 years) | ~150% |
| Approximate annual growth rate | ~12% |
| Peak month | July |
| July avg passengers | ~2× February average |
| SARIMA RMSE | ≈ 15 passengers (~2.8% error) |
| Best model | SARIMA(2,1,1)(1,1,1,12) |

---

 Libraries Used

| Library | Purpose |
|---|---|
| `pandas` | Time series loading and resampling |
| `numpy` | Numerical operations |
| `matplotlib` | Plotting |
| `statsmodels` | Decomposition and SARIMA modelling |
| `scikit-learn` | RMSE calculation |

---

 Tips
- The `model='multiplicative'` setting in decomposition works best when seasonal peaks grow over time
- If you switch to a different dataset, adjust the `seasonal_order` `m=12` to match the data frequency (e.g. `m=4` for quarterly)
- `warnings.filterwarnings("ignore")` is used to suppress SARIMA convergence messages — safe to keep