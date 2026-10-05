from models.grading import GradedDocument

def select_relevant_documents(
    documents: list[GradedDocument]
) -> list[GradedDocument]:
    filtered_docs: list[GradedDocument] = []
    for doc in documents:
        if not doc.grade.relevant:
            continue
        filtered_docs.append(doc)

    return filtered_docs
