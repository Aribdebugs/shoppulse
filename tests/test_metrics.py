import sys
from pathlib import Path
import pandas as pd
import pytest

# Let this test file find src/metrics.py
sys.path.append(str(Path(__file__).parent.parent / "src"))
import metrics


def make_fake_sales():
    """3 rows, 2 orders. Order A has 2 items and is late; order B has 1 item, on time."""
    return pd.DataFrame({
        "order_id": ["A", "A", "B"],
        "revenue":  [100.0, 50.0, 30.0],
        "is_late":  [True, True, False],
        "purchase_month": ["2017-01", "2017-01", "2017-02"],
        "category": ["toys", "toys", "books"],
    })


def test_total_orders_counts_unique_orders():
    sales = make_fake_sales()
    assert metrics.total_orders(sales) == 2      # 3 rows, but only 2 orders


def test_total_revenue():
    sales = make_fake_sales()
    assert metrics.total_revenue(sales) == 180.0     # 100 + 50 + 30


def test_average_order_value():
    sales = make_fake_sales()
    assert metrics.average_order_value(sales) == 90.0    # 180 / 2 orders


def test_late_delivery_rate():
    sales = make_fake_sales()
    # 1 of 2 ORDERS late, not 2 of 3 rows
    assert metrics.late_delivery_rate(sales) == pytest.approx(50.0)


def test_monthly_revenue():
    result = metrics.monthly_revenue(make_fake_sales())
    assert list(result.columns) == ["purchase_month", "revenue"]
    assert result["revenue"].tolist() == [150.0, 30.0]


def test_top_categories():
    result = metrics.top_categories(make_fake_sales(), n=1)
    assert result["category"].tolist() == ["toys"]
    assert result["revenue"].tolist() == [150.0]
