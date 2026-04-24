from pydantic import BaseModel, Field, ConfigDict, field_serializer
from typing import Optional, List, Union
from datetime import datetime

# ==========================================
# ROLE 1: LEAD DATA ARCHITECT
# ==========================================
# Your task is to define the Unified Schema for all sources.
# This is v1. Note: A breaking change is coming at 11:00 AM!

class SourceMetadata(BaseModel):
    model_config = ConfigDict(extra="allow")

    # HTML catalog metadata
    product_id: Optional[str] = None
    name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None

    # CSV sales metadata
    product: Optional[str] = None
    original_id: Optional[Union[int, str]] = None

    # PDF metadata
    original_file: Optional[str] = None
    topics: List[str] = Field(default_factory=list)

    # Transcript metadata
    detected_price_vnd: Optional[int] = None
    currency: Optional[str] = None

    # Legacy code metadata
    file_name: Optional[str] = None
    rule_count: Optional[int] = None

class UnifiedDocument(BaseModel):
    # This is v1 schema. 
    document_id: str
    content: str
    source_type: str # 'PDF', 'Transcript', 'HTML', 'CSV', 'Code'
    author: Optional[str] = "Unknown"
    timestamp: Optional[datetime] = None
    
    source_metadata: SourceMetadata = Field(default_factory=SourceMetadata)

    @field_serializer("source_metadata")
    def serialize_source_metadata(self, source_metadata: SourceMetadata):
        return source_metadata.model_dump(exclude_unset=True)

    def to_dict(self):
        return self.model_dump()
