#Top customer per country 

WITH CountrySales AS (
    SELECT CONCAT(dc.first_name,' ',dc.last_name) as full_name,dc.country,dc.customer_id, SUM(fs.sales_amount) as sales_country_wise,
    ROW_NUMBER() OVER (PARTITION BY dc.country ORDER BY SUM(fs.sales_amount) DESC) as row_rank
    FROM fact_sales fs
    INNER JOIN dim_customer dc ON dc.customer_key = fs.customer_key
    GROUP BY dc.country,dc.customer_id
)

SELECT full_name, country, customer_id, sales_country_wise
FROM CountrySales
WHERE row_rank < 5 AND customer_id != '-1';

SELECT 
SUM(sales_amount) daily_revenue,
SUM(SUM(sales_amount)) OVER (ORDER BY dim_date.full_date ASC ) AS running_revenue,
dim_date.full_date
FROM fact_sales
INNER JOIN dim_date ON dim_date.date_key = fact_sales.date_key
GROUP BY dim_date.full_date
ORDER BY dim_date.full_date ASC;

CREATE OR REPLACE VIEW retail_sales AS (
SELECT CONCAT(dc.first_name,' ',dc.last_name) as full_name,dc.customer_id,dp.product_name,dp.product_id,dd.full_date,fs.sales_amount,fs.quantity
FROM fact_sales fs
INNER JOIN dim_customer dc ON dc.customer_key = fs.customer_key
INNER JOIN dim_product dp ON dp.product_key = fs.product_key
INNER JOIN dim_date dd ON dd.date_key = fs.date_key
);

SELECT * FROM retail_sales
WHERE (customer_id!=-1 AND product_id!=-1) AND full_date >= '2024-01-01' AND full_date < '2025-01-01' ;