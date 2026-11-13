
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =====================================
# LOAD CLEANED DATASETS
# =====================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = BASE_DIR

customers = pd.read_csv(
    os.path.join(DATA_DIR, "cleaned_customers.csv")
)

products = pd.read_csv(
    os.path.join(DATA_DIR, "cleaned_products.csv")
)

orders = pd.read_csv(
    os.path.join(DATA_DIR, "cleaned_orders.csv")
)

order_items = pd.read_csv(
    os.path.join(DATA_DIR, "cleaned_order_items.csv")
)

# Convert date columns
orders["order_date"] = pd.to_datetime(orders["order_date"])
orders["delivery_date"] = pd.to_datetime(
    orders["delivery_date"]
)

customers["signup_date"] = pd.to_datetime(
    customers["signup_date"]
)

# =====================================
# MERGE DATASETS
# =====================================

sales = order_items.merge(
    orders,
    on="order_id",
    how="left"
)

sales = sales.merge(
    products,
    on="product_id",
    how="left"
)

sales = sales.merge(
    customers[["customer_id", "city", "state"]],
    on="customer_id",
    how="left"
)

# =====================================
# INITIAL DATA CHECK
# =====================================


# Keep only delivered orders for revenue analysis
delivered_sales = sales[sales["order_status"] == "Delivered"].copy()

# Calculate monthly revenue
delivered_sales["month"] = (
    delivered_sales["order_date"].dt.to_period("M").astype(str)
)

monthly_revenue = delivered_sales.groupby("month")["revenue"].sum()

# 1. Monthly Revenue Trend
plt.figure(figsize=(12, 5))
monthly_revenue.plot(kind="line", marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart1_monthly_revenue.png")
plt.show()

# 2. Revenue Share by Category
category_revenue = delivered_sales.groupby("category")["revenue"].sum()

plt.figure(figsize=(8, 6))
category_revenue.plot(kind="pie", autopct="%1.1f%%")
plt.title("Revenue Share by Category")
plt.ylabel("")
plt.tight_layout()
plt.savefig("chart2_category_share.png")
plt.show()

# 3. Order Status Distribution
status_counts = orders["order_status"].value_counts()

plt.figure(figsize=(8, 5))
status_counts.plot(kind="bar")
plt.title("Order Status Distribution")
plt.xlabel("Order Status")
plt.ylabel("Number of Orders")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("chart3_order_status.png")
plt.show()

# 4. Delivery Days Distribution
delivery_data = orders.loc[
    orders["order_status"] == "Delivered", "delivery_days"
].dropna()

plt.figure(figsize=(8, 5))
sns.histplot(delivery_data, bins=20, kde=True)
plt.title("Delivery Days Distribution (Delivered Orders)")
plt.xlabel("Delivery Days")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("chart4_delivery_days.png")
plt.show()

# 5. State-wise Revenue
state_revenue = delivered_sales.groupby("state")["revenue"].sum().sort_values(
    ascending=False
)

plt.figure(figsize=(12, 5))
state_revenue.plot(kind="bar")
plt.title("State-wise Revenue")
plt.xlabel("State")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart5_state_revenue.png")
plt.show()

# 6. Discount vs Quantity
plt.figure(figsize=(8, 5))
sns.scatterplot(
    data=delivered_sales,
    x="discount_pct",
    y="quantity",
    alpha=0.5
)
plt.title("Discount Percentage vs Quantity Sold")
plt.xlabel("Discount Percentage")
plt.ylabel("Quantity Sold")
plt.tight_layout()
plt.savefig("chart6_discount_quantity.png")
plt.show()

# 7. Order Value Outlier Detection using IQR
order_values = delivered_sales.groupby("order_id")["revenue"].sum()

Q1 = order_values.quantile(0.25)
Q3 = order_values.quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = order_values[
    (order_values < lower_bound) | (order_values > upper_bound)
]

print("\nORDER VALUE OUTLIER ANALYSIS")
print("Q1:", Q1)
print("Q3:", Q3)
print("IQR:", IQR)
print("Lower Bound:", lower_bound)
print("Upper Bound:", upper_bound)
print("Number of Outlier Orders:", len(outliers))

print("\nAll six EDA charts generated successfully!")
