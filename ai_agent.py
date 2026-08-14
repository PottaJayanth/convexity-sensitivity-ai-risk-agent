import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "raw"
PROCESSED_PATH = BASE_DIR / "data" / "processed"

BOND_FILE = DATA_PATH / "bond_portfolio_data.csv"
RISK_FILE = PROCESSED_PATH / "var_cvar_results.csv"


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv(BOND_FILE)
risk_df = pd.read_csv(RISK_FILE)


# --------------------------------------------------
# PORTFOLIO METRICS
# --------------------------------------------------

portfolio_value = df["MarketValue_INR"].sum()

weighted_duration = (
    df["ModifiedDuration"] *
    df["MarketValue_INR"]
).sum() / portfolio_value

weighted_convexity = (
    df["Convexity"] *
    df["MarketValue_INR"]
).sum() / portfolio_value


# --------------------------------------------------
# AI RISK AGENT
# --------------------------------------------------

def assess_interest_rate_risk(shock_bps):

    delta_y = shock_bps / 10000

    duration_effect = (
        -weighted_duration
        * portfolio_value
        * delta_y
    )

    convexity_effect = (
        0.5
        * weighted_convexity
        * portfolio_value
        * (delta_y ** 2)
    )

    estimated_pnl = (
        duration_effect
        + convexity_effect
    )

    estimated_pnl_pct = (
        estimated_pnl / portfolio_value
    ) * 100

    var_95 = risk_df.loc[
        risk_df["ConfidenceLevel"] == "95%",
        "VaR_INR"
    ].iloc[0]

    cvar_95 = risk_df.loc[
        risk_df["ConfidenceLevel"] == "95%",
        "CVaR_INR"
    ].iloc[0]


    # --------------------------------------------------
    # RISK CLASSIFICATION
    # --------------------------------------------------

    loss = abs(estimated_pnl)

    if estimated_pnl >= 0:
        risk_level = "LOW"
        recommendation = (
            "The scenario produces a positive or neutral "
            "portfolio impact. Continue monitoring interest "
            "rate exposure."
        )

    elif loss < var_95:
        risk_level = "MODERATE"
        recommendation = (
            "The estimated loss is below the 95% VaR threshold. "
            "Monitor duration exposure and sector concentration."
        )

    elif loss < cvar_95:
        risk_level = "HIGH"
        recommendation = (
            "The estimated loss exceeds the 95% VaR threshold. "
            "Consider reducing duration exposure or hedging "
            "interest rate risk."
        )

    else:
        risk_level = "CRITICAL"
        recommendation = (
            "The estimated loss exceeds the 95% CVaR threshold. "
            "Immediate risk review is recommended. Consider "
            "duration reduction, portfolio rebalancing, and "
            "interest rate hedging."
        )


    # --------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------

    return {
        "Shock_bps": shock_bps,
        "PortfolioValue_INR": round(portfolio_value, 2),
        "WeightedDuration": round(weighted_duration, 4),
        "WeightedConvexity": round(weighted_convexity, 4),
        "EstimatedPnL_INR": round(estimated_pnl, 2),
        "EstimatedPnL_Pct": round(estimated_pnl_pct, 4),
        "VaR_95_INR": round(var_95, 2),
        "CVaR_95_INR": round(cvar_95, 2),
        "RiskLevel": risk_level,
        "Recommendation": recommendation
    }


# --------------------------------------------------
# RUN MULTIPLE TEST SCENARIOS
# --------------------------------------------------

print("=" * 75)
print("CONVEXITY & SENSITIVITY AI RISK AGENT")
print("=" * 75)

test_scenarios = [
    50,
    100,
    200,
    -50,
    -100,
    -200
]

results = []

for shock in test_scenarios:

    result = assess_interest_rate_risk(shock)

    results.append(result)

    print("\n" + "-" * 75)
    print(f"INTEREST RATE SHOCK: {shock} bps")
    print("-" * 75)

    for key, value in result.items():

        print(f"{key}: {value}")


# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

results_df = pd.DataFrame(results)

OUTPUT_FILE = (
    PROCESSED_PATH /
    "ai_agent_risk_assessment.csv"
)

results_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 75)
print("AI RISK AGENT COMPLETED SUCCESSFULLY")
print(f"Output saved to: {OUTPUT_FILE}")
print("=" * 75)
