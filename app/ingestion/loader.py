from pathlib import Path
import pymupdf
from app.models.documents import DocumentPage
import logging

def load_pdf(path: str) -> list[DocumentPage]:
    file = Path(path)
    
    if not file.is_file():
        raise FileNotFoundError(f"File not found {file}")

    if not file.suffix.lower() == ".pdf":
        raise ValueError(f"Only pdf files are allowed")
     
    pages: list[DocumentPage] = []

    with pymupdf.open(file) as pdf:
        for page_number, page in enumerate(
            pdf, 
            start=1
        ):
            text = page.get_text(
                "text",
                sort = True
            ).strip()

            if(len(text) < 20):
                try:
                    text_page = (
                        page.get_textpage_ocr(
                            dpi=150
                        )
                    )
                    
                    text = page.get_text(
                        "text",
                        textpage = text_page,
                        sort = True
                    ).strip()
                    
                except Exception as exc:
                    logging.warning(
                        "OCR failed for document %s, page %d: %s",
                        file.name,
                        page_number,
                        exc
                    )

            if(text): 
                pages.append(
                    DocumentPage(
                        source = file.name,
                        page = page_number,
                        text = text
                    )
                )

        return pages
