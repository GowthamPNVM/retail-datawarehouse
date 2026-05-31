# Total Sales Revenue
SELECT SUM(fact_sales.sales_amount) as total_revenue
FROM fact_sales;

#Total Quantity Sold
SELECT SUM(quantity) as total_quantity 
FROM fact_sales;

#Revenue by Product Category
SELECT SUM(fact_sales.sales_amount) as total_revenue_category_wise,category
FROM fact_sales 
INNER JOIN dim_product ON dim_product.product_key = fact_sales.product_key
GROUP BY dim_product.category
ORDER BY dim_product.category;

#Top by 10 customer based on amount spend
SELECT SUM(fact_sales.sales_amount) as total_spent_by_customer,CONCAT(dim_customer.first_name,' ',dim_customer.last_name) as customer_name
FROM fact_sales 
INNER JOIN dim_customer ON dim_customer.customer_key = fact_sales.customer_key
GROUP BY dim_customer.customer_id
HAVING dim_customer.customer_id!='-1'
ORDER BY total_spent_by_customer DESC;

#Monthly Sales
SELECT SUM(fact_sales.sales_amount) as total_sales_month_wise,dim_date.month,dim_date.month_name,dim_date.year
FROM fact_sales 
INNER JOIN dim_date ON dim_date.date_key = fact_sales.date_key
GROUP BY dim_date.month,dim_date.year
ORDER BY dim_date.year DESC,dim_date.month ASC;

#AVG sale amount
SELECT ROUND(AVG(fact_sales.sales_amount),2) as avg_sales_amount
FROM fact_sales;

