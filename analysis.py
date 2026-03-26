import pandas as pd

# Load data
df = pd.read_excel("Afficionado Coffee Roasters.xlsx")

# Basic cleaning
df = df.dropna()

# Create revenue column
df["revenue"] = df["transaction_qty"] * df["unit_price"]

# -------------------------------
# Product Popularity
# -------------------------------
product_sales = df.groupby("product_detail")["transaction_qty"].sum().sort_values(ascending=False)

# -------------------------------
# Revenue by Product
# -------------------------------
product_revenue = df.groupby("product_detail")["revenue"].sum().sort_values(ascending=False)

# -------------------------------
# Category Revenue
# -------------------------------
category_revenue = df.groupby("product_category")["revenue"].sum()

# -------------------------------
# Revenue Contribution %
# -------------------------------
total_revenue = df["revenue"].sum()
product_revenue_percent = (product_revenue / total_revenue) * 100

# -------------------------------
# Pareto (Top 80%)
# -------------------------------
pareto = product_revenue.cumsum() / total_revenue

print("Top Products by Sales:\n", product_sales.head())
print("\nTop Products by Revenue:\n", product_revenue.head())
print("\nCategory Revenue:\n", category_revenue)
