# Matthew Hodgens - October 5th, 2026
# Data App Assignment

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, due on Oct 6th.")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('ME')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='ME')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.header("Data App Assignment Additions")

# drop down for Category
category_user_selection = st.selectbox("Select a Category", df["Category"].unique(), index=None)

# multi-select for Sub-Category in the selected Category
sub_category_user_selection = st.multiselect("Select Sub-Category", df[df["Category"] == category_user_selection]["Sub_Category"].unique())

# show a line chart of sales for each selected sub-categories
st.line_chart(df[df["Sub_Category"].isin(sub_category_user_selection)].groupby(pd.Grouper(freq='ME')).sum(), y="Sales")

# show 3 metrics: total sales, total profit, and overall profit margin (%)
total_sales = df[df["Sub_Category"].isin(sub_category_user_selection)]["Sales"].sum()
total_profit = df[df["Sub_Category"].isin(sub_category_user_selection)]["Profit"].sum()
overall_profit_margin = (total_profit / total_sales) * 100
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")

# calculate the overall average profit margin (all products across all categories)
overall_average_profit_margin = (df["Profit"].sum() / df["Sales"].sum()) * 100
col3.metric("Overall Profit Margin", f"{overall_profit_margin:.2f}%", delta=f"{overall_profit_margin - overall_average_profit_margin:.2f}%")