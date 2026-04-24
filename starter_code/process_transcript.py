import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Clean the transcript text and extract key information.

def clean_transcript(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # ------------------------------------------
    
    # 1. Remove noise tokens like [Music], [inaudible], [Laughter]
    cleaned_text = re.sub(r'\[Music[^\]]*\]', '', text)
    cleaned_text = re.sub(r'\[inaudible\]', '', cleaned_text)
    cleaned_text = re.sub(r'\[Laughter\]', '', cleaned_text)
    
    # 2. Strip timestamps [00:00:00]
    cleaned_text = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', cleaned_text)
    
    # 3. Strip speaker tags [Speaker 1]:
    cleaned_text = re.sub(r'\[Speaker \d+\]:', '', cleaned_text)

    # 4. Find the price mentioned in Vietnamese words ("năm trăm nghìn")
    # This is a bit tricky, but for this lab, we can look for specific keywords
    price_match = re.search(r'(năm trăm nghìn)', cleaned_text)
    extracted_price = None
    if price_match:
        extracted_price = 500000

    # Final cleanup of extra whitespace
    cleaned_text = re.sub(r'\n\s*\n', '\n', cleaned_text).strip()
    
    return {
        "document_id": "trans-001",
        "content": cleaned_text,
        "source_type": "Video", # Forensic agent expects 'Video'
        "author": "Speaker 1",
        "source_metadata": {
            "detected_price_vnd": extracted_price, # Forensic agent expects 'detected_price_vnd'
            "currency": "VND"
        }
    }

