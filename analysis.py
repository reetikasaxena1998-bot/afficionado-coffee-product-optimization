import pandas as pd

# -----------------------
# Load Data
# -----------------------
df = pd.read_excel("data.xlsx", engine="openpyxl")

# -----------------------
# Data Cleaning
# -----------------------
df = df.dropna()

# -----------------------
# Revenue Calculation
# -----------------------
df["revenue"] = df["transaction_qty"] * df["unit_price"]

# -----------------------
# Product Popularity (Sales)
# -----------------------
product_sales = (
    df.groupby("product_detail")["transaction_qty"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 5 Products by Sales:")
print(product_sales.head())

print("\nBottom 5 Products by Sales:")
print(product_sales.tail())

# -----------------------
# Revenue by Product
# -----------------------
product_revenue = (
    df.groupby("product_detail")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 5 Products by Revenue:")
print(product_revenue.head())

print("\nBottom 5 Products by Revenue:")
print(product_revenue.tail())

# -----------------------
# Category Revenue
# -----------------------
category_revenue = df.groupby("product_category")["revenue"].sum()

print("\nCategory Revenue:")
print(category_revenue)

# -----------------------
# Revenue Contribution %
# -----------------------
total_revenue = df["revenue"].sum()

product_contribution = (product_revenue / total_revenue) * 100

print("\nTop 5 Revenue Contribution (%):")
print(product_contribution.head())

# -----------------------
# Product Efficiency
# -----------------------
efficiency = product_revenue / df["product_detail"].nunique()

print("\nProduct Efficiency Score:")
print(efficiency.head())

# -----------------------
# Pareto Analysis (80/20)
# -----------------------
pareto = product_revenue.cumsum() / total_revenue

print("\nPareto (Cumulative Revenue %):")
print(pareto.head(10))

# -----------------------
# Save Results (optional)
# -----------------------
product_revenue.to_csv("product_revenue.csv")
product_sales.to_csv("product_sales.csv")
category_revenue.to_csv("category_revenue.csv")
