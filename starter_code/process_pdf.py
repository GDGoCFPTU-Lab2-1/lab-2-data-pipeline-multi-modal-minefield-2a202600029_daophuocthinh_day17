import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

load_dotenv()

# Use Qwen via OpenAI compatibility
client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url=os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
)
MODEL_NAME = os.getenv("QWEN_MODEL_NAME", "qwen-plus")

def extract_pdf_data(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None
    
    print(f"Extracting text from {file_path}...")
    try:
        reader = PdfReader(file_path)
        text_content = ""
        for page in reader.pages:
            text_content += page.extract_text() + "\n"
    except Exception as e:
        print(f"Failed to read PDF: {e}")
        return None
        
    prompt = f"""
Analyze the following text extracted from a PDF document. 
Extract the Title, Author, and a 3-sentence summary.
Also identify any main topics mentioned.

Text:
{text_content[:4000]}  # Limit text to avoid context window issues

Output exactly as a JSON object matching this exact format:
{{
    "document_id": "pdf-doc-001",
    "content": "Summary: [Insert your 3-sentence summary here]",
    "source_type": "PDF",
    "author": "[Insert author name here]",
    "timestamp": null,
    "source_metadata": {{
        "original_file": "{os.path.basename(file_path)}",
        "topics": ["[topic1]", "[topic2]"]
    }}
}}
"""
    
    print(f"Analyzing PDF content using model {MODEL_NAME}...")
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful data extraction assistant. Output ONLY JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        content_text = response.choices[0].message.content
        
        # Simple cleanup if the response is wrapped in markdown json block
        if "```json" in content_text:
            content_text = content_text.split("```json")[1].split("```")[0]
        elif "```" in content_text:
            content_text = content_text.split("```")[1].split("```")[0]
            
        extracted_data = json.loads(content_text.strip())
        return extracted_data
    except Exception as e:
        print(f"Failed to analyze PDF with LLM: {e}")
        return None
