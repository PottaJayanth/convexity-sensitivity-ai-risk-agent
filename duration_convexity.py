import pandas as pd
from pathlib import Path

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
print("DURATION, CONVEXITY AND DV01 ANALYSIS")
print("=" * 75)

# --------------------------------------------------
# 1. BASIC DATA CHECK
# --------------------------------------------------

required_columns = [
    "BondID",
    "DirtyPrice",
    "MacaulayDuration",
    "ModifiedDuration",
    "Convexity",
    "DV01_Per100Face",
    "YieldToMaturity",
    "CouponFrequency",
    "FaceValue"
]

print("\n1. REQUIRED COLUMN CHECK")
print("-" * 75)

for column in required_columns:
    if column in df.columns:
        print(f"✓ {column}")
    else:
        print(f"✗ MISSING: {column}")

# --------------------------------------------------
# 2. MACAULAY vs MODIFIED DURATION CHECK
#
# Modified Duration ≈ Macaulay Duration /
# (1 + YieldToMaturity / CouponFrequency)
# --------------------------------------------------

df["CalculatedModifiedDuration"] = (
    df["MacaulayDuration"] /
    (1 + df["YieldToMaturity"] / df["CouponFrequency"])
)

df["ModifiedDurationDifference"] = (
    df["ModifiedDuration"] -
    df["CalculatedModifiedDuration"]
)

df["ModifiedDurationAbsDifference"] = (
    df["ModifiedDurationDifference"].abs()
)

# --------------------------------------------------
# 3. DV01 APPROXIMATION
#
# DV01 ≈ Modified Duration × Price × 0.0001
#
# Using DirtyPrice because DV01 is price sensitivity
# --------------------------------------------------

df["CalculatedDV01_Per100Face"] = (
    df["ModifiedDuration"] *
    df["DirtyPrice"] *
    0.0001
)

df["DV01Difference"] = (
    df["DV01_Per100Face"] -
    df["CalculatedDV01_Per100Face"]
)

df["DV01AbsDifference"] = (
    df["DV01Difference"].abs()
)

# --------------------------------------------------
# 4. DISPLAY RESULTS
# --------------------------------------------------

print("\n2. MODIFIED DURATION VALIDATION")
print("-" * 75)

print("Average Absolute Difference:")
print(round(df["ModifiedDurationAbsDifference"].mean(), 6))

print("Maximum Absolute Difference:")
print(round(df["ModifiedDurationAbsDifference"].max(), 6))


print("\n3. DV01 VALIDATION")
print("-" * 75)

print("Average Absolute Difference:")
print(round(df["DV01AbsDifference"].mean(), 6))

print("Maximum Absolute Difference:")
print(round(df["DV01AbsDifference"].max(), 6))


# --------------------------------------------------
# 5. CONVEXITY SUMMARY
# --------------------------------------------------

print("\n4. CONVEXITY SUMMARY")
print("-" * 75)

print(df["Convexity"].describe())


# --------------------------------------------------
# 6. SAMPLE OUTPUT
# --------------------------------------------------

print("\n5. SAMPLE RESULTS")
print("-" * 75)

sample_columns = [
    "BondID",
    "MacaulayDuration",
    "ModifiedDuration",
    "CalculatedModifiedDuration",
    "ModifiedDurationDifference",
    "Convexity",
    "DV01_Per100Face",
    "CalculatedDV01_Per100Face",
    "DV01Difference"
]

print(
    df[sample_columns]
    .head(10)
    .to_string(index=False)
)

# --------------------------------------------------
# 7. SAVE RESULTS
# --------------------------------------------------

OUTPUT_FILE = (
    OUTPUT_PATH /
    "duration_convexity_analysis.csv"
)

df.to_csv(OUTPUT_FILE, index=False)

print("\n" + "=" * 75)
print("DURATION, CONVEXITY AND DV01 ANALYSIS COMPLETED")
print(f"Output saved to: {OUTPUT_FILE}")
print("=" * 75)
