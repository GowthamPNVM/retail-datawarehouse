import pandas as pd
from datetime import datetime, timedelta

#Create a fact table for sales data
def create_fact_sales(sales_data, product_data, customer_data, date_dim):
    print("Creating fact table for sales data...")
    print("Merging sales data with product, customer and date dimensions...")
    product_data['product_id'] = product_data['product_id'].astype(int)
    product_data['product_key'] = product_data['product_key'].astype(int)
    customer_data['customer_key'] = customer_data['customer_key'].astype(int)
    customer_data['customer_id'] = customer_data['customer_id'].astype(int)
    # Merge sales data with product, customer and date dimensions
    sales_data = pd.merge(sales_data, product_data[['product_id', 'product_key']], on='product_id', how='left')
    sales_data = pd.merge(sales_data, customer_data[['customer_id', 'customer_key']], on='customer_id', how='left')
    #sales_data = pd.merge(sales_data, date_dim[['full_date', 'date_key']], left_on='sale_date', right_on='full_date', how='left'
    print(f"Sales data shape: {sales_data['sale_date'].dtype}")
    sales_data['sale_date'] = pd.to_datetime(sales_data['sale_date'], format='%d-%m-%Y').dt.strftime('%Y-%m-%d')

    sales_data['sale_date'] = pd.to_datetime(sales_data['sale_date'], format="%Y-%m-%d")
    formatted_date = sales_data['sale_date'].dt.strftime("%Y%m%d")
    sales_data['date_key'] = formatted_date.astype(int)
    print(f"Sales data shape after merging with dimensions: {sales_data.shape}")
    # Select relevant columns for fact table
    fact_sales = sales_data[['customer_key','product_key', 'date_key', 'sale_amount', 'quantity']]
    
    print("Fact table for sales data created successfully.")
    return fact_sales
    