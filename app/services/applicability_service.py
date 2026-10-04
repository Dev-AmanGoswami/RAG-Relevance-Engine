from models.applicability import ApplicabilityCriteria
from models.retrieval import RetrievalHit
from datetime import date

def filter_applicable_documents(
    hits: list[RetrievalHit],
    criteria: ApplicabilityCriteria
) -> list[RetrievalHit]:
    result_hits: list[RetrievalHit] = []
    for hit in hits:
        chunk = hit.chunk

        if criteria.region is not None:
            if chunk.region not in (criteria.region, "global"):
                continue

        if criteria.policy_id is not None:
            if chunk.policy_id != criteria.policy_id:
                continue
    
        if criteria.as_of_date is not None:
            if chunk.status == "superseded" and chunk.superseded_on is None:
                raise ValueError(
                    f"Missing supersession date for chunk: {chunk.id}"
                )
            
            is_valid = is_within_validity_window(
                effective_date=chunk.effective_date,
                superseded_on=chunk.superseded_on,
                as_of_date=criteria.as_of_date
            )
            
            if not is_valid:
                continue

            if chunk.status == "draft":
                continue

        elif criteria.current_only:
            if chunk.status != "active":
                continue
            
        result_hits.append(hit)

    return result_hits

def is_effective_on(
    effective_date: date | None,
    as_of_date: date
) -> bool:
    if effective_date is None:
        return False

    return effective_date <= as_of_date


def is_within_validity_window(
    effective_date: date | None,
    superseded_on: date | None, 
    as_of_date: date
) -> bool: 
    if not is_effective_on(effective_date, as_of_date):
        return False

    if superseded_on is None:
        return True

    return as_of_date < superseded_on