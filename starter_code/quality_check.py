# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# ==========================================
# Task: Implement quality gates to reject corrupt data or logic discrepancies.

def run_quality_gate(document_dict):
    # 1. Reject documents with 'content' length < 20 characters
    content = document_dict.get('content', '')
    if len(content) < 20:
        print(f"Quality Gate Failed: Content too short for {document_dict.get('document_id')}")
        return False
        
    # 2. Reject documents containing toxic/error strings
    toxic_strings = ['Null pointer exception', 'Access denied', 'Internal server error', 'Segmentation fault']
    for toxic in toxic_strings:
        if toxic.lower() in content.lower():
            print(f"Quality Gate Failed: Toxic/Error string found in {document_dict.get('document_id')}")
            return False
            
    # 3. Flag discrepancies (Example: if legacy code contains conflicting rules)
    # This is more of a logging/warning in this simplified version
    if document_dict.get('source_type') == 'Code':
        if 'tax' in content.lower() and '8%' in content and '10%' in content:
            print(f"Quality Warning: Possible tax logic discrepancy in {document_dict.get('document_id')}")

    return True
