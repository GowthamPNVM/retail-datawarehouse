import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker()

random.seed(42)
np.random.seed(42)


def generate_sales(
        customer_count=30000,
        product_count=3000,
        num_sales=500000
):

    sales = []

    for sale_id in range(1, num_sales + 1):

        sales.append({
            "sale_id": sale_id,
            "customer_id": random.randint(1, customer_count),
            "product_id": random.randint(1, product_count),
            "sale_date": fake.date_between(
                start_date='-2y',
                end_date='today'
            ),
            "quantity": random.randint(1, 10),
            "sale_amount": round(
                random.uniform(50, 5000),
                2
            )
        })

    return pd.DataFrame(sales)


if __name__ == "__main__":

    print("Generating Sales Data...")

    sales_df = generate_sales()

    sales_df.to_csv(
        "data/raw/sales.csv",
        index=False
    )

    print(
        f"Generated {len(sales_df)} sales records"
    )