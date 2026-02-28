# 🧪 Task 4 — Hypothesis Testing & A/B Testing

---

## 📌 Objective
Design and evaluate an e-commerce A/B test to determine whether a new website design significantly improves conversion rates over the existing design, using rigorous statistical methods.

---

## 📥 Dataset

> **No CSV file needed.** The dataset is simulated directly inside the script using NumPy's random generator with a fixed seed for reproducibility.

If you have a real dataset, replace the simulation block with:
```python
ab_data = pd.read_csv("ab_test_data.csv")
```

---

## ⚙️ Installation

```bash
pip install pandas numpy matplotlib scipy statsmodels
```

---

## ▶️ How to Run

```bash
python task4_ab_testing.py
```

---

## 🔍 What the Script Does

### Step 1 — Simulate / Load Data
- Creates 20,000 users (10,000 control + 10,000 treatment)
- Control group: 7.5% conversion rate
- Treatment group: 9.0% conversion rate
- Includes session duration and device type columns

### Step 2 — Formulate Hypotheses
```
H₀ : p_treatment ≤ p_control  (new design is NOT better)
H₁ : p_treatment >  p_control  (new design IS better)
```
- One-tailed test (we only care if treatment is better, not just different)

### Step 3 — Two-Proportion Z-Test
- Tests whether the difference in conversion rates is statistically significant
- Uses `proportions_ztest` from statsmodels
- Prints Z-statistic and p-value with a clear decision

### Step 4 — Confidence Interval Plot
- Calculates 95% CIs for both groups using `proportion_confint`
- Plots error bars — non-overlapping CIs visually confirm significance

### Step 5 — Chi-Square Test
- Tests whether device type (mobile vs desktop) affects conversion
- Uses `chi2_contingency` on a 2×2 contingency table

### Step 6 — Independent T-Test
- Tests whether session duration differs between control and treatment
- Uses `ttest_ind` — checks for unintended side effects of the new design

### Step 7 — Power Analysis
- Calculates the minimum sample size needed per group
- Uses effect size = 0.2, power = 0.8, alpha = 0.05

### Step 8 — Business Report
- Calculates relative lift in conversion rate
- Estimates annual revenue impact based on order value
- Prints a final go/no-go recommendation

---

 Output Files Generated

| File | Description |
|---|---|
| `ab_confidence_intervals.png` | 95% CI error bar chart for both groups |

---

 Test Results Summary

| Test | Purpose | Result |
|---|---|---|
| Two-Proportion Z-Test | Is treatment conversion higher? | p < 0.0001 ✅ Significant |
| Chi-Square Test | Does device type affect conversion? | p ≈ 0.31 ❌ Not significant |
| Independent T-Test | Does session duration differ? | p ≈ 0.62 ❌ Not significant |
| Power Analysis | Minimum sample size needed | ~393 per group |

---

 Key Findings

| Metric | Value |
|---|---|
| Control conversion rate | 7.5% |
| Treatment conversion rate | 9.0% |
| Relative lift | ~20% |
| Z-statistic | ~4.74 |
| P-value | < 0.0001 |
| Estimated annual revenue impact | ~$180,000 |

---

 Libraries Used

| Library | Purpose |
|---|---|
| `pandas` | Data manipulation |
| `numpy` | Data simulation and calculations |
| `matplotlib` | Plotting confidence intervals |
| `scipy.stats` | Chi-square and T-test |
| `statsmodels` | Z-test, CI calculation, power analysis |

---

 Tips
- Always check test assumptions before running: normality (Shapiro-Wilk), equal variance (Levene's test), and independence
- One-tailed vs two-tailed: use one-tailed only when you have a prior reason to expect the direction of the effect
- If using a real dataset, ensure random assignment — use a chi-square test on demographics to validate group balance