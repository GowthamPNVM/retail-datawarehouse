import pandas as pd
from datetime import datetime, timedelta


# Function to create a date dimension table
def create_date_dimension(start_date,end_date):
    # Generate date range
    date_range = pd.date_range(start=start_date, end=end_date)
        
    # Create a DataFrame to hold the date dimension
    date_dimension = pd.DataFrame(date_range, columns=['date'])
    
    # Extract date components
    date_dimension['full_date'] = date_dimension['date'].dt.date
    date_dimension['day_name'] = date_dimension['date'].dt.day_name()
    date_dimension['month_name'] = date_dimension['date'].dt.month_name()
    date_dimension['month'] = date_dimension['date'].dt.month
    date_dimension['quarter'] = date_dimension['date'].dt.quarter
    date_dimension['year'] = date_dimension['date'].dt.year
    date_dimension['date_key'] = date_dimension['date'].dt.strftime('%Y%m%d').astype(int)
    # Returns a new DataFrame without 'column_name'
    date_dimension = date_dimension .drop(columns=['date'])
    
    
    return date_dimension
# Example usage
if __name__ == "__main__":
    start_date = '2024-01-01'
    end_date = '2030-12-31'
    date_dim = create_date_dimension(start_date, end_date)
    print(date_dim.head())
    