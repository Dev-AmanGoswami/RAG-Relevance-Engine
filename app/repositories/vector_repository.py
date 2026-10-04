from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)
from models.documents import DocumentChunk
from config import EMBEDDING_DIMENSIONS
import logging

logger = logging.getLogger(__name__)

EMBEDDING_DIMENSIONS = int(EMBEDDING_DIMENSIONS)
def ensure_collection(
    client: QdrantClient,
    collection_name: str,
    vector_size: int
) -> None:
    if not isinstance(collection_name, str) or not collection_name.strip():
        raise ValueError(
            "Invalid collection name"
        )

    if vector_size <= 0:
        raise ValueError(
            "Vector size must be greater than zero"
        )

    is_collection_exist = client.collection_exists(
        collection_name=collection_name
    )

    if is_collection_exist:
        collection_info = client.get_collection(
            collection_name = collection_name
        )

        existing_config = (
            collection_info.config.params.vectors
        )

        if not isinstance(existing_config, VectorParams):
            raise ValueError(
                "Named vector configurations are not supported"
            )

        if existing_config.size != vector_size:
            raise ValueError(
                f"Vector dimension mismatch for '{collection_name}': "
                f"expected {vector_size}, "
                f"found {existing_config.size}"
            )

        if existing_config.distance != Distance.COSINE:
            raise ValueError(
                "Vector similarity is different"
            )
        
        return

    client.create_collection(
        collection_name = collection_name,
        vectors_config = VectorParams(
            size = vector_size,
            distance = Distance.COSINE
        )
    )  

    print(f"Collection '{collection_name}' created successfully!") 

def build_points(
    chunks: list[DocumentChunk],
    embeddings: list[list[float]]
) -> list[PointStruct]:
    if not chunks and not embeddings:
        return []
    
    if len(chunks) != len(embeddings):
        raise ValueError(
            f"Chunk/embedding count mismatch: "
            f"{len(chunks)} chunks, "
            f"{len(embeddings)} embeddings"
        )

    points: list[PointStruct] = []
    seen_ids: set[str] = set()

    for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        if len(embedding) != EMBEDDING_DIMENSIONS:
            raise ValueError(
                f"Invalid embedding dimensions at index {idx}: "
                f"expected {EMBEDDING_DIMENSIONS}, "
                f"received {len(embedding)}"
            )

        if chunk.id in seen_ids:
            raise ValueError(
                f"Duplicate chunk ID detected: {chunk.id}"
            )
        
        point = PointStruct(
            id = chunk.id,
            vector = embedding,
            payload={
                "text": chunk.text,
                "document_id": chunk.document_id,
                "policy_id": chunk.policy_id,
                "source": chunk.source,
                "page": chunk.page,
                "section": chunk.section,
                "document_type": chunk.document_type,
                "region": chunk.region,
                "version": chunk.version,
                "status": chunk.status,
                "effective_date": (
                    chunk.effective_date.isoformat()
                    if chunk.effective_date is not None
                    else None
                ),
                "content_hash": chunk.content_hash,
                "chunk_index": chunk.chunk_index,
                "superseded_on": chunk.superseded_on
            }
        )

        seen_ids.add(chunk.id)
        points.append(point)

    return points

def upsert_points(
    client: QdrantClient,
    collection_name: str,
    points: list[PointStruct],
    batch_size: int = 100
) -> None:
    if batch_size <= 0:
        raise ValueError(
            "Batch size must be greater than zero"
        )

    if not points:
        return 

    for start in range(
        0,
        len(points),
        batch_size
    ):
        end = start + batch_size

        points_batch = points[start: end]
        client.upsert(
            collection_name = collection_name,
            points = points_batch,
            wait = True
        )

        print(f"Points Batch from {start} to {end} has updated successfully.")
        if end >= len(points):
            break
    