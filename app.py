import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Sales & Revenue Dashboard")

# Auto-create sample data
np.random.seed(42)
n = 1000
regions = ['East', 'West', 'North', 'South']
categories = ['Furniture', 'Technology', 'Office Supplies']
years = [2021, 2022, 2023, 2024]

df = pd.DataFrame({
    'Order ID': [f'ORD-{i:04d}' for i in range(n)],
    'Order Date': pd.date_range('2021-01-01', periods=n, freq='D')[:n],
    'Region': np.random.choice(regions, n),
    'Category': np.random.choice(categories, n),
    'Sales': np.random.uniform(100, 5000, n).round(2),
    'Profit': np.random.uniform(10, 1000, n).round(2),
    'Quantity': np.random.randint(1, 10, n)
})

df['Year'] = df['Order Date'].dt.year

total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_orders = df['Order ID'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("🛒 Total Orders", f"{total_orders:,}")

st.subheader("📅 Sales by Year")
yearly = df.groupby('Year')['Sales'].sum().reset_index()
fig1 = px.bar(yearly, x='Year', y='Sales', color='Sales', title="Yearly Sales")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🌍 Sales by Region")
region = df.groupby('Region')['Sales'].sum().reset_index()
fig2 = px.pie(region, names='Region', values='Sales', title="Sales by Region")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("📦 Sales by Category")
category = df.groupby('Category')['Sales'].sum().reset_index()
fig3 = px.bar(category, x='Category', y='Sales', color='Category', title="Category Sales")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("🔍 Raw Data")
st.dataframe(df.head(100))