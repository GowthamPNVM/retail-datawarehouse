import pandas as pd
from datetime import datetime, timedelta
import logging
from utils import setup_logger

logger = setup_logger()
"""
# Function to create generic loading function for fact and dimension tables
def load_to_database(df, table_name, connection):
    try:
        connection.ping(reconnect=True)
        cursor = connection.cursor()
        df['created_date'] = datetime.now()
        df['created_by'] = 'ADMIN'
        df['updated_date'] = datetime.now()
        df['updated_by'] = 'ADMIN'
        
        cols = ", ".join(df.columns)
        placeholders = ", ".join(["%s"] * len(df.columns))
        sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
        data = list(df.itertuples(index=False, name=None))
        cursor.executemany(sql, data)
        print(f"Data loaded successfully into {table_name} table.")
        logger.info(f"Data loaded successfully into {table_name} table.")
    except Exception as e:
        print(f"Error loading data into {table_name} table: {e}")
        logger.error(f"Error loading data into {table_name} table: {e}")
    finally:
        connection.commit()
        connection.close()
        logger.info(f"Database connection closed after loading {table_name} table.")
"""
def load_to_database(df, tableName, connection, batch_size=2000):    
    # 0. Health Check: Reconnect if the connection dropped before this table started
    if not connection.is_connected():
        connection.reconnect(attempts=3, delay=2)
        
    cursor = connection.cursor()
    
    try:    
        # Create a copy to prevent modifying the original DataFrame outside the function
        df_working = df.copy()

        # =====================================================================
        # NEW STEP: Handle Dimension Keys to Prevent Foreign Key Violations
        # =====================================================================
        # Automatically detect any column ending in '_key' (like customer_key, product_key)
        key_columns = [col for col in df_working.columns if col.lower().endswith('_key')]
        
        for col in key_columns:
            # Replace NaN with -1 (Standard DW placeholder for unknown keys)
            df_working[col] = df_working[col].fillna(-1)
            # Force to integer type so it doesn't send floats (like 457.0) to the DB
            df_working[col] = df_working[col].astype('int64')
        # =====================================================================

        # 1. Add Audit Columns
        df_working['created_date'] = datetime.now()
        df_working['created_by'] = 'ADMIN'
        df_working['updated_date'] = datetime.now()
        df_working['updated_by'] = 'ADMIN'
        
        # 2. Dynamic Query Generation
        columns = ",".join(df_working.columns)       
        placeholders = ",".join(["%s"] * len(df_working.columns))
        insertQry = f"INSERT INTO {tableName} ({columns}) VALUES ({placeholders})"
        logger.info(f"Generated insert query for {tableName}: {insertQry}")

        # 3. Data Preparation: Convert Remaining NaNs (like in sale_amount) to None
        df_clean = df_working.where(pd.notnull(df_working), None)
        logger.info(f"Data prepared for {tableName} with {df_clean.shape[0]} rows.")
        
        # 4. Convert to database-friendly tuples
        data = list(df_clean.itertuples(index=False, name=None))
        
        # 5. Chunked Batch Insertion to prevent Error 10054
        total_rows = len(data)
        logger.info(f"Starting load for {tableName}: {total_rows} total rows.")

        for i in range(0, total_rows, batch_size):
            chunk = data[i : i + batch_size]
            cursor.executemany(insertQry, chunk)
            connection.commit()  # Save progress per batch
            logger.info(f"Data loaded successfully into {tableName} table. Batch {i // batch_size + 1} of {((total_rows - 1) // batch_size) + 1} completed. Rows loaded so far: {min(i + batch_size, total_rows)} of {total_rows}.")
            
        logger.info(f"Data loaded successfully into {tableName} table.")
    except Exception as e:
        connection.rollback()  # Undo the current failed chunk if an error occurs
        print(f"Exception raised for {tableName} of {str(e)}")
        logger.error(f"Error loading data into {tableName} table: {str(e)}")
    finally:
        cursor.close()
        # FIX: The original log message said connection closed, but only the cursor is closed here.
        logger.info(f"Database cursor closed after processing {tableName} table.")