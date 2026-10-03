from app.ingestion.loader import load_pdf
from app.models.documents import DocumentPage
from app.services.metadata_extractor import extract_metadata
from app.services.embedding_service import embed_texts

def main():
    texts = [
        "Employees receive 24 annual leave days.",
        "Contractors are not eligible for employee benefits.",
        "Employees may work remotely for up to three days per week."
    ]

    vectors = embed_texts(texts)

    print("Total embeddings:", len(vectors))
    print("Vector dimensions:", len(vectors[0]))
        
if __name__ == "__main__":
    main()
