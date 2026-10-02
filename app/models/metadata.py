from datetime import date
from typing import Literal
from pydantic import BaseModel

class ExtractedMetadata(BaseModel):
    policy_id: str | None
    document_type: str | None
    region: Literal["india", "us", "global"] | None
    version: str | None
    effective_date: date | None
    declared_status: str | None
    supersedes_version: str | None
