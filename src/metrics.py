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


def review_by_delivery(sales, reviews):
    """Average review score for early / on-time / late orders."""
    # One row per order, so orders with many items don't count extra
    orders = sales.drop_duplicates("order_id")[["order_id", "delay_days"]]

    # Inner join: only orders that have a review
    orders = orders.merge(reviews, on="order_id", how="inner")

    # Bins are right-inclusive: <=-1 early, 0 on time, 1-7 late, 8+ very late
    orders["delivery_group"] = pd.cut(
        orders["delay_days"],
        bins=[-1000, -1, 0, 7, 1000],
        labels=["Early", "On time", "1-7 days late", "8+ days late"],
    )
    return orders.groupby("delivery_group", observed=True)["review_score"].mean().reset_index()