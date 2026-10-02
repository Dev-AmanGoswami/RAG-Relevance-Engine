from pydantic import BaseModel
from typing import Literal
from datetime import date

class DocumentChunk(BaseModel):
    id: str
    document_id: str
    text: str
    source: str
    page: int | None
    section: str | None
    document_type: str | None
    region: str | None
    version: str | None
    effective_date: date | None
    status: Literal[
        "active", 
        "superseded",
        "draft"
    ]
    content_hash: str

class DocumentPage(BaseModel):
    source: str
    text: str
    page: int | None
