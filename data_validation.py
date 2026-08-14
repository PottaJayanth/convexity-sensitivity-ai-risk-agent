import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "raw"

# File paths
BOND_FILE = DATA_PATH / "bond_portfolio_data.csv"
YIELD_FILE = DATA_PATH / "yield_curve_history.csv"
MONTE_CARLO_FILE = DATA_PATH / "monte_carlo_scenarios.csv"


def validate_dataset(df, dataset_name):
    """Validate a dataset and print a summary."""

    print("\n" + "=" * 60)
    print(f"VALIDATING: {dataset_name}")
    print("=" * 60)

    print(f"\nRows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nCOLUMN NAMES:")
    for column in df.columns:
        print(f" - {column}")

    print("\nMISSING VALUES:")
    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if missing.empty:
        print("No missing values found.")
    else:
        print(missing)

    print("\nDUPLICATE ROWS:")
    print(df.duplicated().sum())

    print("\nDATA TYPES:")
    print(df.dtypes)

    print("\n" + "=" * 60)


def main():

    # Load datasets
    bond_df = pd.read_csv(BOND_FILE)
    yield_df = pd.read_csv(YIELD_FILE)
    monte_df = pd.read_csv(MONTE_CARLO_FILE)

    # Validate datasets
    validate_dataset(bond_df, "bond_portfolio_data")
    validate_dataset(yield_df, "yield_curve_history")
    validate_dataset(monte_df, "monte_carlo_scenario")

    print("\nALL DATASETS LOADED AND VALIDATED SUCCESSFULLY.")


if __name__ == "__main__":
    main()
