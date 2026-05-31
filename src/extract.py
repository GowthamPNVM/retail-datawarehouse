import pandas as pd
from datetime import datetime, timedelta
import logging
from utils import setup_logger

logger = setup_logger()

# Function to extract data from csv files
def extract_data_from_csv(file_path,columns=None):
    try:
        data = pd.read_csv(file_path)
        if columns:
            data = data[columns]            
        logger.info(f"Data extracted successfully from {file_path}.")
        return data
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Error extracting data from {file_path}: {e}")
        return None
    
# Function to extract data from database tables
def extract_data_from_table(connection, table_name):
    try:
        connection.ping(reconnect=True)
        query = f"SELECT * FROM {table_name}"
        data = pd.read_sql(query, connection)
        logger.info("Data extracted successfully from database.")
        return data
    except Exception as e:
        logger.error(f"Error extracting data from database: {e}")
        return None
