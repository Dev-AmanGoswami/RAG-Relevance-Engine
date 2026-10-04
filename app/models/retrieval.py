from pydantic import BaseModel, Field
from models.documents import DocumentChunk

class RetrievalHit(BaseModel):
    chunk: DocumentChunk

    similarity_score: float = Field(
        ge = 0.0,
        le = 1.0
    )