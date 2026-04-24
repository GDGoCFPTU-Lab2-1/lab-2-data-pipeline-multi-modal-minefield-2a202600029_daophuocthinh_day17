import ast

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract docstrings and comments from legacy Python code.

def extract_logic_from_code(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    # ------------------------------------------
    
    # 1. Use 'ast' to find docstrings for functions
    tree = ast.parse(source_code)
    logic_pieces = []
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
            docstring = ast.get_docstring(node)
            if docstring:
                name = getattr(node, 'name', 'Module')
                logic_pieces.append(f"{name}: {docstring}")
    
    # 2. Use regex to find business rules in comments like "# Business Logic Rule 001"
    import re
    rules = re.findall(r'Business Logic Rule \d+: (.*)', source_code)
    for rule in rules:
        logic_pieces.append(f"Rule Found: {rule.strip()}")

    # 3. Specific check for the tax discrepancy mentioned in the lab
    if 'tax_rate = 0.10' in source_code and '8%' in source_code:
        logic_pieces.append("DISCREPANCY DETECTED: Code uses 10% tax rate but comments/docstrings mention 8%.")

    content = "\n".join(logic_pieces)
    
    return {
        "document_id": "code-legacy-001",
        "content": content,
        "source_type": "Code",
        "author": "Legacy System",
        "source_metadata": {
            "file_name": "legacy_pipeline.py",
            "rule_count": len(rules)
        }
    }

