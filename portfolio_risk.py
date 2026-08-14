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
# LOAD BOND PORTFOLIO
# --------------------------------------------------

df = pd.read_csv(BOND_FILE)

print("=" * 75)
print("PORTFOLIO RISK AGGREGATION")
print("=" * 75)


# --------------------------------------------------
# PORTFOLIO LEVEL METRICS
# --------------------------------------------------

total_market_value = df["MarketValue_INR"].sum()

weighted_modified_duration = (
    (df["ModifiedDuration"] * df["MarketValue_INR"]).sum()
    / total_market_value
)

weighted_convexity = (
    (df["Convexity"] * df["MarketValue_INR"]).sum()
    / total_market_value
)

total_dv01 = (
    df["DV01_Per100Face"] *
    df["Quantity"] *
    df["FaceValue"] / 100
).sum()


print("\n1. PORTFOLIO LEVEL RISK METRICS")
print("-" * 75)

print(f"Total Market Value INR: {total_market_value:,.2f}")

print(
    f"Weighted Modified Duration: "
    f"{weighted_modified_duration:.4f}"
)

print(
    f"Weighted Convexity: "
    f"{weighted_convexity:.4f}"
)

print(
    f"Estimated Portfolio DV01: "
    f"{total_dv01:,.2f} INR"
)


# --------------------------------------------------
# SECTOR LEVEL RISK
# --------------------------------------------------

sector_risk = (
    df.groupby("Sector")
    .apply(
        lambda x: pd.Series({
            "BondCount": len(x),

            "MarketValue_INR":
                x["MarketValue_INR"].sum(),

            "PortfolioWeight":
                x["MarketValue_INR"].sum()
                / total_market_value,

            "WeightedModifiedDuration":
                (
                    x["ModifiedDuration"]
                    * x["MarketValue_INR"]
                ).sum()
                / x["MarketValue_INR"].sum(),

            "WeightedConvexity":
                (
                    x["Convexity"]
                    * x["MarketValue_INR"]
                ).sum()
                / x["MarketValue_INR"].sum()
        })
    )
    .reset_index()
)


print("\n2. SECTOR LEVEL RISK")
print("-" * 75)

print(
    sector_risk
    .sort_values(
        by="MarketValue_INR",
        ascending=False
    )
    .to_string(index=False)
)


# --------------------------------------------------
# CREDIT RATING LEVEL RISK
# --------------------------------------------------

rating_risk = (
    df.groupby("CreditRating")
    .apply(
        lambda x: pd.Series({

            "BondCount": len(x),

            "MarketValue_INR":
                x["MarketValue_INR"].sum(),

            "PortfolioWeight":
                x["MarketValue_INR"].sum()
                / total_market_value,

            "WeightedModifiedDuration":
                (
                    x["ModifiedDuration"]
                    * x["MarketValue_INR"]
                ).sum()
                / x["MarketValue_INR"].sum(),

            "WeightedConvexity":
                (
                    x["Convexity"]
                    * x["MarketValue_INR"]
                ).sum()
                / x["MarketValue_INR"].sum()

        })
    )
    .reset_index()
)


print("\n3. CREDIT RATING LEVEL RISK")
print("-" * 75)

print(
    rating_risk
    .sort_values(
        by="MarketValue_INR",
        ascending=False
    )
    .to_string(index=False)
)


# --------------------------------------------------
# SAVE OUTPUTS
# --------------------------------------------------

portfolio_summary = pd.DataFrame({

    "Metric": [
        "Total Market Value INR",
        "Weighted Modified Duration",
        "Weighted Convexity",
        "Estimated Portfolio DV01"
    ],

    "Value": [
        total_market_value,
        weighted_modified_duration,
        weighted_convexity,
        total_dv01
    ]

})


portfolio_summary.to_csv(
    OUTPUT_PATH / "portfolio_risk_summary.csv",
    index=False
)

sector_risk.to_csv(
    OUTPUT_PATH / "sector_risk_analysis.csv",
    index=False
)

rating_risk.to_csv(
    OUTPUT_PATH / "rating_risk_analysis.csv",
    index=False
)


print("\n" + "=" * 75)
print("PORTFOLIO RISK AGGREGATION COMPLETED SUCCESSFULLY")
print("=" * 75)

print("\nFiles created:")

print(
    OUTPUT_PATH / "portfolio_risk_summary.csv"
)

print(
    OUTPUT_PATH / "sector_risk_analysis.csv"
)

print(
    OUTPUT_PATH / "rating_risk_analysis.csv"
)
