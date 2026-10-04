from models.grading import RelevanceGrade, RelevanceLLMOutput, GradedDocument
from models.retrieval import RetrievalHit
from pathlib import Path
from openai import OpenAI
from config import RELEVANCE_GRADER_MODEL
from utils.prompt_extracter import get_prompt

PROMPT_PATH = Path(__file__).resolve().parents[2] / "prompts" / "relevance_grader.txt"
client = OpenAI()

def grade_document(
    question: str,
    document: str
) -> RelevanceGrade:
    if not isinstance(question, str) or not question.strip():
        raise ValueError(
            "Invalid question input."
        )

    if not isinstance(document, str) or not document.strip():
        raise ValueError(
            "Invalid document input."
        )


    response = client.responses.parse(
        model = RELEVANCE_GRADER_MODEL,
        input = [
            {
                "role": "system",
                "content": get_prompt(
                    path = PROMPT_PATH
                )
            },
            {
                "role": "user",
                "content": (
                    f"Question: \n{question.strip()}\n\n"
                    f"Retrieved Document: \n{document}"
                )
            }
        ],
        text_format = RelevanceLLMOutput
    )

    parsed_output = response.output_parsed

    if parsed_output is None:
        raise RuntimeError(
            "Relevance grading returned no structured output"
        )
    
    relevance_grade = RelevanceGrade(
        **parsed_output.model_dump()
    )

    return relevance_grade

def grade_documents(
    question: str,
    documents: list[RetrievalHit]
) -> list[GradedDocument]:
    if not isinstance(question, str) or not question.strip():
        raise ValueError(
            "Invalid question input."
        )

    if not documents:
        return []

    graded_documents: list[GradedDocument] = []
    for hit in documents:
        try:
            grade = grade_document(
                question = question,
                document = hit.chunk.text
            )

            graded_documents.append(GradedDocument(
                retrieval_hit = hit,
                grade = grade
            ))
        except Exception as exc:
            raise RuntimeError(
                f"Failed to grade chunk {hit.chunk.id}"
            ) from exc


    return graded_documents