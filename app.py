import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Load Data
# -------------------------------
df = pd.read_excel("Afficionado Coffee Roasters.xlsx", engine="openpyxl")

# Create revenue column
df["revenue"] = df["transaction_qty"] * df["unit_price"]

# -------------------------------
# Title
# -------------------------------
st.title("☕ Coffee Product Optimization Dashboard")

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("Filters")

category = st.sidebar.selectbox(
    "Select Category",
    options=df["product_category"].unique()
)

store = st.sidebar.selectbox(
    "Select Store Location",
    options=df["store_location"].unique()
)

top_n = st.sidebar.slider("Top N Products", 5, 20, 10)

# Apply filters
filtered_df = df[
    (df["product_category"] == category) &
    (df["store_location"] == store)
]

# -------------------------------
# KPI Section
# -------------------------------
total_revenue = filtered_df["revenue"].sum()
total_sales = filtered_df["transaction_qty"].sum()

st.subheader("Key Metrics")
st.write("Total Revenue:", round(total_revenue, 2))
st.write("Total Sales Volume:", int(total_sales))

# -------------------------------
# Top Products by Revenue
# -------------------------------
st.subheader("Top Products by Revenue")

top_products = (
    filtered_df.groupby("product_detail")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(top_n)
)

st.bar_chart(top_products)

# -------------------------------
# Top Products by Sales
# -------------------------------
st.subheader("Top Products by Sales Volume")

top_sales = (
    filtered_df.groupby("product_detail")["transaction_qty"]
    .sum()
    .sort_values(ascending=False)
    .head(top_n)
)

st.bar_chart(top_sales)

# -------------------------------
# Category Revenue Distribution
# -------------------------------
st.subheader("Category Revenue Distribution")

category_rev = df.groupby("product_category")["revenue"].sum()

st.bar_chart(category_rev)

# -------------------------------
# Scatter Plot (Popularity vs Revenue)
# -------------------------------
st.subheader("Popularity vs Revenue")

scatter_data = df.groupby("product_detail").agg({
    "transaction_qty": "sum",
    "revenue": "sum"
})

fig, ax = plt.subplots()
ax.scatter(scatter_data["transaction_qty"], scatter_data["revenue"])
ax.set_xlabel("Sales Volume")
ax.set_ylabel("Revenue")

st.pyplot(fig)

# -------------------------------
# Pareto Analysis
# -------------------------------
st.subheader("Pareto Analysis (Top Revenue Contributors)")

pareto = (
    df.groupby("product_detail")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

pareto_cum = pareto.cumsum() / pareto.sum()

st.line_chart(pareto_cum)

# -------------------------------
# Raw Data View
# -------------------------------
if st.checkbox("Show Raw Data"):
    st.write(filtered_df)
