import pandas as pd
import numpy as np

def clean_amazon_data(file_path):

    # Loading Data
    df = pd.read_csv(file_path, skiprows=3)
    print(f"Loaded! Shape: {df.shape}")

    # Validating Columns
    required_columns = ['title', 'price', 'rating', 'reviews', 'discount', 'brand', 'product_url']
    missing_cols = [col for col in required_columns if col not in df.columns]
    
    if missing_cols:
        print(f"Error: These columns are missing: {missing_cols}")
        return None
    print("Required columns are Available")

    # Removing Duplicates
    before = df.shape[0]
    df = df.drop_duplicates()
    after = df.shape[0]
    print(f"Duplicates removed: {before - after} rows")

    # Handling Missing Values
    df['rating']   = df['rating'].fillna(df['rating'].median())
    df['discount'] = df['discount'].fillna(0)
    df['brand']    = df['brand'].fillna('Unknown')
    print("Missing values handle ho gaye!")
 
    # Fixing Data Types
    df['price']    = pd.to_numeric(df['price'],    errors='coerce')
    df['discount'] = pd.to_numeric(df['discount'], errors='coerce').fillna(0)
    df['reviews']  = pd.to_numeric(df['reviews'],  errors='coerce').fillna(0).astype(int)
    print("Data types fixed")

    # Cleaning Brand Column
    df['brand'] = df['brand'].str.replace('Brand: ', '', regex=False).str.strip()
    print("Brand column cleaned")

    # Calculating Original Price
    df['original_price'] = np.where(
        df['discount'] == 0,
        df['price'],
        (df['price'] / (1 - df['discount'] / 100))).round(2)
    print("original_price column added")

    # Adding Site Name Column
    site_name = input("Enter Site Name: ").strip()
    df['site'] = site_name
    print("Site column added")
 
    # Saving Cleaned File
    output_path = file_path.replace('.csv', '_cleaned.csv')
    df.to_csv(output_path, index=False)
    print(f"\n Done! Clean file saved {output_path}")
    print(f"Final Shape: {df.shape}")
    
    return df

df = clean_amazon_data("/Users/somitagarwal/Desktop/MCA Project/Uncleaned data/merge-csv_com__6994ddc3d422d.csv")

# Result after Cleaning
print(df[['title', 'price', 'discount', 'original_price']].head())
