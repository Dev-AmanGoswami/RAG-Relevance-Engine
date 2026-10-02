from app.ingestion.loader import load_pdf
from app.models.documents import DocumentPage
def main():
    path = "data/leave_policy_india_2026.pdf"
    pages: list[DocumentPage] = load_pdf(path)     

    for page in pages:
        print("-" * 50)
        print(f"Source: {page.source}")
        print(f"Page: {page.page}")
        print(f"Characters: {len(page.text)}")
        print(f"Preview: {page.text[:150]}")
        
if __name__ == "__main__":
    main()
