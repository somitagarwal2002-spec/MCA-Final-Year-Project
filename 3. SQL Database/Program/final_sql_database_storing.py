import pandas as pd
import os
from sqlalchemy import create_engine

# Database path
DB_PATH = "/Users/somitagarwal/Desktop/MCA-Project/ZFinal Database Storage/amazon_products.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
engine = create_engine(f"sqlite:///{DB_PATH}")

def save_cleaned_data(file_path):
    
    print("Loading CSV file...")
    df = pd.read_csv(file_path)
    print(f"Loaded! Total records: {df.shape[0]}")

    try:
        existing_df = pd.read_sql("SELECT title, price FROM amazon_products", engine)
        
        df['temp_key'] = df['title'] + df['price'].astype(str)
        existing_df['temp_key'] = existing_df['title'] + existing_df['price'].astype(str)
        
        new_records = df[~df['temp_key'].isin(existing_df['temp_key'])]
        new_records = new_records.drop(columns=['temp_key'])
        
        print(f"Records already in database: {len(df) - len(new_records)}")
        print(f"New records to add: {len(new_records)}")

    except:
        # Table does not exist yet — first time
        new_records = df
        print("Database is empty. Saving all records...")

    if new_records.shape[0] == 0:
        print("No new records found. Database is already up to date!")
        return

    new_records.to_sql(
        name='amazon_products',
        con=engine,
        if_exists='append',
        index=False
    )

    total = pd.read_sql("SELECT COUNT(*) as total FROM amazon_products", engine)
    print(f"Done! {new_records.shape[0]} new records added.")
    print(f"Total records in database: {total['total'][0]}")


save_cleaned_data("/Users/somitagarwal/Desktop/MCA-Project/ZFinal Cleaned Data/final_cleaned_data.csv")
