from openai import OpenAI
from config import OPENAI_API_KEY, EMBEDDING_MODEL, EMBEDDING_BATCH_SIZE, EMBEDDING_DIMENSIONS

client = OpenAI(
    api_key = OPENAI_API_KEY
)

BATCH_SIZE = int(EMBEDDING_BATCH_SIZE)
EMBEDDING_DIMENSIONS = int(EMBEDDING_DIMENSIONS)

def embed_texts(texts: list[str]) -> list[list[float]]:
    if BATCH_SIZE <= 0:
        raise ValueError(
            "Embedding batch size must be greater than zero"
        )

    if not texts:
        return []

    for index, text in enumerate(texts):
        if not isinstance(text, str) or not text.strip():
            raise ValueError(
                f"Invalid embedding input at index {index}"
            )

    embeddings = []
    for start in range(
        0, 
        len(texts),
        BATCH_SIZE
    ):
        batch = texts[start : start + BATCH_SIZE]
        response = client.embeddings.create(
            model = EMBEDDING_MODEL,
            input = batch
        )

        ordered = sorted(
            response.data,
            key = lambda item: item.index
        )

        if(len(ordered) != len(batch)):
            raise ValueError(
                "Failed to generate appropiate embeddings"
            )
        

        for item in ordered:
            if(len(item.embedding) != EMBEDDING_DIMENSIONS):
                raise ValueError(
                    "Incorrect embedding dimension error"
                )
            
        embeddings.extend(
            item.embedding
            for item in ordered
        )

    return embeddings