

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# ── 1. LOAD DATA ────────────────────────────────────────────────────────────
# Download: https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv
df = pd.read_csv("titanic.csv")

print("Shape:", df.shape)
print("\nData Types:\n", df.dtypes)
print("\nMissing Values:\n", df.isnull().sum())
print("\nSummary Stats:\n", df.describe(include="all"))

# ── 2. HANDLE MISSING VALUES ─────────────────────────────────────────────────
df["Age"].fillna(df["Age"].median(), inplace=True)
df["Embarked"].fillna(df["Embarked"].mode()[0], inplace=True)

print("\nMissing after cleaning:\n", df.isnull().sum())

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Age histogram
sns.histplot(df["Age"], bins=30, kde=True, ax=axes[0], color="steelblue")
axes[0].set_title("Age Distribution")
axes[0].set_xlabel("Age")

# Fare by passenger class
sns.boxplot(x="Pclass", y="Fare", data=df, ax=axes[1], palette="Set2")
axes[1].set_title("Fare by Passenger Class")

plt.tight_layout()
plt.savefig("dist_analysis.png", dpi=150)
plt.show()

# Survival by gender
plt.figure(figsize=(7, 4))
sns.countplot(x="Sex", hue="Survived", data=df, palette="Set1")
plt.title("Survival Count by Gender")
plt.legend(["Did not survive", "Survived"])
plt.savefig("survival_gender.png", dpi=150)
plt.show()

plt.figure(figsize=(10, 6))
corr = df.corr(numeric_only=True)
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)
plt.title("Feature Correlation Matrix")
plt.tight_layout()
plt.savefig("correlation_heatmap.png", dpi=150)
plt.show()

# Cross-tabulation: survival rate per class
cross = pd.crosstab(df["Pclass"], df["Survived"], normalize="index") * 100
print("\nSurvival Rate by Passenger Class (%):\n", cross.round(1))


plt.figure(figsize=(8, 4))
sns.boxplot(x=df["Fare"], color="coral")
plt.title("Fare Outlier Detection")
plt.savefig("fare_outliers.png", dpi=150)
plt.show()

z_scores = np.abs(stats.zscore(df["Fare"]))
outliers = df[z_scores > 3]
print(f"\nFare outliers found: {len(outliers)}")
print(outliers[["Name", "Pclass", "Fare"]].head())

# Pairplot
pairplot_df = df[["Age", "Fare", "Parch", "Survived"]].copy()
pairplot_df["Survived"] = pairplot_df["Survived"].map({0: "No", 1: "Yes"})
sns.pairplot(pairplot_df, hue="Survived", plot_kws={"alpha": 0.5})
plt.suptitle("Pairplot of Key Features", y=1.02)
plt.savefig("pairplot.png", dpi=150)
plt.show()

# FacetGrid: age distribution by survival and class
g = sns.FacetGrid(df, col="Survived", row="Pclass", height=2.8, aspect=1.2)
g.map(sns.histplot, "Age", bins=18, color="teal")
g.set_titles("Survived={col_name} | Class={row_name}")
plt.savefig("facet_grid.png", dpi=150)
plt.show()


print("\n===== KEY EDA INSIGHTS =====")
print(f"Overall survival rate: {df['Survived'].mean()*100:.1f}%")
print(f"Female survival rate: {df[df['Sex']=='female']['Survived'].mean()*100:.1f}%")
print(f"Male survival rate:   {df[df['Sex']=='male']['Survived'].mean()*100:.1f}%")

for cls in [1, 2, 3]:
    rate = df[df["Pclass"] == cls]["Survived"].mean() * 100
    print(f"Class {cls} survival rate: {rate:.1f}%")

print(f"\nAge skewness: {df['Age'].skew():.3f}")
print(f"Fare kurtosis: {df['Fare'].kurtosis():.3f}")
print(f"Pearson r (Fare vs Survived): {df['Fare'].corr(df['Survived']):.3f}")