

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportions_ztest, proportion_confint
from statsmodels.stats.power import TTestIndPower
import warnings
warnings.filterwarnings("ignore")

np.random.seed(42)
n = 10_000

ab_data = pd.DataFrame({
    "group":            ["control"] * n + ["treatment"] * n,
    "converted":        np.concatenate([
                            np.random.binomial(1, 0.075, n),   # 7.5% control rate
                            np.random.binomial(1, 0.090, n)    # 9.0% treatment rate
                        ]),
    "session_duration": np.concatenate([
                            np.random.normal(180, 45, n),
                            np.random.normal(182, 45, n)
                        ]),
    "device":           np.random.choice(["mobile", "desktop"], 2 * n, p=[0.55, 0.45])
})

# Replace with: ab_data = pd.read_csv("ab_test_data.csv")

print("Sample data:\n", ab_data.head(8))
print("\nGroup summary:")
print(ab_data.groupby("group")["converted"].agg(["sum", "count", "mean"]).rename(
    columns={"sum": "Conversions", "count": "Visitors", "mean": "Rate"}))


conv_ctrl  = ab_data[ab_data["group"] == "control"]["converted"].sum()
conv_treat = ab_data[ab_data["group"] == "treatment"]["converted"].sum()
n_ctrl     = ab_data[ab_data["group"] == "control"].shape[0]
n_treat    = ab_data[ab_data["group"] == "treatment"].shape[0]

z_stat, p_val = proportions_ztest(
    [conv_treat, conv_ctrl],
    [n_treat, n_ctrl],
    alternative="larger"
)

print(f"\n--- Two-Proportion Z-Test ---")
print(f"Z-statistic : {z_stat:.4f}")
print(f"P-value     : {p_val:.6f}")
print("Decision    :", "Reject H₀ ✅ (Treatment is significantly better)" if p_val < 0.05
      else "Fail to reject H₀ ❌")


ci_ctrl  = proportion_confint(conv_ctrl,  n_ctrl,  alpha=0.05)
ci_treat = proportion_confint(conv_treat, n_treat, alpha=0.05)

rates    = [conv_ctrl / n_ctrl, conv_treat / n_treat]
ci_lower = [rates[0] - ci_ctrl[0],  rates[1] - ci_treat[0]]
ci_upper = [ci_ctrl[1] - rates[0],  ci_treat[1] - rates[1]]

plt.figure(figsize=(8, 5))
plt.errorbar(
    x=[0, 1],
    y=rates,
    yerr=[ci_lower, ci_upper],
    fmt="o",
    capsize=12,
    markersize=10,
    color=["steelblue", "coral"],
    ecolor=["steelblue", "coral"]
)
plt.xticks([0, 1], ["Control", "Treatment"], fontsize=13)
plt.ylabel("Conversion Rate", fontsize=12)
plt.title("95% Confidence Intervals — A/B Test Result", fontsize=13)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("ab_confidence_intervals.png", dpi=150)
plt.show()


contingency = pd.crosstab(ab_data["device"], ab_data["converted"])
chi2, p_chi, dof, _ = stats.chi2_contingency(contingency)

print(f"\n--- Chi-Square Test (Device vs Conversion) ---")
print(f"Chi² = {chi2:.3f} | p = {p_chi:.4f} | dof = {dof}")
print("Device affects conversion:" , "Yes ✅" if p_chi < 0.05 else "No ❌")


dur_ctrl  = ab_data[ab_data["group"] == "control"]["session_duration"]
dur_treat = ab_data[ab_data["group"] == "treatment"]["session_duration"]

t_stat, p_t = stats.ttest_ind(dur_treat, dur_ctrl)
print(f"\n--- Independent T-Test (Session Duration) ---")
print(f"T-statistic: {t_stat:.4f} | P-value: {p_t:.4f}")
print("Duration differs:", "Yes ✅" if p_t < 0.05 else "No ❌")


analysis     = TTestIndPower()
sample_size  = analysis.solve_power(effect_size=0.2, power=0.8, alpha=0.05)
print(f"\n--- Power Analysis ---")
print(f"Minimum sample per group needed: {int(np.ceil(sample_size))}")


lift        = (rates[1] - rates[0]) / rates[0] * 100
revenue_est = (rates[1] - rates[0]) * n_treat * 120  # assumed $120 avg order

print("\n===== A/B TEST BUSINESS REPORT =====")
print(f"Control conversion rate  : {rates[0]*100:.2f}%")
print(f"Treatment conversion rate: {rates[1]*100:.2f}%")
print(f"Relative lift            : {lift:.1f}%")
print(f"Statistical significance : p = {p_val:.6f}")
print(f"Estimated annual revenue impact: ${revenue_est * 12:,.0f}")
print("\nRecommendation: Roll out new design to all users.")
print("Monitor: Mobile conversion rate is lower — investigate separately.")