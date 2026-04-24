import pandas as pd

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Process sales records, handling type traps and duplicates.

def process_sales_csv(file_path):
    # --- FILE READING (Handled for students) ---
    df = pd.read_csv(file_path)
    # ------------------------------------------
    df = df.drop_duplicates(subset=['id'])
    def clean_price(price):
        if isinstance(price, str):
            price = price.lower().strip()
            if price.startswith('$'):
                price = price[1:]
            
            # Handle "five dollars" case
            word_to_digit = {
                "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
            }
            
            if price in word_to_digit:
                price = float(word_to_digit[price])
            else:
                try:
                    price = float(price)
                except ValueError:
                    return None # Failed to convert
        return float(price)

    # Apply cleaning
    df['price'] = df['price'].apply(clean_price)
    
    # Normalize date to YYYY-MM-DD
    df['date_of_sale'] = pd.to_datetime(df['date_of_sale'], errors='coerce').dt.strftime('%Y-%m-%d')

    # Convert to list of dictionaries compatible with UnifiedDocument
    results = []
    for _, row in df.iterrows():
        results.append({
            "document_id": f"csv-sale-{row['id']}",
            "content": f"Sale of {row['product_name']} for {row['price']} on {row['date_of_sale']}",
            "source_type": "CSV",
            "author": "Sales System",
            "timestamp": row['date_of_sale'],
            "source_metadata": {
                "product": row['product_name'],
                "price": row['price'],
                "original_id": row['id']
            }
        })
    return results

