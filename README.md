Task 2 — Exploratory Data Analysis (EDA)

---
 Objective
Perform a full Exploratory Data Analysis on the Titanic dataset to uncover patterns, distributions, correlations, and anomalies before any modelling.

---

 Dataset

| Dataset | Download Link |
|---|---|
| `titanic.csv` | https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv |

**Quick download:**
```bash
curl -O https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv
```

---

 Installation

```bash
pip install pandas numpy matplotlib seaborn scipy
```

---

 How to Run

```bash
python task2_eda.py
```

> Make sure `titanic.csv` is in the same folder as the script.

---

 What the Script Does

### Step 1 — Load & Inspect
- Reads the CSV file
- Prints shape, data types, and missing value counts
- Shows full summary statistics for all columns

### Step 2 — Handle Missing Values
- Fills missing `Age` values with the **median**
- Fills missing `Embarked` values with the **mode**

### Step 3 — Distribution Analysis
- **Histogram + KDE** — Age distribution curve
- **Boxplot** — Fare spread across passenger classes
- **Countplot** — Survival count split by gender

### Step 4 — Correlation Analysis
- **Heatmap** of all numeric feature correlations
- **Cross-tabulation** of survival rate by passenger class

### Step 5 — Outlier Detection
- **Boxplot** to visually spot fare outliers
- **Z-score method** to identify extreme fare values (|Z| > 3)

### Step 6 — Advanced Visualizations
- **Pairplot** — relationships between Age, Fare, Parch, and Survived
- **FacetGrid** — Age distribution broken down by Survived × Pclass

### Step 7 — Key Insights Printed
- Overall, female, and male survival rates
- Survival rate per passenger class
- Skewness, kurtosis, and Pearson correlation values

---

 Output Files Generated

| File | Description |
|---|---|
| `dist_analysis.png` | Age histogram and Fare boxplot |
| `survival_gender.png` | Survival count by gender |
| `correlation_heatmap.png` | Feature correlation matrix |
| `fare_outliers.png` | Fare outlier boxplot |
| `pairplot.png` | Multivariate pairplot |
| `facet_grid.png` | Age distribution by class and survival |

---

 Key Findings

| Finding | Value |
|---|---|
| Female survival rate | ~74% |
| Male survival rate | ~19% |
| 1st class survival rate | ~63% |
| 3rd class survival rate | ~24% |
| Fare vs Survived correlation | r ≈ 0.26 |
| Fare outliers detected | ~20 passengers (fare > $300) |

---

 Libraries Used

| Library | Purpose |
|---|---|
| `pandas` | Data loading and manipulation |
| `numpy` | Numerical calculations |
| `matplotlib` | Base plotting |
| `seaborn` | Statistical visualizations |
| `scipy.stats` | Z-score outlier detection |

---

 Tips
- All plots are saved automatically — no need to click anything
- The script prints all insights to the console at the end
- You can replace `titanic.csv` with any similar dataset and adjust column names accordingly