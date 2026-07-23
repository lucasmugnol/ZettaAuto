"""Unit tests for Ground Truth schema validation and No-Data-Leakage checks (Sprint 2.2)."""

import os
import json
import tempfile
import pytest
from scripts.real_ground_truth_validation import validate_ground_truth_schema


def test_ground_truth_schema_validation_success():
    valid_gt = {
        "vehicle_id": "vehicle_test",
        "reviewer": "human",
        "photos": {
            "IMG_001.jpg": {
                "category": "FRONT_3_4",
                "macro_category": "EXTERIOR",
                "quality_status": "GOOD",
                "suitable_for_cover": True,
                "cover_rank_human": 1,
                "duplicate_group": None,
                "issues": []
            }
        },
        "expected_gallery_coverage": {"EXTERIOR": True},
        "human_cover_top_3": ["IMG_001.jpg"]
    }
    assert validate_ground_truth_schema(valid_gt, "vehicle_test") is True


def test_ground_truth_schema_validation_raises_error_on_missing_field():
    invalid_gt = {
        "vehicle_id": "vehicle_test",
        "photos": {}
    }
    with pytest.raises(ValueError) as excinfo:
        validate_ground_truth_schema(invalid_gt, "vehicle_test")
    assert "missing required top-level field" in str(excinfo.value)
