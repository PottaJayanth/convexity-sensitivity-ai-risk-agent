import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "raw"
OUTPUT_PATH = BASE_DIR / "data" / "processed"

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

YIELD_FILE = DATA_PATH / "yield_curve_history.csv"

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv(YIELD_FILE)

# Convert date column
df["CurveDate"] = pd.to_datetime(df["CurveDate"])

print("=" * 75)
print("YIELD CURVE ANALYTICS")
print("=" * 75)

print(f"\nTotal Records: {len(df)}")
print(f"Date Range: {df['CurveDate'].min().date()} to {df['CurveDate'].max().date()}")

# --------------------------------------------------
# LATEST CURVE
# --------------------------------------------------

latest_date = df["CurveDate"].max()

latest_curve = df[
    df["CurveDate"] == latest_date
].copy()

latest_curve = latest_curve.sort_values("Tenor_Years")

print("\nLATEST YIELD CURVE")
print("-" * 75)

print(
    latest_curve[
        [
            "Currency",
            "Tenor_Years",
            "TenorLabel",
            "Yield",
            "ZeroRate",
            "ForwardRate",
            "DiscountFactor"
        ]
    ].to_string(index=False)
)

# --------------------------------------------------
# CURVE SUMMARY BY DATE
# --------------------------------------------------

curve_summary = (
    df.groupby("CurveDate")
    .agg(
        AverageYield=("Yield", "mean"),
        MinYield=("Yield", "min"),
        MaxYield=("Yield", "max"),
        AverageZeroRate=("ZeroRate", "mean")
    )
    .reset_index()
)

# --------------------------------------------------
# CURVE SLOPE
# Longest tenor yield - shortest tenor yield
# --------------------------------------------------

curve_pivot = df.pivot_table(
    index="CurveDate",
    columns="Tenor_Years",
    values="Yield"
)

short_tenor = curve_pivot.columns.min()
long_tenor = curve_pivot.columns.max()

curve_summary["CurveSlope"] = (
    curve_pivot[long_tenor].values
    - curve_pivot[short_tenor].values
)

print("\nCURVE SLOPE ANALYSIS")
print("-" * 75)

print(f"Shortest Tenor: {short_tenor} years")
print(f"Longest Tenor: {long_tenor} years")

print("\nLatest Curve Slope:")
print(
    round(
        curve_summary.iloc[-1]["CurveSlope"],
        6
    )
)

# --------------------------------------------------
# SAVE OUTPUTS
# --------------------------------------------------

latest_curve.to_csv(
    OUTPUT_PATH / "latest_yield_curve.csv",
    index=False
)

curve_summary.to_csv(
    OUTPUT_PATH / "yield_curve_summary.csv",
    index=False
)

print("\n" + "=" * 75)
print("YIELD CURVE ANALYTICS COMPLETED SUCCESSFULLY")
print("=" * 75)

print("\nFiles created:")
print(OUTPUT_PATH / "latest_yield_curve.csv")
print(OUTPUT_PATH / "yield_curve_summary.csv")
