import pandas as pd
from datetime import datetime, timedelta
import logging
from utils import get_database_connection , setup_logger 
from extract import extract_data_from_csv, extract_data_from_table
from date_dimension import create_date_dimension
from dimension_loader import load_to_database
from fact_loader import create_fact_sales
logger = setup_logger()

# Main function to orchestrate the data warehouse pipeline
def main(): 
    try:
        logger.info("Warehouse pipeline started.")
        
        # Read connection details from config file
        connection = get_database_connection()
        
        # Create date dimension table
        start_date = '2024-01-01'
        end_date = '2030-12-31'
        date_dim = create_date_dimension(start_date, end_date)
        logger.info("Date dimension data created.")
        #print(date_dim.head())
        
        # Extract customer data from csv files
        customer_data = extract_data_from_csv("data/raw/customers.csv")
        customer_data = customer_data.rename(columns={"active_status": "current_flag"})
        customer_data = customer_data .drop(columns=['created_date','created_by','updated_date','updated_by'])
        #print(customer_data.head())
        logger.info("Customer data extracted from CSV file.")
        
        # Extract product data from csv files
        product_data = extract_data_from_csv("data/raw/products.csv")
        product_data = product_data .drop(columns=['added_date','added_by'])
        
        print(product_data.head())
        logger.info("Productdata extracted from CSV file.")
        
        # Load customer data to database
        if customer_data is not None:            
            load_to_database(customer_data, "dim_customer", connection)
            logger.info("Customer data loaded successfully.")
        else:
            logger.error("Customer data extraction failed. Skipping loading to database.")
        if product_data is not None:
            load_to_database(product_data, "dim_product", connection)
            logger.info("Product data loaded successfully.")
        else:
            logger.error("Product data extraction failed. Skipping loading to database.")
        if date_dim is not None:
            print(date_dim.head())
            load_to_database(date_dim, "dim_date", connection)
            logger.info("Date dimension data loaded successfully.")
        else:
            logger.error("Date dimension data creation failed. Skipping loading to database.")
        
        
        # Extract data from database tables (if needed)
        # For example, if you want to extract existing data from dim_customer table:
        existing_customer_data = extract_data_from_table(connection, "dim_customer")
        print(existing_customer_data.head())
        print(len(existing_customer_data))
        logger.info(f"Existing customer data extracted from database: {len(existing_customer_data)} rows.")
        
        # Extract data from database tables (if needed)
        # For example, if you want to extract existing data from dim_product table:
        existing_product_data = extract_data_from_table(connection, "dim_product")
        print(existing_product_data.head())
        print(len(existing_product_data))
        logger.info(f"Existing product data extracted from database: {len(existing_product_data)} rows.")
        
        # Extract data from database tables (if needed)
        # For example, if you want to extract existing data from dim_date table:
        existing_date_data = extract_data_from_table(connection, "dim_date")
        print(existing_date_data.head())
        print(len(existing_date_data))
        logger.info(f"Existing date data extracted from database: {len(existing_date_data)} rows.")
        
        

        #Extract sales data from csv files
        sales_data = extract_data_from_csv("data/raw/sales.csv")
        print(sales_data.head())
        logger.info("Sales data extracted from CSV file.")
                        
        # Create fact table for sales data
        fact_sales = create_fact_sales(sales_data, existing_product_data, existing_customer_data, existing_date_data)
        print(fact_sales.head())
        logger.info("Fact table for sales data created.")
        fact_sales = fact_sales.rename(columns={"sale_amount": "sales_amount"})
        # Load fact table to database
        if fact_sales is not None:
            load_to_database(fact_sales, "fact_sales", connection)
            logger.info("Fact sales data loaded successfully.")
        else:
            logger.error("Fact sales data creation failed. Skipping loading to database.")
        
        
    except Exception as e:
        logger.error(f"Error in warehouse pipeline: {e}")
    finally:
        logger.info("Warehouse pipeline completed.")
        
if __name__ == "__main__":
    main()