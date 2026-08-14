# Convexity & Sensitivity AI Risk Agent

## 📌 Project Overview

The **Convexity & Sensitivity AI Risk Agent** is an end-to-end bond portfolio risk analytics project designed to analyze interest rate sensitivity and portfolio risk.

The project combines **Python, financial risk analytics, Monte Carlo simulation, Machine Learning, AI-based risk assessment, and Power BI** to provide a comprehensive view of bond portfolio exposure.

The solution analyzes:

- Bond pricing and dirty price validation
- Macaulay Duration and Modified Duration
- Convexity and DV01
- Portfolio-level risk aggregation
- Interest rate stress testing
- Monte Carlo simulation
- Value at Risk (VaR) and Conditional Value at Risk (CVaR)
- Yield curve analytics
- Machine Learning-based duration prediction
- AI-driven risk recommendations
- Interactive Power BI dashboards

---

# 🎯 Business Problem

Bond portfolios are highly sensitive to changes in interest rates.

A portfolio manager needs to understand:

- How much the portfolio value could change when interest rates move
- Which sectors contribute the most to interest rate risk
- How duration and convexity affect portfolio sensitivity
- Potential losses under extreme market scenarios
- Value at Risk and Conditional Value at Risk
- The shape and movement of the yield curve
- Whether Machine Learning can predict bond duration
- What risk actions should be taken under different interest rate shocks

This project builds an analytics solution to answer these questions.

---

# 🏗️ Project Architecture

```text
Raw Bond & Market Data
        │
        ▼
Data Validation
        │
        ▼
Bond Pricing Validation
        │
        ▼
Duration • Convexity • DV01 Analysis
        │
        ▼
Portfolio Risk Aggregation
        │
        ├──────────────► Interest Rate Stress Testing
        │
        ├──────────────► Monte Carlo Simulation → VaR & CVaR
        │
        ├──────────────► Yield Curve Analytics
        │
        └──────────────► Machine Learning Risk Model
                                      │
                                      ▼
                              AI Risk Agent
                                      │
                                      ▼
                              Power BI Dashboard
