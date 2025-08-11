import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_excel("Onafriq Agents info Sept - feb 25_pp.xlsx", sheet_name="Data")

month_cols = ['September value', 'October value', 'November value', 'December value',
              'January value', 'February value']

month_order = {
    'September value': 'Sep', 'October value': 'Oct', 'November value': 'Nov', 'December value': 'Dec',
    'January value': 'Jan', 'February value': 'Feb'
}

# Melt for trend analysis
df_melt = df.melt(id_vars=['UserName', 'Gender', 'Region'],
                  value_vars=month_cols,
                  var_name='Month', value_name='Transactions')
df_melt['Month'] = df_melt['Month'].map(month_order)
df_melt['Month'] = pd.Categorical(df_melt['Month'],
                                  categories=['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb'],
                                  ordered=True)

# =========================
# Streamlit App
# =========================



st.set_page_config(page_title="Field Officer Dashboard", layout="wide")

st.title("📊 Field Officer Data Dashboard")

# Filters
col1, col2 = st.columns([1, 2])
with col1:
    selected_genders = st.multiselect("Filter by Gender:", options=df['Gender'].unique())
with col2:
    selected_regions = st.multiselect("Filter by Region:", options=df['Region'].unique())

# Apply filters
filtered_df = df.copy()
filtered_trend = df_melt.copy()

if selected_genders:
    filtered_df = filtered_df[filtered_df['Gender'].isin(selected_genders)]
    filtered_trend = filtered_trend[filtered_trend['Gender'].isin(selected_genders)]

if selected_regions:
    filtered_df = filtered_df[filtered_df['Region'].isin(selected_regions)]
    filtered_trend = filtered_trend[filtered_trend['Region'].isin(selected_regions)]


 # =========================
# Heatmap
# =========================
st.subheader("Heatmap: Agent Productivity by Location")
heatmap_fig = px.density_heatmap(
    filtered_df, x='Sim_Longitude', y='Sim_Latitude',
    z='Average Productivity', nbinsx=20, nbinsy=20,
    color_continuous_scale='Viridis',
    title="Agent Productivity by Location"
)
st.plotly_chart(heatmap_fig, use_container_width=True)

# =========================
# KPIs
# =========================
kpi_col1, kpi_col2 = st.columns(2)

with kpi_col1:
    st.subheader("Active vs Dormant Agents")
    active_counts = filtered_df['Active'].value_counts().reset_index()
    active_counts.columns = ['Active Status', 'Count']
    active_fig = px.pie(active_counts, names='Active Status', values='Count')
    st.plotly_chart(active_fig, use_container_width=True)

with kpi_col2:
    st.subheader("Gender Ratio")
    gender_counts = filtered_df['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    gender_fig = px.pie(gender_counts, names='Gender', values='Count')
    st.plotly_chart(gender_fig, use_container_width=True)


  # =========================
# Average Transactions Table
# =========================
st.subheader("Average Transactions by Month")
avg_transactions = filtered_df[month_cols].mean().reset_index()
avg_transactions.columns = ['Month', 'Avg Transactions']
avg_transactions['Month'] = avg_transactions['Month'].map(month_order)
avg_transactions = avg_transactions.sort_values(
    'Month', key=lambda x: pd.Categorical(x, categories=['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb'], ordered=True)
)
avg_fig = px.bar(avg_transactions, x='Month', y='Avg Transactions', text_auto='.2s')
st.plotly_chart(avg_fig, use_container_width=True)
     

# =========================
# Trend Analysis
# =========================
st.subheader("Monthly Productivity Trend by Region")
trend_fig = px.line(
    filtered_trend.groupby(['Month', 'Region'], as_index=False)['Transactions'].mean(),
    x='Month', y='Transactions', color='Region'
)
st.plotly_chart(trend_fig, use_container_width=True)




