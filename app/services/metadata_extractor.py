from app.models.documents import DocumentPage
from app.models.metadata import ExtractedMetadata
from config import METADATA_MODEL
from openai import OpenAI
from pathlib import Path

client = OpenAI()

PROMPT_PATH = Path(__file__).resolve().parents[2] / "prompts" / "extract_metadata.txt"

def get_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8").strip()

def extract_metadata(
    pages: list[DocumentPage]
) -> ExtractedMetadata:
    if not pages:
        raise ValueError("No pages provided for metadata extraction")

    first_page = pages[0]
    text = first_page.text 

    if not text:
        raise ValueError(
            f"First page contains no extractable text: "
            f"{first_page.source}"
        )

    response = client.responses.parse(
        model=METADATA_MODEL,
        input=[
            {
                "role": "system",
                "content": get_prompt()
            },
            {
                "role": "user",
                "content": (
                    f"Source: {first_page.source}\n\n"
                    f"Document text: \n{text}"
                )
            }
        ],
        text_format=ExtractedMetadata
    )

    metadata = response.output_parsed

    if metadata is None:
        raise ValueError(
            f"Metadata extraction returned no structured output "
            f"for {first_page.source}"
        )
    return metadata
