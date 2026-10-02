from models.metadata import ExtractedMetadata
from models.documents import DocumentMetadata
from typing import Literal
import hashlib

def generate_document_id(
    policy_id: str,
    version: str,
    region: str
) -> str:
    combined_string = (
        f"{policy_id.strip().upper()}|"
        f"{version.strip()}|"
        f"{region.strip().lower()}"
    )

    hashed_string = hashlib.sha256(
        combined_string.encode("utf-8")
    ).hexdigest()

    return hashed_string


def normalize_status(
    declared_status: str
) -> Literal["active", "superseded", "draft"]:

    normalized = declared_status.strip().lower()
    status = normalized.split()[0]

    if status in ("active", "superseded", "draft"):
        return status

    raise ValueError(
        f"Unsupported document status: {declared_status}"
    )
    
def resolve_metadata(
    source: str,
    extracted: ExtractedMetadata
) -> DocumentMetadata:
    if not source.strip():
        raise ValueError("Source cannot be empty")
    
    if not extracted.policy_id: 
        raise ValueError("Policy Id does not exist")
    elif not extracted.document_type:
        raise ValueError("Document type does not exist")
    elif not extracted.region:
        raise ValueError("Region does not exist")
    elif not extracted.version:
        raise ValueError("Version does not exist")
    elif not extracted.effective_date:
        raise ValueError("Effective date does not exist")
    elif not extracted.declared_status:
        raise ValueError("Declared status does not exist")

    document_id = generate_document_id(
        policy_id=extracted.policy_id,
        version=extracted.version,
        region=extracted.region
    )

    document = DocumentMetadata(
        document_id = document_id,
        source = source,
        policy_id = extracted.policy_id,
        document_type = extracted.document_type,
        region = extracted.region,
        version = extracted.version,
        effective_date = extracted.effective_date,
        status = normalize_status(
            extracted.declared_status
        ),
        declared_status = extracted.declared_status,
        supersedes_version = extracted.supersedes_version
    )

    return document

def resolve_policy_versions(
    documents: list[DocumentMetadata]
) -> list[DocumentMetadata]:

    copy_docs = [
        document.model_copy(deep = True)
        for document in documents
    ]

    document_lookup = {}
    for doc in copy_docs:
        if doc.document_id in document_lookup:
            raise ValueError(
                f"Duplicate document ID: {doc.document_id}"
            )
        
        document_lookup[doc.document_id] = doc

    superseded_ids: set[str] = set()

    for doc in copy_docs:
        if not doc.supersedes_version:
            continue

        if doc.status != "active":
            continue

        old_doc_id = generate_document_id(
            policy_id=doc.policy_id,
            version=doc.supersedes_version,
            region=doc.region
        )
        
        old_doc = document_lookup.get(old_doc_id)
        
        if not old_doc:
            continue

        validate_effective_date(
            old_doc=old_doc,
            new_doc=doc
        )

        superseded_ids.add(old_doc_id)

    for old_doc_id in superseded_ids:
        document_lookup[old_doc_id].status = "superseded"
        
    return copy_docs

def validate_effective_date(
    old_doc: DocumentMetadata,
    new_doc: DocumentMetadata
): 
    if new_doc.effective_date <= old_doc.effective_date:
        raise ValueError(
            f"Invalid supersession relationship: "
            f"{new_doc.policy_id} v{new_doc.version} cannot supersede "
            f"v{old_doc.version} because its effective date "
            f"is not later."
        )