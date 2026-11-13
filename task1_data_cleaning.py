
import pandas as pd
import numpy as np
import os

print("STARTING E-COMMERCE DATA CLEANING")

# ==========================================
# 1. LOAD DATASETS
# ==========================================

customers = pd.read_csv("task1_customers.csv")
products = pd.read_csv("task1_products.csv")
orders = pd.read_csv("task1_orders.csv")
order_items = pd.read_csv("task1_order_items.csv")

print("\nAll four datasets loaded successfully!")

# ==========================================
# 2. CHECK INITIAL SHAPES
# ==========================================

print("\nINITIAL DATASET SHAPES")

print("Customers:", customers.shape)
print("Products:", products.shape)
print("Orders:", orders.shape)
print("Order Items:", order_items.shape)

# ==========================================
# 3. REMOVE DUPLICATE ORDERS
# ==========================================

print("\nCHECKING DUPLICATE ORDERS")

duplicate_count = orders.duplicated(
    subset=["order_id"]
).sum()

print("Duplicate order IDs:", duplicate_count)

# Check whether duplicate IDs have conflicting records
duplicate_rows = orders[
    orders.duplicated(subset=["order_id"], keep=False)
]

conflicting_ids = []

for column in orders.columns.drop("order_id"):
    conflicts = (
        duplicate_rows.groupby("order_id")[column]
        .nunique(dropna=False)
    )
    conflicting_ids.extend(conflicts[conflicts > 1].index.tolist())

if conflicting_ids:
    raise ValueError(
        "Conflicting duplicate orders found. "
        "Inspect these IDs before removing duplicates: "
        + str(set(conflicting_ids))
    )

orders = orders.drop_duplicates(
    subset=["order_id"],
    keep="first"
)

print("Orders after cleaning:", orders.shape)

# ==========================================
# 4. CLEAN CUSTOMER STATES
# ==========================================

customers["state"] = (
    customers["state"]
    .fillna("UNKNOWN")
    .str.strip()
    .str.upper()
)

print("\nSTATE VALUES AFTER CLEANING")
print(customers["state"].value_counts())

# ==========================================
# 5. CONVERT DATE COLUMNS
# ==========================================

customers["signup_date"] = pd.to_datetime(
    customers["signup_date"],
    format="%Y-%m-%d",
    errors="coerce"
)

orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    format="%d-%m-%Y",
    errors="coerce"
)

orders["delivery_date"] = pd.to_datetime(
    orders["delivery_date"],
    format="%d-%m-%Y",
    errors="coerce"
)

print("\nDATE CONVERSION COMPLETED")

# ==========================================
# 6. HANDLE MISSING DISCOUNTS
# ==========================================

overall_median = order_items["discount_pct"].median()

product_medians = (
    order_items.groupby("product_id")["discount_pct"]
    .transform("median")
)

order_items["discount_pct"] = (
    order_items["discount_pct"]
    .fillna(product_medians)
    .fillna(overall_median)
)

print("\nDISCOUNT CLEANING COMPLETED")
print("Overall median:", overall_median)
print(
    "Remaining missing discounts:",
    order_items["discount_pct"].isnull().sum()
)

# ==========================================
# 7. CALCULATE REVENUE
# ==========================================

order_items["revenue"] = (
    order_items["quantity"]
    * order_items["unit_price"]
    * (1 - order_items["discount_pct"] / 100)
)

print("\nREVENUE COLUMN CREATED")

# ==========================================
# 8. CALCULATE DELIVERY DAYS
# ==========================================

orders["delivery_days"] = (
    orders["delivery_date"] - orders["order_date"]
).dt.days

print("\nDELIVERY DAYS COLUMN CREATED")

# ==========================================
# 9. CREATE CLEANED DATA FOLDER
# ==========================================

os.makedirs("cleaned_data", exist_ok=True)

# ==========================================
# 10. EXPORT CLEANED DATASETS
# ==========================================

customers.to_csv(
    "cleaned_data/cleaned_customers.csv",
    index=False
)

products.to_csv(
    "cleaned_data/cleaned_products.csv",
    index=False
)

orders.to_csv(
    "cleaned_data/cleaned_orders.csv",
    index=False
)

order_items.to_csv(
    "cleaned_data/cleaned_order_items.csv",
    index=False
)

print("\nALL CLEANED DATASETS EXPORTED SUCCESSFULLY!")

# ==========================================
# 11. FINAL DATA QUALITY REPORT
# ==========================================

final_datasets = {
    "Customers": customers,
    "Products": products,
    "Orders": orders,
    "Order Items": order_items
}

print("\n========== FINAL DATA QUALITY REPORT ==========")

for name, df in final_datasets.items():

    print("\n", name)
    print("Shape:", df.shape)
    print("\nData Types:")
    print(df.dtypes)
    print("\nMissing Values:")
    print(df.isnull().sum())

print("\nDATA CLEANING COMPLETED SUCCESSFULLY!")
