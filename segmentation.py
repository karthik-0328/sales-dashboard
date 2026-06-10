import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Customer Segmentation", layout="wide")
st.title("👥 Customer Segmentation Dashboard")

np.random.seed(42)
n = 500
df = pd.DataFrame({
    'CustomerID': [f'CUST-{i:04d}' for i in range(n)],
    'Age': np.random.randint(18, 70, n),
    'Annual Income (k$)': np.random.randint(15, 150, n),
    'Spending Score': np.random.randint(1, 100, n),
    'Purchase Frequency': np.random.randint(1, 50, n)
})

features = ['Age', 'Annual Income (k$)', 'Spending Score', 'Purchase Frequency']
scaler = StandardScaler()
scaled = scaler.fit_transform(df[features])

kmeans = KMeans(n_clusters=4, random_state=42)
df['Segment'] = kmeans.fit_predict(scaled)

segment_names = {0: '🔵 High Value', 1: '🟢 Regular', 2: '🟡 Low Activity', 3: '🔴 At Risk'}
df['Segment Name'] = df['Segment'].map(segment_names)

col1, col2, col3, col4 = st.columns(4)
col1.metric("🔵 High Value", len(df[df['Segment']==0]))
col2.metric("🟢 Regular", len(df[df['Segment']==1]))
col3.metric("🟡 Low Activity", len(df[df['Segment']==2]))
col4.metric("🔴 At Risk", len(df[df['Segment']==3]))

st.subheader("📊 Customer Segments Scatter Plot")
fig1 = px.scatter(df, x='Annual Income (k$)', y='Spending Score',
                  color='Segment Name', size='Purchase Frequency',
                  hover_data=['CustomerID', 'Age'],
                  title="Customer Segments by Income vs Spending")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🥧 Segment Distribution")
fig2 = px.pie(df, names='Segment Name', title="Customer Segment Distribution")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("📈 Age Distribution by Segment")
fig3 = px.histogram(df, x='Age', color='Segment Name', title="Age Distribution")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("🔍 Raw Data")
st.dataframe(df.head(100))