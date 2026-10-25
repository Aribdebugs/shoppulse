"""Plotly chart builders for the ShopPulse dashboard. Each returns a figure."""

import plotly.express as px


def revenue_line(monthly):
    """Line chart of revenue per month. Input: output of metrics.monthly_revenue()."""
    fig = px.line(
        monthly,
        x="purchase_month",
        y="revenue",
        markers=True,
        title="Monthly Revenue",
        labels={"purchase_month": "Month", "revenue": "Revenue (R$)"},
    )
    return fig


def category_bar(top):
    """Horizontal bar chart of top categories. Input: output of metrics.top_categories()."""
    fig = px.bar(
        top,
        x="revenue",
        y="category",
        orientation="h",
        title="Top Categories by Revenue",
        labels={"revenue": "Revenue (R$)", "category": "Category"},
    )
    # Biggest bar at the top
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig


def review_bar(review_by_group):
    """Bar chart of average review score per delivery group."""
    fig = px.bar(
        review_by_group,
        x="delivery_group",
        y="review_score",
        title="Average Review Score by Delivery Time",
        labels={"delivery_group": "Delivery", "review_score": "Avg review (stars)"},
    )
    # Review stars go from 1 to 5
    fig.update_yaxes(range=[1, 5])
    return fig