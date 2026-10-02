from app.services.metadata_resolver import (
    generate_document_id,
    normalize_status
)

import pytest


def test_document_id_is_deterministic():

    first_id = generate_document_id(
        "HR-LV-104",
        "4.0",
        "india"
    )

    second_id = generate_document_id(
        "HR-LV-104",
        "4.0",
        "india"
    )

    assert first_id == second_id
    assert len(first_id) == 64


def test_active_status_normalization():

    result = normalize_status(
        "Active - supersedes version 3.0"
    )

    assert result == "active"


def test_invalid_status():

    with pytest.raises(ValueError):
        normalize_status("Inactive")