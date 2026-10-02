from models.documents import (
    DocumentPage,
    DocumentChunk,
    DocumentMetadata
)

import tiktoken
import hashlib
import uuid

encoding = tiktoken.get_encoding(
    "cl100k_base"
)

def create_chunks(
    pages: list[DocumentPage],
    metadata: DocumentMetadata,
    chunk_size: int = 400,
    overlap: int = 60
) -> list[DocumentChunk]:
    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero")

    if overlap < 0:
        raise ValueError("Overlap cannot be negative")
    
    if overlap >= chunk_size:
        raise ValueError(
            "Overlap must be smaller that Chunk size"
        )

    
    chunks = []
    step = chunk_size - overlap
    global_chunk_index = 0

    for page in pages:
        if page.source != metadata.source:
            raise ValueError(
                f"Source mismatch: {page.source} "
                f"does not match {metadata.source}"
            )
        
        tokens = encoding.encode(
            page.text
        )

        for start in range(
            0, 
            len(tokens),
            step
        ):
            end = start + chunk_size
            chunk_tokens = tokens[start: end]

            token_text = encoding.decode(
                chunk_tokens
            ).strip()

            if not token_text:
                continue

            content_hash = hashlib.sha256(
                token_text.encode()
            ).hexdigest()

            point_id = str(
                uuid.uuid5(
                    uuid.NAMESPACE_URL,
                    (   
                        f"{metadata.document_id}|"
                        f"{page.page}|"
                        f"{global_chunk_index}|"
                        f"{content_hash}"
                    )
                )
            )

            chunks.append(
                DocumentChunk(
                    id = point_id,
                    document_id = metadata.document_id,
                    text = token_text,
                    source = metadata.source,
                    section = None,
                    page = page.page,
                    document_type = metadata.document_type,
                    region = metadata.region,
                    version = metadata.version,
                    effective_date = metadata.effective_date,
                    status = metadata.status,
                    content_hash = content_hash,
                    chunk_index = global_chunk_index
                )
            )

            global_chunk_index += 1

            if end >= len(tokens):
                break

    return chunks