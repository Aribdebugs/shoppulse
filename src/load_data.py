"""Load the raw Olist CSV files and merge them into one table."""

from pathlib import Path   # Path handles file paths the same way on Windows and Mac
import pandas as pd

# Folder where the raw Kaggle CSVs live.
# __file__ is this script's location; .parent goes up one folder (to src/),
# and the second .parent goes up again (to shoppulse/).
RAW_DIR = Path(__file__).parent.parent / "data" / "raw" /"dataset"


def load_raw_tables():
    """Read the 5 CSVs we need and return them in a dictionary."""
    files = {
        "orders": "olist_orders_dataset.csv",
        "items": "olist_order_items_dataset.csv",
        "products": "olist_products_dataset.csv",
        "categories": "product_category_name_translation.csv",
        "reviews": "olist_order_reviews_dataset.csv",
    }
    tables = {}
    for name, filename in files.items():          # loop over each key-value pair
        tables[name] = pd.read_csv(RAW_DIR / filename)
        print(f"Loaded {name}: {len(tables[name]):,} rows")
    return tables


def inspect(df, name):
    """Print a quick health check of one table."""
    print(f"\n=== {name} ===")
    print("Shape (rows, columns):", df.shape)
    print("Missing values per column:")
    missing = df.isna().sum()
    print(missing[missing > 0])                   # only show columns that have gaps


# This block only runs when you execute this file directly
# (python src/load_data.py), not when another file imports it.
if __name__ == "__main__":
    tables = load_raw_tables()
    for name, df in tables.items():
        inspect(df, name)