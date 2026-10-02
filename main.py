from app.ingestion.loader import load_pdf
from app.models.documents import DocumentPage
from app.services.metadata_extractor import extract_metadata

def main():
    path = "data/leave_policy_india_2026.pdf"

    pages: list[DocumentPage] = load_pdf(path)     

    metadata = extract_metadata(pages)

    print(
        metadata.model_dump_json(indent=2)
    )
        
if __name__ == "__main__":
    main()
