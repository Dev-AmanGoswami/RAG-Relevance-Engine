from datetime import date
from typing import Literal
from pydantic import BaseModel

class ApplicabilityCriteria(BaseModel):
    region: Literal["india", "us"] | None = None
    as_of_date: date | None = None
    policy_id: str | None = None
    current_only: bool = True
    