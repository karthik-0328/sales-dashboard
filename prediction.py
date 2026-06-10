import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Predictive Analytics", layout="wide")
st.title("🔮 Predictive Analytics Dashboard")

np.random.seed(42)
months = pd.date_range('2021-01-01', periods=48, freq='ME')
sales = np.random.randint(30000, 80000, 48) + np.linspace(0, 20000, 48)

df = pd.DataFrame({
    'Month': months,
    'Sales': sales.round(2)
})
df['Month_Num'] = range(1, len(df) + 1)

X = df[['Month_Num']]
y = df['Sales']
model = LinearRegression()
model.fit(X, y)

future_months = pd.date_range(df['Month'].iloc[-1], periods=7, freq='ME')[1:]
future_num = range(len(df) + 1, len(df) + 7)
future_sales = model.predict([[m] for m in future_num])

future_df = pd.DataFrame({
    'Month': future_months,
    'Sales': future_sales.round(2),
    'Type': 'Predicted'
})
df['Type'] = 'Actual'

combined = pd.concat([df[['Month', 'Sales', 'Type']], future_df])

total_months = len(df)
avg_sales = df['Sales'].mean()
accuracy = model.score(X, y) * 100

col1, col2, col3 = st.columns(3)
col1.metric("📊 Total Months", total_months)
col2.metric("💰 Avg Monthly Sales", f"${avg_sales:,.0f}")
col3.metric("🎯 Model Accuracy", f"{accuracy:.1f}%")

st.subheader("📈 Sales Forecast — Next 6 Months")
fig1 = px.line(combined, x='Month', y='Sales', color='Type',
               title="Actual vs Predicted Sales",
               color_discrete_map={'Actual': '#00CC96', 'Predicted': '#EF553B'})
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📊 Monthly Sales Bar Chart")
fig2 = px.bar(df, x='Month', y='Sales', title="Monthly Sales History", color='Sales')
st.plotly_chart(fig2, use_container_width=True)

st.subheader("🔮 Predicted Sales — Next 6 Months")
st.dataframe(future_df[['Month', 'Sales']].reset_index(drop=True))

st.subheader("🔍 Raw Data")
st.dataframe(df[['Month', 'Sales']].head(48))