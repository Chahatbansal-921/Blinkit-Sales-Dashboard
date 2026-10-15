import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(
    page_title="Blinkit Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)
@st.cache_data
def load_data():
    df = pd.read_excel("blinkit_data_10000.xlsx")
    return df

df = load_data()
st.title("🛒 Blinkit Sales Dashboard")
st.markdown("### Interactive Sales Analysis")

st.markdown("---")
st.sidebar.header("Filters")

selected_outlet = st.sidebar.multiselect(
    "Outlet Type",
    options=df["Outlet_Type"].unique(),
    default=df["Outlet_Type"].unique()
)

selected_location = st.sidebar.multiselect(
    "Location Tier",
    options=df["Outlet_Location_Type"].unique(),
    default=df["Outlet_Location_Type"].unique()
)

selected_fat = st.sidebar.multiselect(
    "Fat Content",
    options=df["Item_Fat_Content"].unique(),
    default=df["Item_Fat_Content"].unique()
)

filtered_df = df[
    (df["Outlet_Type"].isin(selected_outlet)) &
    (df["Outlet_Location_Type"].isin(selected_location)) &
    (df["Item_Fat_Content"].isin(selected_fat))
]

total_sales = filtered_df["Item_Outlet_Sales"].sum()
avg_sales = filtered_df["Item_Outlet_Sales"].mean()
total_items = filtered_df["Item_Identifier"].nunique()
avg_price = filtered_df["Item_MRP"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
col2.metric("📦 Total Items", total_items)
col3.metric("📈 Average Sales", f"₹{avg_sales:,.2f}")
col4.metric("🏷 Average MRP", f"₹{avg_price:,.2f}")

st.markdown("---")

sales_item = (
    filtered_df.groupby("Item_Type")["Item_Outlet_Sales"]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    sales_item,
    x="Item_Type",
    y="Item_Outlet_Sales",
    color="Item_Outlet_Sales",
    title="Sales by Item Type"
)

st.plotly_chart(fig1, use_container_width=True)

sales_outlet = (
    filtered_df.groupby("Outlet_Type")["Item_Outlet_Sales"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    sales_outlet,
    names="Outlet_Type",
    values="Item_Outlet_Sales",
    title="Sales by Outlet Type"
)

st.plotly_chart(fig2, use_container_width=True)

location_sales = (
    filtered_df.groupby("Outlet_Location_Type")["Item_Outlet_Sales"]
    .sum()
    .reset_index()
)

fig3 = px.bar(
    location_sales,
    x="Outlet_Location_Type",
    y="Item_Outlet_Sales",
    color="Outlet_Location_Type",
    title="Sales by Location Tier"
)

st.plotly_chart(fig3, use_container_width=True)

fat = (
    filtered_df.groupby("Item_Fat_Content")["Item_Outlet_Sales"]
    .sum()
    .reset_index()
)

fig4 = px.pie(
    fat,
    names="Item_Fat_Content",
    values="Item_Outlet_Sales",
    title="Sales by Fat Content"
)

st.plotly_chart(fig4, use_container_width=True)

top = (
    filtered_df.groupby("Item_Identifier")["Item_Outlet_Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig5 = px.bar(
    top,
    x="Item_Identifier",
    y="Item_Outlet_Sales",
    color="Item_Outlet_Sales",
    title="Top 10 Selling Products"
)

st.plotly_chart(fig5, use_container_width=True)

size = (
    filtered_df.groupby("Outlet_Size")["Item_Outlet_Sales"]
    .sum()
    .reset_index()
)

fig6 = px.bar(
    size,
    x="Outlet_Size",
    y="Item_Outlet_Sales",
    color="Outlet_Size",
    title="Sales by Outlet Size"
)

st.plotly_chart(fig6, use_container_width=True)

st.subheader("Dataset")

st.dataframe(filtered_df)

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Filtered Data",
    csv,
    "Blinkit_Filtered_Data.csv",
    "text/csv"
)