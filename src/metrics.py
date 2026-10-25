"""KPI calculations for the ShopPulse dashboard. Input: the cleaned sales table."""

import pandas as pd


def total_revenue(sales):
    """Sum of revenue across all items."""
    # TODO 1
    return sales["revenue"].sum()


def total_orders(sales):
    """Number of unique orders (NOT number of rows)."""
    # TODO 2
    return sales["order_id"].nunique()


def average_order_value(sales):
    """Average money spent per order = total revenue / total orders."""
    # TODO 3: reuse your two functions above
    return total_revenue(sales) / total_orders(sales)


def late_delivery_rate(sales):
    """% of ORDERS delivered late (0-100). One row per order first!"""
    # TODO 4
    # is_late is the same for every item in an order, so keep one row per order
    orders = sales.drop_duplicates("order_id")
    return orders["is_late"].mean() * 100


def monthly_revenue(sales):
    """Return a DataFrame with columns: purchase_month, revenue."""
    # TODO 5: groupby + sum + reset_index()
    # Hint: convert purchase_month to string so Plotly can plot it later
    monthly = sales.groupby("purchase_month")["revenue"].sum().reset_index()
    monthly["purchase_month"] = monthly["purchase_month"].astype(str)
    return monthly


def top_categories(sales, n=10):
    """Return the top n categories by revenue."""
    # TODO 6: groupby + sum + sort_values + head(n)
    return (
        sales.groupby("category")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )
