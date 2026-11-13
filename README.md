# E-commerce Sales Analysis

An end-to-end data analytics project using **Python, MySQL and Power BI** to analyse e-commerce sales, customer behaviour, product performance and delivery operations.

## Project Overview

This project analyses four e-commerce datasets containing customer, product, order and order-item information. It includes data cleaning, exploratory data analysis, SQL business analysis and an interactive Power BI dashboard.

## Tech Stack

- **Python:** Pandas, NumPy, Matplotlib
- **Database:** MySQL
- **Data Visualisation:** Power BI
- **Analytics:** SQL, DAX

## Dataset

| Dataset | Records |
|---|---:|
| Customers | 3,000 |
| Products | 150 |
| Orders | 15,000 |
| Order Items | 30,058 |
| **Total** | **48,208** |

## Project Workflow

1. Data cleaning and preparation using Python.
2. Exploratory Data Analysis using Pandas and Matplotlib.
3. Importing cleaned datasets into MySQL.
4. SQL analysis using joins, aggregations and window functions.
5. Building an interactive Power BI dashboard.

## SQL Analysis

Seven business questions were explored:

1. Monthly revenue and month-over-month growth.
2. Top 10 products by revenue and category ranking.
3. Repeat customer percentage.
4. Average delivery days by category and state.
5. Running total customer spending.
6. Top 10% customers by lifetime spending.
7. Cancellation and return rates by payment method.

## Key Findings

- Repeat customer rate: **85.40%**
- Highest-revenue product: **Electronics Item 21**
- Highest monthly revenue: **April 2024 — ₹14.69 million**
- Highest cancellation rate: **COD — 6.32%**
- Highest return rate: **Debit Card — 5.46%**
- Highest-spending customer in the top-decile results: **C01604 — approximately ₹35.56 lakh**

## Exploratory Data Analysis

Six visualisations were created:

- Monthly Revenue Trend
- Revenue Share by Category
- Order Status Distribution
- Delivery Days Distribution
- State-wise Revenue
- Discount vs Quantity Analysis

## Power BI Dashboard

The interactive dashboard includes five KPI cards:

- Total Revenue: ₹312.09 million
- Total Orders: 15,000
- Average Order Value: ₹24,180
- Repeat Customer Percentage: 85.40%
- Average Delivery Days: 7.96

It also includes six visualisations and four interactive slicers:

- Order Date
- Product Category
- Customer State
- Payment Method

## Project Structure

```text
Ecommerce_Sales_Analysis/
│
├── task1_data_cleaning.py
├── task1_queries.sql
├── Ecommerce_Sales_Analysis_Dashboard.pbix
│
└── cleaned_data/
    ├── cleaned_customers.csv
    ├── cleaned_products.csv
    ├── cleaned_orders.csv
    ├── cleaned_order_items.csv
    └── task4_eda_visualization.py
```

## Conclusion

This project demonstrates practical data analytics skills, including Python-based data preparation, SQL querying, exploratory analysis and interactive dashboard development. It provides business insights that can support sales monitoring, customer segmentation and operational analysis.
