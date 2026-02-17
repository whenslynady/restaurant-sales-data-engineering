import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import argparse
import psutil
import time

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv('.env')

PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE')

engine = create_engine(f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}')

# -----------------------------
# Transformations function
# -----------------------------
def apply_transformations(df):
    df['order_datetime'] = pd.to_datetime(df['order_datetime'], errors='coerce')
    df['delivery_datetime'] = pd.to_datetime(df['delivery_datetime'], errors='coerce')
    df['prep_time'] = (df['delivery_datetime'] - df['order_datetime']).dt.total_seconds() / 60.0
    df['prep_time'] = df['prep_time'] - 3

    df[['unit_price', 'food_cost', 'total_amount', 'total_amount_discounted']] = \
        df[['unit_price', 'food_cost', 'total_amount', 'total_amount_discounted']].astype(float).round(2)
    df['quantity'] = df['quantity'].astype(int)
    df['total_amount'] = (df['unit_price'] * df['quantity']).round(2)
    df['food_cost'] = (df['unit_price'] - 10).round(2)
    df['total_amount_discounted'] = (df['total_amount'] * (1 - df['discount_percent'])).round(2)

    # Fact table
    fact_sales = df[['sale_id', 'order_id', 'order_datetime', 'estimated_delivery_time',
                     'delivery_datetime', 'total_service_time',
                     'restaurant_id', 'staff_id', 'payment_id', 'promo_id',
                     'item_id', 'quantity', 'unit_price', 'food_cost', 
                     'total_amount', 'total_amount_discounted']]

    # Dimension tables
    dim_items = df[['item_id', 'item_name', 'item_size', 'category', 'ingredients']].drop_duplicates()
    dim_restaurants = df[['restaurant_id', 'restaurant_name', 'restaurant_location']].drop_duplicates()
    dim_staff = df[['staff_id', 'staff_name', 'restaurant_id']].drop_duplicates()
    dim_payments = df[['payment_id', 'payment_method']].drop_duplicates()
    dim_promotions = df[['promo_id', 'discount_percent', 'discount_name']].drop_duplicates()
    dim_customer_satisfaction = df[['sale_id', 'prep_time', 'customer_satisfaction']].drop_duplicates()

    return fact_sales, dim_items, dim_restaurants, dim_staff, dim_payments, dim_promotions, dim_customer_satisfaction

# -----------------------------
# Main function
# -----------------------------
def main(params):
    excel_path = params.excel_path  # path to local Excel file

    print(f"Memory before loading dataset: {psutil.Process().memory_info().rss / (1024 ** 2):.2f} MB")
    start_time = time.time()

    df = pd.read_excel(excel_path)

    print(f"Memory after loading dataset: {psutil.Process().memory_info().rss / (1024 ** 2):.2f} MB")

    fact_sales, dim_items, dim_restaurants, dim_staff, dim_payments, dim_promotions, dim_satisfaction = apply_transformations(df)

    # Load tables into PostgreSQL
    fact_sales.to_sql('Fact_Sales', con=engine, if_exists='replace', index=False)
    dim_items.to_sql('Dim_Items', con=engine, if_exists='replace', index=False)
    dim_restaurants.to_sql('Dim_Restaurants', con=engine, if_exists='replace', index=False)
    dim_staff.to_sql('Dim_Staff', con=engine, if_exists='replace', index=False)
    dim_payments.to_sql('Dim_Payments', con=engine, if_exists='replace', index=False)
    dim_promotions.to_sql('Dim_Promotions', con=engine, if_exists='replace', index=False)
    dim_satisfaction.to_sql('Dim_Satisfaction', con=engine, if_exists='replace', index=False)

    print(f"Total processing time: {time.time() - start_time:.2f} seconds")
    print("Data ingestion completed successfully!")

# -----------------------------
# Command-line arguments
# -----------------------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest local Excel data into PostgreSQL')
    parser.add_argument('--excel_path', required=True, help='Path to the local Excel file (e.g., restaurant_sales_2.xlsx)')

    args = parser.parse_args()
    main(args)
