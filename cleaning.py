import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

st.set_page_config(page_title="Data Cleaning Dashboard", layout="wide")
st.title("🧹 Data Cleaning & Reporting Dashboard")

st.write("This dashboard cleans messy data automatically.")

# Create sample messy data
np.random.seed(42)
n = 200
df = pd.DataFrame({
    'Name': [f'Customer {i}' for i in range(n)],
    'Age': np.random.choice([25, 30, np.nan, 45, 50, -5, 200], n),
    'Sales': np.random.choice([1000, 2000, np.nan, 3000, -100], n),
    'Region': np.random.choice(['East', 'West', 'North', 'south', 'EAST'], n)
})

st.subheader("Original Data")
st.write(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")
st.dataframe(df.head(20))

missing = df.isnull().sum()
duplicates = df.duplicated().sum()

col1, col2, col3 = st.columns(3)
col1.metric("Missing Values", int(missing.sum()))
col2.metric("Duplicate Rows", int(duplicates))
col3.metric("Total Rows", df.shape[0])

cleaned_df = df.drop_duplicates()

for col in cleaned_df.select_dtypes(include=[np.number]).columns:
    median_val = cleaned_df[col].median()
    cleaned_df[col] = cleaned_df[col].fillna(median_val)
    cleaned_df[col] = cleaned_df[col].clip(lower=0)

cleaned_df['Region'] = cleaned_df['Region'].str.strip().str.title()

st.subheader("Cleaned Data")
st.write(f"Rows: {cleaned_df.shape[0]} | Columns: {cleaned_df.shape[1]}")
st.dataframe(cleaned_df.head(20))

st.subheader("Download Cleaned Data")

csv = cleaned_df.to_csv(index=False).encode('utf-8')
st.download_button("Download as CSV", csv, "cleaned_data.csv", "text/csv")

output = BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    cleaned_df.to_excel(writer, index=False, sheet_name='Cleaned Data')
excel_data = output.getvalue()

st.download_button("Download as Excel", excel_data, "cleaned_data.xlsx",
                   "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")