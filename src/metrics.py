"""KPI calculations for the ShopPulse dashboard. Input: the cleaned sales table."""

import pandas as pd


def total_revenue(sales):
    """Sum of revenue across all items."""
    return sales["revenue"].sum()


def total_orders(sales):
    """Number of unique orders (NOT number of rows)."""
    return sales["order_id"].nunique()


def average_order_value(sales):
    """Average money spent per order = total revenue / total orders."""
    return total_revenue(sales) / total_orders(sales)


def late_delivery_rate(sales):
    """% of ORDERS delivered late (0-100). One row per order first!"""

    orders = sales.drop_duplicates("order_id")
    return orders["is_late"].mean() * 100


def monthly_revenue(sales):
    """Return a DataFrame with columns: purchase_month, revenue."""
    monthly = sales.groupby("purchase_month")["revenue"].sum().reset_index()
    monthly["purchase_month"] = monthly["purchase_month"].astype(str)
    return monthly


def top_categories(sales, n=10):
    """Return the top n categories by revenue."""
    return (
        sales.groupby("category")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )
