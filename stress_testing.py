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
print("INTEREST RATE STRESS TESTING")
print("=" * 75)

# --------------------------------------------------
# PORTFOLIO MARKET VALUE
# --------------------------------------------------

portfolio_value = df["MarketValue_INR"].sum()

# --------------------------------------------------
# STRESS SCENARIOS
# Yield change in basis points
# --------------------------------------------------

stress_scenarios = {
    "Up 50 bps": 0.005,
    "Down 50 bps": -0.005,
    "Up 100 bps": 0.010,
    "Down 100 bps": -0.010,
    "Up 200 bps": 0.020,
    "Down 200 bps": -0.020
}

results = []

for scenario, delta_y in stress_scenarios.items():

    # Duration effect
    df["DurationPnL"] = (
        -df["ModifiedDuration"]
        * df["MarketValue_INR"]
        * delta_y
    )

    # Convexity effect
    df["ConvexityPnL"] = (
        0.5
        * df["Convexity"]
        * df["MarketValue_INR"]
        * (delta_y ** 2)
    )

    # Total P&L
    df["TotalPnL"] = (
        df["DurationPnL"]
        + df["ConvexityPnL"]
    )

    scenario_pnl = df["TotalPnL"].sum()

    stressed_value = (
        portfolio_value
        + scenario_pnl
    )

    results.append({
        "Scenario": scenario,
        "YieldChange": delta_y,
        "PortfolioPnL_INR": scenario_pnl,
        "PortfolioPnL_Pct": (
            scenario_pnl / portfolio_value
        ) * 100,
        "StressedPortfolioValue_INR": stressed_value
    })


# --------------------------------------------------
# CREATE RESULTS
# --------------------------------------------------

stress_results = pd.DataFrame(results)

print("\nSTRESS TEST RESULTS")
print("-" * 75)

print(
    stress_results.to_string(
        index=False
    )
)

# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

OUTPUT_FILE = (
    OUTPUT_PATH /
    "interest_rate_stress_results.csv"
)

stress_results.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 75)
print("STRESS TESTING COMPLETED SUCCESSFULLY")
print(f"Output saved to: {OUTPUT_FILE}")
print("=" * 75)
