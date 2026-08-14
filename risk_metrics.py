import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "raw"
OUTPUT_PATH = BASE_DIR / "data" / "processed"

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

SCENARIO_FILE = DATA_PATH / "monte_carlo_scenarios.csv"

# --------------------------------------------------
# LOAD MONTE CARLO DATA
# --------------------------------------------------

df = pd.read_csv(SCENARIO_FILE)

print("=" * 75)
print("MONTE CARLO RISK METRICS - VaR AND CVaR")
print("=" * 75)

# --------------------------------------------------
# BASIC SUMMARY
# --------------------------------------------------

print("\n1. SCENARIO SUMMARY")
print("-" * 75)

print(f"Total Scenarios: {len(df)}")

print("\nPnL Summary:")
print(df["PnL_Total_INR"].describe())

# --------------------------------------------------
# CALCULATE VAR
# --------------------------------------------------

confidence_levels = [0.95, 0.99]

results = []

for confidence in confidence_levels:

    percentile = (1 - confidence) * 100

    var_value = -df["PnL_Total_INR"].quantile(
        1 - confidence
    )

    # CVaR / Expected Shortfall
    tail_losses = df[
        df["PnL_Total_INR"] <= -var_value
    ]

    cvar_value = -tail_losses["PnL_Total_INR"].mean()

    results.append({
        "ConfidenceLevel": f"{int(confidence * 100)}%",
        "VaR_INR": var_value,
        "CVaR_INR": cvar_value,
        "TailScenarios": len(tail_losses)
    })

risk_results = pd.DataFrame(results)

# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

print("\n2. VaR AND CVaR RESULTS")
print("-" * 75)

print(
    risk_results.to_string(index=False)
)

# --------------------------------------------------
# BEST AND WORST SCENARIOS
# --------------------------------------------------

print("\n3. WORST 10 SCENARIOS")
print("-" * 75)

worst_scenarios = (
    df.sort_values(
        by="PnL_Total_INR",
        ascending=True
    )
    .head(10)
)

print(
    worst_scenarios[
        [
            "ScenarioID",
            "ParallelShift_bps",
            "TwistFactor_bps",
            "ButterflyFactor_bps",
            "PnL_Total_INR",
            "PnL_Pct"
        ]
    ].to_string(index=False)
)

# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

risk_results.to_csv(
    OUTPUT_PATH / "var_cvar_results.csv",
    index=False
)

worst_scenarios.to_csv(
    OUTPUT_PATH / "worst_monte_carlo_scenarios.csv",
    index=False
)

print("\n" + "=" * 75)
print("MONTE CARLO VaR AND CVaR ANALYSIS COMPLETED")
print("=" * 75)

print("\nFiles created:")
print(OUTPUT_PATH / "var_cvar_results.csv")
print(OUTPUT_PATH / "worst_monte_carlo_scenarios.csv")
