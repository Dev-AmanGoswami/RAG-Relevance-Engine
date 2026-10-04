from pydantic import BaseModel, Field, computed_field
from typing import Literal
from models.retrieval import RetrievalHit

class RelevanceGrade(BaseModel):
    score: float = Field(
        ge = 0.0,
        le = 1.0
    )
    reason: str
    evidence_type: Literal[
        "direct",
        "partial",
        "contextual",
        "none"
    ]

    @computed_field
    @property
    def relevant(self) -> bool:
        return self.evidence_type in ("direct", "partial")


class GradedDocument(BaseModel):
    retrieval_hit: RetrievalHit
    grade: RelevanceGrade


class RelevanceLLMOutput(BaseModel):
    evidence_type: Literal[
        "direct",
        "partial",
        "contextual",
        "none"
    ]

    score: float = Field(ge=0.0, le=1.0)
    reason: str