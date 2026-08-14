import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "raw"
OUTPUT_PATH = BASE_DIR / "data" / "processed"

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

BOND_FILE = DATA_PATH / "bond_portfolio_data.csv"

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv(BOND_FILE)

print("=" * 75)
print("MACHINE LEARNING - BOND RISK MODEL")
print("=" * 75)

# --------------------------------------------------
# SELECT VERIFIED FEATURES
# --------------------------------------------------

features = [
    "YearsToMaturity",
    "CouponRate",
    "YieldToMaturity",
    "CouponFrequency",
    "CleanPrice",
    "Convexity"
]

target = "ModifiedDuration"

X = df[features]
y = df[target]

# --------------------------------------------------
# TRAIN / TEST SPLIT
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# --------------------------------------------------
# TRAIN MODEL
# --------------------------------------------------

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# --------------------------------------------------
# PREDICTIONS
# --------------------------------------------------

predictions = model.predict(X_test)

# --------------------------------------------------
# MODEL EVALUATION
# --------------------------------------------------

mae = mean_absolute_error(
    y_test,
    predictions
)

r2 = r2_score(
    y_test,
    predictions
)

print("\n1. MODEL PERFORMANCE")
print("-" * 75)

print(f"Training Records: {len(X_train)}")
print(f"Testing Records: {len(X_test)}")
print(f"Mean Absolute Error: {mae:.4f}")
print(f"R² Score: {r2:.4f}")

# --------------------------------------------------
# FEATURE IMPORTANCE
# --------------------------------------------------

importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print("\n2. FEATURE IMPORTANCE")
print("-" * 75)

print(
    importance_df.to_string(index=False)
)

# --------------------------------------------------
# SAVE PREDICTIONS
# --------------------------------------------------

results = X_test.copy()

results["Actual_ModifiedDuration"] = y_test.values
results["Predicted_ModifiedDuration"] = predictions

results.to_csv(
    OUTPUT_PATH / "ml_duration_predictions.csv",
    index=False
)

importance_df.to_csv(
    OUTPUT_PATH / "ml_feature_importance.csv",
    index=False
)

print("\n" + "=" * 75)
print("ML MODEL COMPLETED SUCCESSFULLY")
print("=" * 75)

print("\nFiles created:")
print(OUTPUT_PATH / "ml_duration_predictions.csv")
print(OUTPUT_PATH / "ml_feature_importance.csv")
