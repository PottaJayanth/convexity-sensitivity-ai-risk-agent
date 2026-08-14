import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "raw"

BOND_FILE = DATA_PATH / "bond_portfolio_data.csv"

df = pd.read_csv(BOND_FILE)

print("=" * 75)
print("PORTFOLIO DV01 VALIDATION")
print("=" * 75)

# --------------------------------------------------
# METHOD 1
# Dataset DV01 scaled using Quantity and FaceValue
# --------------------------------------------------

df["DV01_Method1"] = (
    df["DV01_Per100Face"]
    * df["Quantity"]
    * df["FaceValue"]
    / 100
)

# --------------------------------------------------
# METHOD 2
# DV01 estimated from Market Value
#
# DV01 ≈ Modified Duration × Market Value × 0.0001
# --------------------------------------------------

df["DV01_Method2"] = (
    df["ModifiedDuration"]
    * df["MarketValue_INR"]
    * 0.0001
)

print("\n1. PORTFOLIO DV01 COMPARISON")
print("-" * 75)

method1_total = df["DV01_Method1"].sum()
method2_total = df["DV01_Method2"].sum()

print(f"Method 1 - Quantity Based DV01: {method1_total:,.2f} INR")
print(f"Method 2 - Market Value Based DV01: {method2_total:,.2f} INR")

print("\n2. SAMPLE COMPARISON")
print("-" * 75)

sample_columns = [
    "BondID",
    "Quantity",
    "FaceValue",
    "MarketValue_INR",
    "ModifiedDuration",
    "DV01_Per100Face",
    "DV01_Method1",
    "DV01_Method2"
]

print(
    df[sample_columns]
    .head(10)
    .to_string(index=False)
)

print("\n3. QUANTITY SUMMARY")
print("-" * 75)

print(df["Quantity"].describe())

print("\n4. FACE VALUE SUMMARY")
print("-" * 75)

print(df["FaceValue"].describe())

print("\n" + "=" * 75)
print("DV01 VALIDATION COMPLETED")
print("=" * 75)
