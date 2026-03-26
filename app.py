import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_excel("Afficionado Coffee Roasters.xlsx")

# Revenue column
df["revenue"] = df["transaction_qty"] * df["unit_price"]

st.title("Coffee Product Analysis Dashboard")

# Sidebar filters
category = st.sidebar.selectbox("Select Category", df["product_category"].unique())

filtered_df = df[df["product_category"] == category]

# -------------------
# Top Products
# -------------------
top_products = filtered_df.groupby("product_detail")["revenue"].sum().sort_values(ascending=False).head(10)

st.subheader("Top 10 Products by Revenue")
st.bar_chart(top_products)

# -------------------
# Sales Volume
# -------------------
sales = filtered_df.groupby("product_detail")["transaction_qty"].sum().sort_values(ascending=False).head(10)

st.subheader("Top 10 Products by Sales")
st.bar_chart(sales)

# -------------------
# Category Distribution
# -------------------
category_rev = df.groupby("product_category")["revenue"].sum()

st.subheader("Category Revenue Distribution")
st.bar_chart(category_rev)

# -------------------
# Scatter Plot
# -------------------
st.subheader("Popularity vs Revenue")

scatter = df.groupby("product_detail").agg({
    "transaction_qty": "sum",
    "revenue": "sum"
})

fig, ax = plt.subplots()
ax.scatter(scatter["transaction_qty"], scatter["revenue"])
ax.set_xlabel("Sales Volume")
ax.set_ylabel("Revenue")

st.pyplot(fig)
