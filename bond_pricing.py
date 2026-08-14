import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "raw"
OUTPUT_PATH = BASE_DIR / "data" / "processed"

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

# Load data
BOND_FILE = DATA_PATH / "bond_portfolio_data.csv"
df = pd.read_csv(BOND_FILE)

print("=" * 70)
print("BOND PRICING DATA ANALYSIS")
print("=" * 70)

# --------------------------------------------------
# Compare CleanPrice + AccruedInterest with DirtyPrice
# --------------------------------------------------

df["CalculatedDirtyPrice"] = (
    df["CleanPrice"] + df["AccruedInterest"]
)

df["DirtyPriceDifference"] = (
    df["DirtyPrice"] - df["CalculatedDirtyPrice"]
)

df["AbsoluteDifference"] = (
    df["DirtyPriceDifference"].abs()
)

print("\n1. DIRTY PRICE COMPARISON")
print("-" * 70)

print(f"Total Bonds: {len(df)}")

print("\nDifference Summary:")
print(df["DirtyPriceDifference"].describe())

print("\nAverage Absolute Difference:")
print(round(df["AbsoluteDifference"].mean(), 4))

print("\nMaximum Absolute Difference:")
print(round(df["AbsoluteDifference"].max(), 4))


# --------------------------------------------------
# Check matches at different tolerances
# --------------------------------------------------

print("\n2. MATCH ANALYSIS AT DIFFERENT TOLERANCES")
print("-" * 70)

tolerances = [0.01, 0.10, 0.50, 1.00]

for tolerance in tolerances:

    matches = (
        df["AbsoluteDifference"] <= tolerance
    ).sum()

    percentage = matches / len(df) * 100

    print(
        f"Tolerance ±{tolerance}: "
        f"{matches} bonds "
        f"({percentage:.2f}%)"
    )


# --------------------------------------------------
# Show sample records
# --------------------------------------------------

print("\n3. SAMPLE PRICING COMPARISON")
print("-" * 70)

sample_columns = [
    "BondID",
    "CleanPrice",
    "AccruedInterest",
    "CalculatedDirtyPrice",
    "DirtyPrice",
    "DirtyPriceDifference",
    "AbsoluteDifference"
]

print(
    df[sample_columns]
    .head(15)
    .to_string(index=False)
)


# --------------------------------------------------
# Identify largest differences
# --------------------------------------------------

print("\n4. TOP 10 LARGEST DIFFERENCES")
print("-" * 70)

largest_differences = (
    df[sample_columns]
    .sort_values(
        by="AbsoluteDifference",
        ascending=False
    )
    .head(10)
)

print(
    largest_differences.to_string(index=False)
)


# --------------------------------------------------
# Save analysis
# --------------------------------------------------

OUTPUT_FILE = (
    OUTPUT_PATH / "bond_pricing_analysis.csv"
)

df.to_csv(OUTPUT_FILE, index=False)

print("\n" + "=" * 70)
print("BOND PRICING ANALYSIS COMPLETED")
print(f"Output saved to: {OUTPUT_FILE}")
print("=" * 70)
