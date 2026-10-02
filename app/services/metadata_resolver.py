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
    status = normalized.strip()[0]

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

