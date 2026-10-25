"""ShopPulse: e-commerce sales analytics dashboard."""

from pathlib import Path
import pandas as pd
import streamlit as st
from src import metrics, charts

DATA_DIR = Path(__file__).parent / "data" / "processed"

# Page settings: browser tab title, icon, and use the full screen width
st.set_page_config(page_title="ShopPulse", page_icon="📊", layout="wide")


# @st.cache_data = load the files once and reuse them.
# Without it, Streamlit re-reads the files every time a filter changes.
@st.cache_data
def load_data():
    sales = pd.read_parquet(DATA_DIR / "sales.parquet")
    reviews = pd.read_parquet(DATA_DIR / "reviews.parquet")
    return sales, reviews


sales, reviews = load_data()

# ---------- Sidebar filters ----------
st.sidebar.header("Filters")

min_date = sales["purchase_month"].min().date()
max_date = sales["purchase_month"].max().date()
date_range = st.sidebar.date_input(
    "Purchase month range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

categories = st.sidebar.multiselect(
    "Categories (leave empty for all)",
    options=sorted(sales["category"].unique()),
)

# Apply filters to a copy of the data
filtered = sales
if len(date_range) == 2:   # the date picker returns 1 date while the user is still choosing
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    filtered = filtered[filtered["purchase_month"].between(start, end)]
if categories:
    filtered = filtered[filtered["category"].isin(categories)]

if filtered.empty:
    st.warning("No orders match these filters.")
    st.stop()   # stop drawing the rest of the page

# ---------- Header ----------
st.title("📊 ShopPulse")
st.caption(
    "Sales analytics on delivered orders from the Olist Brazilian marketplace "
    "(2016–2018). All amounts in Brazilian reais (R$)."
)

# ---------- KPI cards ----------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue", f"R$ {metrics.total_revenue(filtered):,.0f}")
c2.metric("Orders", f"{metrics.total_orders(filtered):,}")
c3.metric("Avg order value", f"R$ {metrics.average_order_value(filtered):,.2f}")
c4.metric("Late deliveries", f"{metrics.late_delivery_rate(filtered):.1f}%")

# ---------- Charts ----------
st.plotly_chart(charts.revenue_line(metrics.monthly_revenue(filtered)))

left, right = st.columns(2)
left.plotly_chart(charts.category_bar(metrics.top_categories(filtered)))
right.plotly_chart(charts.review_bar(metrics.review_by_delivery(filtered, reviews)))

# ---------- Insights ----------
st.subheader("Key insights")
st.markdown(
    """
    - **Late delivery destroys ratings:** early orders average 4.3★ and on-time 4.0★,
      but 1–7 days late drops to 2.7★ and 8+ days late to just 1.7★.
    - **Revenue is spread out:** the top 3 categories (health & beauty, watches & gifts,
      bed/bath/table) bring in only about 25% of revenue, and the top 10 about 62%.
    - **Fast growth, then a plateau:** monthly revenue grew from about R\\$ 127k in Jan 2017
      to a R\\$ 1.15M peak in Nov 2017 (Black Friday), then levelled off around R\\$ 1.0–1.1M a month in 2018.
    """
)