import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------
# Load Data
# -----------------------
df = pd.read_excel("data.xlsx", engine="openpyxl")

# Revenue column
df["revenue"] = df["transaction_qty"] * df["unit_price"]

# -----------------------
# Title
# -----------------------
st.title("Coffee Product Analysis Dashboard")

# -----------------------
# Sidebar Filters
# -----------------------
category = st.sidebar.selectbox(
    "Category",
    df["product_category"].unique()
)

store = st.sidebar.selectbox(
    "Store Location",
    df["store_location"].unique()
)

top_n = st.sidebar.slider("Top N Products", 5, 20, 10)

filtered_df = df[
    (df["product_category"] == category) &
    (df["store_location"] == store)
]

# -----------------------
# KPIs
# -----------------------
st.subheader("Key Metrics")
st.write("Total Revenue:", round(filtered_df["revenue"].sum(), 2))
st.write("Total Sales:", int(filtered_df["transaction_qty"].sum()))

# -----------------------
# Top Products (Revenue)
# -----------------------
st.subheader("Top Products by Revenue")

top_rev = (
    filtered_df.groupby("product_detail")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(top_n)
)

st.bar_chart(top_rev)

# -----------------------
# Top Products (Sales)
# -----------------------
st.subheader("Top Products by Sales")

top_sales = (
    filtered_df.groupby("product_detail")["transaction_qty"]
    .sum()
    .sort_values(ascending=False)
    .head(top_n)
)

st.bar_chart(top_sales)

# -----------------------
# Category Contribution
# -----------------------
st.subheader("Category Revenue Contribution")

cat_rev = df.groupby("product_category")["revenue"].sum()
st.bar_chart(cat_rev)

# -----------------------
# Scatter Plot
# -----------------------
st.subheader("Popularity vs Revenue")

scatter = df.groupby("product_detail").agg({
    "transaction_qty": "sum",
    "revenue": "sum"
})

fig, ax = plt.subplots()
ax.scatter(scatter["transaction_qty"], scatter["revenue"])
ax.set_xlabel("Sales")
ax.set_ylabel("Revenue")

st.pyplot(fig)

# -----------------------
# Pareto Analysis
# -----------------------
st.subheader("Pareto Analysis")

pareto = df.groupby("product_detail")["revenue"].sum().sort_values(ascending=False)
pareto_cum = pareto.cumsum() / pareto.sum()

st.line_chart(pareto_cum)
