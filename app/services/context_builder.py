from models.grading import GradedDocument

def build_context(
    documents: list[GradedDocument]
) -> str:
    context_parts: list[str] = []
    for idx, doc in enumerate(documents, start=1):
        if doc is None:
            continue

        chunk = doc.retrieval_hit.chunk
        context_parts.append(
            f"[Source {idx}]\n"
            f"Policy ID: {chunk.policy_id}\n"
            f"Version: {chunk.version}\n"
            f"Region: {chunk.region}\n"
            f"Source: {chunk.source}\n"
            f"Page: {chunk.page}\n\n"

            f"{chunk.text}"
        )

    return "\n\n".join(context_parts)