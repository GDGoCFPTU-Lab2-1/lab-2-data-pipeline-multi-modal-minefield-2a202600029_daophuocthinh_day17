from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ==========================================
# ROLE 1: LEAD DATA ARCHITECT
# ==========================================
# Your task is to define the Unified Schema for all sources.
# This is v1. Note: A breaking change is coming at 11:00 AM!

class UnifiedDocument(BaseModel):
    # This is v1 schema. 
    document_id: str
    content: str
    source_type: str # 'PDF', 'Transcript', 'HTML', 'CSV', 'Code'
    author: Optional[str] = "Unknown"
    timestamp: Optional[datetime] = None
    
    # You might want a dict for source-specific metadata
    source_metadata: dict = Field(default_factory=dict)

    def to_dict(self):
        return self.model_dump()
