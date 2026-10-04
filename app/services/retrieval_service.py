from qdrant_client import QdrantClient
from models.retrieval import RetrievalHit
from models.documents import DocumentChunk
from app.services.embedding_service import embed_texts

def retrieve_documents(
    client: QdrantClient,
    collection_name: str,
    question: str,
    top_k: int = 5
) -> list[RetrievalHit]: 
    if not isinstance(question, str) or not question.strip():
        raise ValueError(
            "Parameter: question is invalid."
        )

    if type(top_k) is not int or top_k <= 0:
        raise ValueError(
            "top_k must be a positive integer"
        )

    if not isinstance(collection_name, str) or not collection_name.strip():
        raise ValueError(
            "Parameter: collection_name is invalid."
        )

    query_vector = embed_texts( 
        texts=[question.strip()]
    )[0]

    response = client.query_points(
        collection_name = collection_name,
        query = query_vector,
        limit = top_k,
        with_payload = True
    )

    retrieval_hits: list[RetrievalHit] = []

    for point in response.points:
        payload = point.payload or {}
        try:
            chunk = DocumentChunk(
                id = str(point.id),
                text = payload["text"],
                document_id = payload["document_id"],
                policy_id = payload["policy_id"],
                source = payload["source"],
                page = payload["page"],
                section = payload["section"],
                document_type = payload["document_type"],
                region = payload["region"],
                version = payload["version"],
                status = payload["status"],
                effective_date = payload["effective_date"],
                content_hash = payload["content_hash"],
                chunk_index = payload["chunk_index"]
            )
        except (KeyError, ValueError) as exc:
            raise RuntimeError(
                f"Failed to reconstruct Qdrant point {point.id}"
            ) from exc
        
        retrieval_hits.append(
            RetrievalHit(
                chunk = chunk,
                similarity_score = point.score
            )
        )
    return retrieval_hits