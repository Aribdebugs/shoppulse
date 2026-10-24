# 📊 ShopPulse: E-commerce Sales Analytics Dashboard

🔗 **Live demo:** [your-app.streamlit.app](link)

## Overview
ShopPulse turns 100K+ raw orders from a Brazilian marketplace into an
interactive dashboard that answers: Is revenue growing? What sells?
Do late deliveries hurt customer reviews?

## Key Insights
- Revenue grew X% from [month] to [month]
- [Category] drives Y% of revenue
- Late orders average Z fewer review stars than on-time orders

## Features
- KPI cards: revenue, orders, average order value, on-time delivery rate
- Monthly revenue trend
- Top 10 categories
- Delivery delay vs. review score analysis
- Filters by date range and state

## Screenshots
![Dashboard](assets/screenshots/dashboard.png)

## How to Run
```bash
git clone https://github.com/shahipervez/shoppulse.git
cd shoppulse
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Tech Stack
Python · pandas · Plotly · Streamlit · Parquet

## Data
[Olist Brazilian E-Commerce Public Dataset](kaggle link), 2016–2018.

## Project Structure
(paste your folder tree)

## Future Improvements
- Revenue forecasting
- Customer segmentation (see my SegmentIQ project)