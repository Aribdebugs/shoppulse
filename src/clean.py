"""Clean and merge raw Olist tables into one analysis-ready sales table."""

from pathlib import Path
import pandas as pd
from load_data import load_raw_tables

PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"

DATE_COLS = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]


def clean_orders(orders):
    """Return only delivered orders with valid dates."""
    orders = orders.copy()   # work on a copy so the original stays untouched

    # Dates load as text; invalid values become NaT instead of crashing
    for col in DATE_COLS:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")

    # Only delivered orders count as real revenue
    orders = orders[orders["order_status"] == "delivered"]

    # A few "delivered" orders have no delivery date, so delay can't be computed
    before = len(orders)
    orders = orders.dropna(subset=["order_delivered_customer_date"])
    print(f"Dropped {before - len(orders)} delivered orders with no delivery date")
    return orders


def add_features(df):
    """Add revenue, delivery delay, late flag, and purchase month."""
    df = df.copy()
    # Revenue per item includes the shipping the customer paid
    df["revenue"] = df["price"] + df["freight_value"]

    # Positive = delivered after the promised date
    df["delay_days"] = (
        df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]
    ).dt.days
    df["is_late"] = df["delay_days"] > 0

    # First day of the purchase month, for monthly trends
    df["purchase_month"] = df["order_purchase_timestamp"].dt.to_period("M").dt.to_timestamp()
    return df


def build_sales_table(tables):
    """Merge items + orders + products + English categories into one table."""
    orders = clean_orders(tables["orders"])
    # Inner join: items from canceled/undelivered orders have no match and are dropped
    sales = tables["items"].merge(orders, on="order_id", how="inner")

    # Left joins: keep every sale even if its product/category info is missing
    sales = sales.merge(tables["products"], on="product_id", how="left")
    sales = sales.merge(tables["categories"], on="product_category_name", how="left")

    # Some products have no category or no English translation
    sales["product_category_name_english"] = sales["product_category_name_english"].fillna("unknown")
    sales = sales.rename(columns={"product_category_name_english": "category"})

    sales = add_features(sales)
    return sales


def build_review_table(tables):
    """Average review score per order."""
    # Some orders have several reviews, so average them to one row per order
    return tables["reviews"].groupby("order_id", as_index=False)["review_score"].mean()


if __name__ == "__main__":
    tables = load_raw_tables()
    sales = build_sales_table(tables)
    print(sales.shape)
    print(sales.head())

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    sales.to_parquet(PROCESSED_DIR / "sales.parquet", index=False)
    print(f"Saved {len(sales):,} rows to {PROCESSED_DIR / 'sales.parquet'}")

    reviews = build_review_table(tables)
    reviews.to_parquet(PROCESSED_DIR / "reviews.parquet", index=False)
    print(f"Saved {len(reviews):,} rows to {PROCESSED_DIR / 'reviews.parquet'}")
