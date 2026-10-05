from qdrant_client import QdrantClient
from models.applicability import ApplicabilityCriteria
from services.retrieval_service import retrieve_documents
from models.retrieval import RetrievalHit
from models.grading import GradedDocument
from services.relevance_grader import grade_documents
from services.applicability_service import filter_applicable_documents
from services.relevance_decision_service import select_relevant_documents
from services.answer_generator import generate_answer

from services.context_builder import build_context
def answer_question(
    client: QdrantClient,
    collection_name: str,
    question: str,
    criteria: ApplicabilityCriteria,
    top_k: int = 5
) -> str: 
    if not isinstance(question, str) or not question.strip():
        raise ValueError(
            "Parameter: question is invalid"
        )

    if not isinstance(collection_name, str) or not collection_name.strip():
        raise ValueError(
            "Parameter: collection_name is invalid"
        )

    if type(top_k) is not int or top_k <= 0:
        raise ValueError(
            "Parameter: top_k must be a positive integer"
        )

    retrieval_hits: list[RetrievalHit] = retrieve_documents(
        client = client,
        collection_name = collection_name,
        question = question,
        top_k = top_k
    )

    filtered_retrieval_hits: list[RetrievalHit] = filter_applicable_documents(
        hits=retrieval_hits,
        criteria=criteria    
    )

    graded_documents: list[GradedDocument] = grade_documents(
        question=question,
        documents=filtered_retrieval_hits
    )

    relevant_graded_documents: list[GradedDocument] = select_relevant_documents(
        documents=graded_documents
    )

    context = build_context(documents=relevant_graded_documents)

    return generate_answer(
        question=question,
        context=context
    )