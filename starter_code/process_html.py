from bs4 import BeautifulSoup

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract product data from the HTML table, ignoring boilerplate.

def parse_html_catalog(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    # TODO: Use BeautifulSoup to find the table with id 'main-catalog'
    table = soup.find('table', id='main-catalog')
    
    products = []
    
    # Skip header row (thead)
    for row in table.find('tbody').find_all('tr'):
        cols = row.find_all(['th', 'td'])
        # Skip any potential empty or footer rows
        if not cols or len(cols) < 4: 
            continue
        # Extract and clean data
        product_id = cols[0].get_text(strip=True)
        name = cols[1].get_text(strip=True)
        description = cols[2].get_text(strip=True)
        
        price_text = cols[3].get_text(strip=True)
        # Handle N/A or "Liên hệ"
        if price_text in ['N/A', 'Liên hệ']:
            price = None
        else:
            # Clean and convert
            cleaned = price_text.replace('$', '').replace(',', '').strip()
            try:
                price = float(cleaned)
            except ValueError:
                price = None

        product = {
            "document_id": f"html-prod-{product_id}",
            "content": f"Product: {name}. Description: {description}. Price: {price}",
            "source_type": "HTML",
            "author": "Web Catalog",
            "source_metadata": {
                "product_id": product_id,
                "name": name,
                "price": price,
                "category": "Tablet"
            }
        }
        products.append(product)
    
    return products

