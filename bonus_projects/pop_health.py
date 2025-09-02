import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import sqlite3
from datetime import datetime, timedelta

# Set style for better visualizations
plt.style.use("seaborn-v0_8")
sns.set_palette("husl")

# Generate synthetic healthcare data for demonstration
np.random.seed(42)


def generate_patient_data(n_patients=1000):
    """Generate synthetic patient data for analysis"""

    # Patient demographics
    patient_ids = [f"P{i:06d}" for i in range(1, n_patients + 1)]
    ages = np.random.normal(65, 12, n_patients).astype(int)
    ages = np.clip(ages, 25, 85)  # Keep realistic age range

    # Social determinants (correlated with outcomes)
    income_levels = np.random.choice(
        ["Low", "Medium", "High"], n_patients, p=[0.4, 0.4, 0.2]
    )
    education_levels = np.random.choice(
        ["Less than HS", "HS/GED", "College+"], n_patients, p=[0.3, 0.4, 0.3]
    )
    insurance_types = np.random.choice(
        ["Medicaid", "Medicare", "Commercial"], n_patients, p=[0.25, 0.45, 0.3]
    )

    # Geographic data
    zip_codes = np.random.choice([f"{i:05d}" for i in range(10001, 10100)], n_patients)

    return pd.DataFrame(
        {
            "patient_id": patient_ids,
            "age": ages,
            "income_level": income_levels,
            "education_level": education_levels,
            "insurance_type": insurance_types,
            "zip_code": zip_codes,
        }
    )


def generate_clinical_data(patients_df):
    """Generate clinical outcomes data"""
    n_patients = len(patients_df)

    # Create bias based on social determinants
    income_bias = {"Low": 0.3, "Medium": 0.0, "High": -0.2}
    education_bias = {"Less than HS": 0.2, "HS/GED": 0.0, "College+": -0.15}

    clinical_data = []

    for _, patient in patients_df.iterrows():
        # Calculate risk factors based on social determinants
        base_risk = 0.0
        base_risk += income_bias[patient["income_level"]]
        base_risk += education_bias[patient["education_level"]]

        # HbA1c levels (diabetes control marker)
        hba1c_mean = 7.5 + base_risk  # Target is <7.0
        hba1c = max(5.5, np.random.normal(hba1c_mean, 1.2))

        # Healthcare utilization
        er_visits = max(0, int(np.random.poisson(1.5 + base_risk * 2)))
        primary_care_visits = max(1, int(np.random.poisson(4 - base_risk)))

        # Complications
        has_complications = np.random.random() < (0.2 + base_risk * 0.3)

        clinical_data.append(
            {
                "patient_id": patient["patient_id"],
                "hba1c_latest": round(hba1c, 1),
                "controlled_diabetes": hba1c < 7.0,
                "er_visits_12mo": er_visits,
                "pcp_visits_12mo": primary_care_visits,
                "has_complications": has_complications,
                "medication_adherence": max(
                    0.3, min(1.0, np.random.normal(0.8 - base_risk * 0.2, 0.15))
                ),
            }
        )

    return pd.DataFrame(clinical_data)


# Generate the datasets
print("Generating synthetic healthcare data...")
patients = generate_patient_data(1000)
clinical = generate_clinical_data(patients)

# Merge datasets
df = patients.merge(clinical, on="patient_id")

print(f"Dataset created with {len(df)} patients")
print("\nFirst few rows:")
print(df.head())

# SQL Analysis Example using SQLite
print("\n" + "=" * 50)
print("SQL ANALYSIS")
print("=" * 50)

# Create in-memory SQLite database
conn = sqlite3.connect(":memory:")

# Load data into SQLite
df.to_sql("patient_data", conn, index=False, if_exists="replace")

# Example SQL queries for population health analysis
queries = {
    "Diabetes Control by Income Level": """
    SELECT 
        income_level,
        COUNT(*) as total_patients,
        SUM(CASE WHEN controlled_diabetes = 1 THEN 1 ELSE 0 END) as controlled_patients,
        ROUND(AVG(hba1c_latest), 2) as avg_hba1c,
        ROUND(100.0 * SUM(CASE WHEN controlled_diabetes = 1 THEN 1 ELSE 0 END) / COUNT(*), 1) as control_rate_pct
    FROM patient_data
    GROUP BY income_level
    ORDER BY control_rate_pct DESC
    """,
    "High Utilizers Analysis": """
    SELECT 
        income_level,
        education_level,
        COUNT(*) as patient_count,
        ROUND(AVG(er_visits_12mo), 1) as avg_er_visits,
        ROUND(AVG(pcp_visits_12mo), 1) as avg_pcp_visits
    FROM patient_data
    WHERE er_visits_12mo >= 3
    GROUP BY income_level, education_level
    ORDER BY avg_er_visits DESC
    """,
    "Care Gaps by Demographics": """
    SELECT 
        insurance_type,
        ROUND(AVG(medication_adherence), 3) as avg_adherence,
        ROUND(100.0 * SUM(CASE WHEN has_complications = 1 THEN 1 ELSE 0 END) / COUNT(*), 1) as complication_rate_pct,
        COUNT(*) as patient_count
    FROM patient_data
    GROUP BY insurance_type
    ORDER BY complication_rate_pct DESC
    """,
}

# Execute SQL queries
for query_name, query in queries.items():
    print(f"\n{query_name}:")
    print("-" * len(query_name))
    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))

conn.close()

# PYTHON ANALYSIS AND VISUALIZATIONS
print("\n" + "=" * 50)
print("PYTHON STATISTICAL ANALYSIS")
print("=" * 50)

# 1. Statistical testing for disparities
print("\n1. Statistical Analysis of HbA1c by Income Level")
income_groups = [
    df[df["income_level"] == level]["hba1c_latest"]
    for level in ["Low", "Medium", "High"]
]
f_stat, p_value = stats.f_oneway(*income_groups)
print(f"ANOVA F-statistic: {f_stat:.3f}, p-value: {p_value:.3f}")

if p_value < 0.05:
    print("Significant differences found between income groups!")
else:
    print("No significant differences between income groups.")

# 2. Correlation analysis
print("\n2. Correlation Analysis")
# Create numeric versions for correlation
df_numeric = df.copy()
df_numeric["income_numeric"] = df["income_level"].map(
    {"Low": 1, "Medium": 2, "High": 3}
)
df_numeric["education_numeric"] = df["education_level"].map(
    {"Less than HS": 1, "HS/GED": 2, "College+": 3}
)

correlations = df_numeric[
    [
        "income_numeric",
        "education_numeric",
        "hba1c_latest",
        "er_visits_12mo",
        "medication_adherence",
    ]
].corr()
print("Correlation with HbA1c levels:")
print(correlations["hba1c_latest"].sort_values())

# 3. Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle("Diabetes Care Disparities Analysis", fontsize=16, fontweight="bold")

# Plot 1: HbA1c by Income Level
sns.boxplot(data=df, x="income_level", y="hba1c_latest", ax=axes[0, 0])
axes[0, 0].axhline(y=7.0, color="red", linestyle="--", alpha=0.7, label="Target HbA1c")
axes[0, 0].set_title("HbA1c Levels by Income Level")
axes[0, 0].set_ylabel("HbA1c (%)")
axes[0, 0].legend()

# Plot 2: Control rates by education
control_rates = df.groupby("education_level")["controlled_diabetes"].mean() * 100
control_rates.plot(kind="bar", ax=axes[0, 1], color="skyblue")
axes[0, 1].set_title("Diabetes Control Rate by Education Level")
axes[0, 1].set_ylabel("Control Rate (%)")
axes[0, 1].tick_params(axis="x", rotation=45)

# Plot 3: ER Visits by Insurance Type
sns.boxplot(data=df, x="insurance_type", y="er_visits_12mo", ax=axes[1, 0])
axes[1, 0].set_title("Emergency Room Visits by Insurance Type")
axes[1, 0].set_ylabel("ER Visits (12 months)")

# Plot 4: Medication Adherence vs Outcomes
scatter = axes[1, 1].scatter(
    df["medication_adherence"],
    df["hba1c_latest"],
    c=df["income_numeric"],
    cmap="viridis",
    alpha=0.6,
)
axes[1, 1].set_xlabel("Medication Adherence")
axes[1, 1].set_ylabel("HbA1c (%)")
axes[1, 1].set_title("Medication Adherence vs Diabetes Control")
plt.colorbar(scatter, ax=axes[1, 1], label="Income Level (1=Low, 3=High)")

plt.tight_layout()
plt.show()

# 4. Risk Stratification Model (Simple)
print("\n3. Risk Stratification")
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Prepare features for modeling
features = pd.get_dummies(
    df[["age", "income_level", "education_level", "insurance_type"]]
)
target = df["has_complications"]

X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.3, random_state=42
)

# Simple Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Feature importance
feature_importance = pd.DataFrame(
    {"feature": features.columns, "importance": rf_model.feature_importances_}
).sort_values("importance", ascending=False)

print("Top Risk Factors for Complications:")
print(feature_importance.head(10))

# Model performance
y_pred = rf_model.predict(X_test)
print(f"\nModel Accuracy: {rf_model.score(X_test, y_test):.3f}")

# 5. Population Health Summary
print("\n" + "=" * 50)
print("POPULATION HEALTH INSIGHTS")
print("=" * 50)

insights = {
    "Total Population": len(df),
    "Overall Diabetes Control Rate": f"{df['controlled_diabetes'].mean()*100:.1f}%",
    "Average HbA1c": f"{df['hba1c_latest'].mean():.2f}%",
    "High ER Utilizers (3+ visits)": f"{(df['er_visits_12mo'] >= 3).sum()} patients ({(df['er_visits_12mo'] >= 3).mean()*100:.1f}%)",
    "Patients with Complications": f"{df['has_complications'].sum()} patients ({df['has_complications'].mean()*100:.1f}%)",
}

for key, value in insights.items():
    print(f"{key}: {value}")

# Disparities summary
print("\nKey Disparities Identified:")
low_income_control = df[df["income_level"] == "Low"]["controlled_diabetes"].mean() * 100
high_income_control = (
    df[df["income_level"] == "High"]["controlled_diabetes"].mean() * 100
)
disparity_gap = high_income_control - low_income_control

print(f"• Income-based control gap: {disparity_gap:.1f} percentage points")
print(
    f"• Low-income patients have {df[df['income_level'] == 'Low']['er_visits_12mo'].mean():.1f} avg ER visits"
)
print(
    f"• High-income patients have {df[df['income_level'] == 'High']['er_visits_12mo'].mean():.1f} avg ER visits"
)

print(f"\nRecommendations:")
print("• Implement targeted interventions for low-income populations")
print("• Enhance care coordination to reduce ER utilization")
print("• Develop health education programs focused on medication adherence")
print("• Consider social determinants in care planning")
