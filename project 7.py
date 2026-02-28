
Download: https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
import warnings
warnings.filterwarnings("ignore")


df = pd.read_csv(
    "airline-passengers.csv",
    parse_dates=["Month"],
    index_col="Month"
)
df.columns = ["Passengers"]

print("Shape:", df.shape)
print(df.head())


plt.figure(figsize=(12, 5))
plt.plot(df["Passengers"], color="navy")
plt.title("Monthly Airline Passengers (1949–1960)")
plt.xlabel("Month")
plt.ylabel("Passengers")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("raw_timeseries.png", dpi=150)
plt.show()


quarterly = df.resample("Q").mean()
print("\nQuarterly averages (first 5):\n", quarterly.head())


decomp = seasonal_decompose(df["Passengers"], model="multiplicative")

fig = decomp.plot()
fig.set_size_inches(12, 9)
plt.suptitle("Seasonal Decomposition (Multiplicative)", y=1.01, fontsize=13)
plt.tight_layout()
plt.savefig("decomposition.png", dpi=150)
plt.show()

print("\nTrend range:", round(decomp.trend.min(), 1), "→", round(decomp.trend.dropna().max(), 1))


df["MA_6"]  = df["Passengers"].rolling(window=6).mean()
df["MA_12"] = df["Passengers"].rolling(window=12).mean()

plt.figure(figsize=(12, 5))
plt.plot(df["Passengers"], label="Actual",       color="steelblue",  alpha=0.7)
plt.plot(df["MA_6"],       label="6-Month MA",   color="orange",     linestyle="--")
plt.plot(df["MA_12"],      label="12-Month MA",  color="red",        linewidth=2)
plt.title("Moving Averages Smoothing")
plt.xlabel("Month")
plt.ylabel("Passengers")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("moving_averages.png", dpi=150)
plt.show()


train = df["Passengers"].iloc[:-12]
test  = df["Passengers"].iloc[-12:]

print(f"\nTrain size: {len(train)} | Test size: {len(test)}")


model  = SARIMAX(train, order=(2, 1, 1), seasonal_order=(1, 1, 1, 12))
result = model.fit(disp=False)

forecast = result.forecast(steps=12)
rmse = np.sqrt(mean_squared_error(test, forecast))
print(f"\nSARIMA RMSE: {rmse:.2f} passengers")


plt.figure(figsize=(12, 6))
plt.plot(train.index, train,        label="Training Data",  color="steelblue")
plt.plot(test.index,  test,         label="Actual",         color="green",  linewidth=2)
plt.plot(test.index,  forecast,     label="Forecast",       color="red",    linestyle="--", linewidth=2)
plt.fill_between(test.index, forecast * 0.88, forecast * 1.12, alpha=0.15, color="red", label="±12% band")
plt.title(f"SARIMA Forecast vs Actual  (RMSE = {rmse:.1f})")
plt.xlabel("Month")
plt.ylabel("Passengers")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("sarima_forecast.png", dpi=150)
plt.show()


growth = (df["Passengers"].iloc[-1] / df["Passengers"].iloc[0] - 1) * 100
peak_month = df["Passengers"].idxmax().strftime("%B")

print("\n===== TIME SERIES INSIGHTS =====")
print(f"Total growth over 12 years: {growth:.1f}%")
print(f"Annual growth rate ≈ {growth/12:.1f}%")
print(f"Peak month historically: {peak_month}")
print(f"July avg passengers: {df[df.index.month == 7]['Passengers'].mean():.0f}")
print(f"Feb  avg passengers: {df[df.index.month == 2]['Passengers'].mean():.0f}")