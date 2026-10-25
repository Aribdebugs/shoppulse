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
    orders = orders.copy()   
    # TODO 1: convert every column in DATE_COLS to datetime (use a loop!)
    for col in DATE_COLS:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")

    # TODO 2: keep only rows where order_status == "delivered"
    orders = orders[orders["order_status"] == "delivered"]

    # TODO 3: drop rows where order_delivered_customer_date is missing
    #         (print how many you dropped; you'll quote this number in interviews)
    before = len(orders)
    orders = orders.dropna(subset=["order_delivered_customer_date"])
    print(f"Dropped {before - len(orders)} delivered orders with no delivery date")
    return orders


def add_features(df):
    """Add revenue, delivery delay, late flag, and purchase month."""
    df = df.copy()
    # TODO 4: revenue = price + freight_value
    df["revenue"] = df["price"] + df["freight_value"]

    # TODO 5: delay_days = delivered date - estimated date, in days
    df["delay_days"] = (
        df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]
    ).dt.days

    # TODO 6: is_late = delay_days > 0
    df["is_late"] = df["delay_days"] > 0

    # TODO 7: purchase_month from order_purchase_timestamp
    df["purchase_month"] = df["order_purchase_timestamp"].dt.to_period("M").dt.to_timestamp()
    return df


def build_sales_table(tables):
    """Merge items + orders + products + English categories into one table."""
    orders = clean_orders(tables["orders"])
    # TODO 8: merge items with orders (think: which "how" drops canceled orders' items?)
    # inner join: items whose order isn't in the cleaned (delivered) orders are dropped
    sales = tables["items"].merge(orders, on="order_id", how="inner")
    # TODO 9: merge in products, then the category translation
    # left joins: keep every sale even if its product/category info is missing
    sales = sales.merge(tables["products"], on="product_id", how="left")
    sales = sales.merge(tables["categories"], on="product_category_name", how="left")

    # TODO 10: fill missing English category names with "unknown"
    sales["product_category_name_english"] = sales["product_category_name_english"].fillna("unknown")

    # TODO 11: call add_features
    sales = add_features(sales)
    return sales


def build_review_table(tables):
    """Average review score per order."""
    # TODO 12: group reviews by order_id and take the mean of review_score
    return tables["reviews"].groupby("order_id", as_index=False)["review_score"].mean()


if __name__ == "__main__":
    tables = load_raw_tables()
    sales = build_sales_table(tables)
    print(sales.shape)
    print(sales.head())
    # TODO 13: save sales to PROCESSED_DIR / "sales.parquet" with .to_parquet()
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    sales.to_parquet(PROCESSED_DIR / "sales.parquet", index=False)
    print(f"Saved {len(sales):,} rows to {PROCESSED_DIR / 'sales.parquet'}")
