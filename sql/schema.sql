#SQL script to create the schema for the sales data warehouse
#This script creates a star schema with one fact table (fact_sales) and three dimension tables (dim_customer, dim_product, dim_date).

#DATABASE NAME: sales_dw
#DATABASE NAME: sales_dw
CREATE DATABASE IF NOT EXISTS sales_dw;
USE sales_dw;


#Dimension tables
CREATE TABLE IF NOT EXISTS dim_customer(
    customer_key INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100), 
    country VARCHAR(100),
    effective_date DATE,
    expiry_date DATE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) DEFAULT 'ADMIN',
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(50) DEFAULT 'ADMIN',
    current_flag BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS dim_product(
    product_key INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT,
    product_name VARCHAR(100),
    category VARCHAR(100),
    price DECIMAL(10, 2),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) DEFAULT 'ADMIN',
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,   
    updated_by VARCHAR(50) DEFAULT 'ADMIN',
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS dim_date(
    date_key INT PRIMARY KEY NOT NULL,
    full_date DATE,
    day_name VARCHAR(20),
    month_name VARCHAR(20),
    month INT,
    quarter INT,
    year INT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) DEFAULT 'ADMIN',
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(50) DEFAULT 'ADMIN'
);
#Fact table
CREATE TABLE IF NOT EXISTS fact_sales(
    sales_key INT PRIMARY KEY AUTO_INCREMENT,
    product_key INT,
    customer_key INT,
    date_key INT,
    sales_amount DECIMAL(10, 2),
    quantity INT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) DEFAULT 'ADMIN',
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(50) DEFAULT 'ADMIN'
);


#ALTER TABLE `sales_dw`.`dim_date` CHANGE COLUMN `date_key` `date_key` INT NOT NULL ;

ALTER TABLE fact_sales
ADD CONSTRAINT FK_Product
FOREIGN KEY (product_key) REFERENCES dim_product(product_key);
ADD CONSTRAINT FK_CustomerOrder
FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key);
ADD CONSTRAINT FK_Date
FOREIGN KEY (date_key) REFERENCES dim_date(date_key);

-- 1. Insert the default missing row for Customers that for unknown customers
INSERT INTO dim_customer (customer_key, customer_id, first_name, last_name, email, city, state, country, effective_date, expiry_date)
VALUES (-1, -1, 'Unknown', 'Customer', 'unknown.customer@example.com', 'Unknown', 'Unknown', 'Unknown', '1900-01-01', '9999-12-31');
-- 2. Insert the default missing row for Products that for unknown products
INSERT INTO dim_product (product_key, product_id, product_name, category, price) 
VALUES (-1, -1,     'Unknown Product', 'Unknown', 0.00);
-- 3. Insert the default missing row for Dates that for unknown dates   
INSERT INTO dim_date (date_key, full_date, day_name, month_name, month, quarter, year)
VALUES (-1, '1900-01-01', 'Monday', 'January', 1, 1, 1900);