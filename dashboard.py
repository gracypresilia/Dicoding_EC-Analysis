import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from babel.numbers import format_currency
from babel.numbers import format_decimal
import seaborn as sns
import streamlit as st
import numpy as np

sns.set(style='whitegrid')

# Function for Company's Sales and Revenues Variable
def create_vis_order(df):
    # Resampling The Data
    vis_order = df.resample(rule='M', on='order_delivered_customer_date').agg({
        "order_id": "nunique",
        "payment_value": "sum"
    })
    # Indexing and Renaming Data
    vis_order.index = vis_order.index.strftime('%Y-%m')
    vis_order = vis_order.reset_index()
    vis_order.rename(columns={
        "order_delivered_customer_date": "order_date",
        "order_id": "order_count",
        "payment_value": "revenue"
    }, inplace=True)

    return vis_order

# Function for Geographic Spread of Customers Variable
def create_topCustCities(df):
    # Grouping The Data
    vis_cust = df.groupby(by="customer_city").customer_id.nunique().reset_index()
    vis_cust.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    # Categorizing Data
    # Insert the top 9 data with the highest count into the 'top_cities' variable
    top_cities = vis_cust.sort_values(by="customer_count", ascending=False).head(9)
    # Insert the remaining data into the 'others_cities' variable
    others_cities = vis_cust.sort_values(by="customer_count", ascending=False).iloc[9:]["customer_count"].sum()
    # Create the 'others_cities' variable in a data frame format
    others_df = pd.DataFrame({
        "customer_city": ["Others"],
        "customer_count": [others_cities]
    })
    # Combine the 'top_cities' and 'others_cities' DataFrames to present them together in the next stage
    top_cities = pd.concat([top_cities, others_df], ignore_index=True)

    return top_cities

# Function for Relationship of Customer and Seller Locations Variable
def create_vis_loc(df):
    # Grouping The Data
    vis_loc = df.groupby(by='customer_city').agg({
        "customer_id": "nunique",
        "seller_city": "nunique"
    })
    # Indexing and Renaming Data
    vis_loc.nunique().reset_index()
    vis_loc.rename(columns={
        # Number of customers from a particular city
        "customer_id": "customer_count",    
        # Number of seller locations that have transacted with customers from a particular city
        "seller_city": "city_of_sellers"    
    }, inplace=True)

    return vis_loc

# Reading Cleaned Dataset
main_data = pd.read_csv("./main_data.csv")

# Correcting Inappropriate Data Types
datetime_columns = ["order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]
main_data.sort_values(by="order_delivered_customer_date", inplace=True)
main_data.reset_index(inplace=True)
for column in datetime_columns:
    main_data[column] = pd.to_datetime(main_data[column].astype(str), errors='coerce')

# Creating Data Frames
vis_order_df = create_vis_order(main_data)
vis_topCustCities_df = create_topCustCities(main_data)
vis_loc_df = create_vis_loc(main_data)

# Streamlit Header
st.header(":book: E-commerce Dataset Analysis :book:")

# Streamlit Subheader: Company's Sales and Revenue
st.subheader(":coin: Orders Data (Oktober 2016 - Oktober 2018)")
# Status Columns
col1, col2 = st.columns(2)
with col1:
    total_orders = format_decimal(vis_order_df.order_count.sum(), locale="es_US")
    st.metric("Total Orders Delivered :package:", value=total_orders)
with col2:
    total_revenue = format_currency(vis_order_df.revenue.sum(), "R$", locale="es_US") 
    st.metric("Total Revenues Received :moneybag:", value=total_revenue)
# Company's Sales Plot
fig, ax = plt.subplots(figsize=(16, 8))
# Find highest and lowest values for sales
highest_sales = vis_order_df["order_count"].max()
lowest_sales = vis_order_df["order_count"].min()
highest_sales_date = vis_order_df[vis_order_df["order_count"] == highest_sales]["order_date"].values[0]
lowest_sales_date = vis_order_df[vis_order_df["order_count"] == lowest_sales]["order_date"].values[0]
# Plotting the data
ax.plot(
    vis_order_df["order_date"],
    vis_order_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#72BCD4"
)
ax.set_title("Number of Orders per Month (October 2016-October 2018)", loc="center", fontsize=30, pad=15)
ax.set_xlabel("Year-Month", fontsize=20, labelpad=10)
ax.set_ylabel("Number of Order", fontsize=20, labelpad=10)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', rotation=45, labelsize=15)
# Adjust y-axis to have a bit of space around the data
ax.set_ylim(vis_order_df["order_count"].min() - 1000, vis_order_df["order_count"].max() + 1000)
# Highlight the highest and lowest point
ax.scatter(highest_sales_date, highest_sales, color="#4A8F5F", zorder=5)
ax.annotate(f"Highest: {highest_sales}", (highest_sales_date, highest_sales), 
             textcoords="offset points", xytext=(0, 10), ha="center", fontsize=15, color="green")
ax.scatter(lowest_sales_date, lowest_sales, color="red", zorder=5)
ax.annotate(f"Lowest: {lowest_sales}", (lowest_sales_date, lowest_sales), 
             textcoords="offset points", xytext=(0, -20), ha="center", fontsize=15, color="#B03A2F")
st.pyplot(fig)
# Company's Revenues Plot
fig, ax = plt.subplots(figsize=(16, 8))
# Find highest and lowest values for revenues
highest_revenues = vis_order_df["revenue"].max()
lowest_revenues = vis_order_df["revenue"].min()
highest_revenues_date = vis_order_df[vis_order_df["revenue"] == highest_revenues]["order_date"].values[0]
lowest_revenues_date = vis_order_df[vis_order_df["revenue"] == lowest_revenues]["order_date"].values[0]
# Plotting the data
ax.plot(
    vis_order_df["order_date"],
    vis_order_df["revenue"],
    marker='o', 
    linewidth=2,
    color="#72BCD4"
)
ax.set_title("Revenues per Month (October 2016-October 2018)", loc="center", fontsize=30, pad=15)
ax.set_xlabel("Year-Month", fontsize=20, labelpad=10)
ax.set_ylabel("Revenue", fontsize=20, labelpad=10)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', rotation=45, labelsize=15)
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.2f}'))
# Adjust y-axis to have a bit of space around the data
ax.set_ylim(vis_order_df["revenue"].min() - 170000, vis_order_df["revenue"].max() + 170000)
# Highlight the highest and lowest point
plt.scatter(highest_revenues_date, highest_revenues, color="#4A8F5F", zorder=5)
plt.annotate(f"Highest: {highest_revenues:.2f}", (highest_revenues_date, highest_revenues), 
             textcoords="offset points", xytext=(0, 10), ha="center", fontsize=15, color="green")
plt.scatter(lowest_revenues_date, lowest_revenues, color="red", zorder=5)
plt.annotate(f"Lowest: {lowest_revenues:.2f}", (lowest_revenues_date, lowest_revenues), 
             textcoords="offset points", xytext=(0, -22), ha="right", fontsize=15, color="#B03A2F")
st.pyplot(fig)
# Explanation
st.write("The company's sales and revenue performance shows a tending upward trend month to month, indicating improved performance and increasing customer trust.")

# Streamlit Subheader: Geographic Spread of Customers
st.subheader(":man-woman-girl-boy: Customer Demographics")
# Status Columns
col1, col2 = st.columns(2)
with col1:
    total_customers = format_decimal(vis_topCustCities_df.customer_count.sum(), locale="en_US")
    st.metric("Total Customers :male-technologist:", value=total_customers)
with col2:
    total_custCity = format_decimal(main_data.customer_city.nunique(), locale="en_US")
    st.metric("Total Locations :world_map:", value=total_custCity)
# Geographic Spread of Customers Plot
fig, ax = plt.subplots(figsize=(16, 8))
# Plotting the data
ax.set_title("Number of Customers by City (Top 9 and Others)", loc="center", fontsize=30, pad=15)
ax.set_ylabel("City", fontsize=20, labelpad=10)
ax.set_xlabel("Number of Customer", fontsize=20, labelpad=10)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=15)
# Adjust x-axis to have a bit of space around the data
ax.set_xlim(0,vis_topCustCities_df["customer_count"].max() + 6000)
vis_custCity = sns.barplot(
    x="customer_count", 
    y="customer_city",
    data=vis_topCustCities_df,
    color='#A0D3E4'
)
# Highlight the top first city
vis_custCity.patches[0].set_facecolor('#5A9BB2')
# Annotate the bars with customer count values
for index, value in enumerate(vis_topCustCities_df["customer_count"]):
    vis_custCity.text(value + 500, index, f'{value}', va='center', 
                      # Apply bold only for the top first city (index 0)
                      fontweight='bold' if index == 0 else 'normal')
ax.get_yticklabels()[0].set_fontweight('bold')
st.pyplot(fig)
# Explanation
st.write("The company's customers are distributed across 4,110 cities, with an average of 24 customers per city. Sao Paulo has the highest number of customers, totaling 15,402.")

# Streamlit Subheader: Relationship of Customer and Seller Locations Variable
st.subheader(":handshake: Customer and Seller Demographics Correlation")
# Status COlumns
col1, col2 = st.columns(2)
with col1:
    total_customers = format_decimal(vis_loc_df.customer_count.sum(), locale="en_US")
    st.metric("Total Customers :male-technologist:", value=total_customers)
with col2:
    total_sellers = format_decimal(main_data.seller_id.nunique(), locale="en_US")
    st.metric("Total Sellers :money_with_wings:", value=total_sellers)
# Relationship of Customer and Seller Locations Plot
fig, ax = plt.subplots(figsize=(16, 8))
# Calculating the regression line
slope, intercept = np.polyfit(vis_loc_df["customer_count"], vis_loc_df["city_of_sellers"], 1)
regression_line = slope * vis_loc_df["customer_count"] + intercept
# PLotting the data
ax.set_title("Number of Customers by City VS Number of Seller Cities Involved", loc="center", fontsize=30, pad=15)
ax.set_ylabel("Number of Seller Cities", fontsize=20, labelpad=10)
ax.set_xlabel("Number of Customer", fontsize=20, labelpad=10)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=15)
sns.scatterplot(
    x="customer_count",
    y="city_of_sellers",
    data=vis_loc_df,
    color='#72BCD4'
) 
sns.lineplot(
    x=vis_loc_df["customer_count"], 
    y=regression_line, 
    color='#4A8F5F'
)
st.pyplot(fig)
# Explanation
st.write("The relationship between customer and seller locations shows a positive correlation: the higher the number of customers in a city, the more diverse the seller locations transacting with those customers.")