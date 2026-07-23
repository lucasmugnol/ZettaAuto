"""Unit tests for Sprint 2 Module 3: Intelligent Cover Selection."""

from automedia.core.models import (
    ImageAsset, VehicleData, PhotoQualityScore, PhotoClassificationResult, PhotoCategory
)
from automedia.modules.cover_selector import CoverSelector


def test_cover_selector_ranks_front_3_4_above_interior():
    selector = CoverSelector()
    assets = [
        ImageAsset(path="", filename="interior.jpg"),
        ImageAsset(path="", filename="front_3_4.jpg")
    ]

    quality_map = {
        "interior.jpg": PhotoQualityScore(overall_score=85.0),
        "front_3_4.jpg": PhotoQualityScore(overall_score=80.0)
    }

    class_map = {
        "interior.jpg": PhotoClassificationResult(category=PhotoCategory.INTERIOR_FRONT),
        "front_3_4.jpg": PhotoClassificationResult(category=PhotoCategory.FRONT_3_4)
    }

    res = selector.select_cover(assets, quality_map, class_map, [], VehicleData("Toyota", "Corolla", 2022, "R$ 100k"))

    # FRONT_3_4 must win over interior despite slightly lower quality score because of category priority
    assert res.selected_file == "front_3_4.jpg"
    assert res.rank == 1


def test_cover_selector_respects_explicit_vehicle_config_override():
    selector = CoverSelector()
    assets = [
        ImageAsset(path="", filename="photo_01.jpg"),
        ImageAsset(path="", filename="override_cover.jpg")
    ]

    quality_map = {
        "photo_01.jpg": PhotoQualityScore(overall_score=95.0),
        "override_cover.jpg": PhotoQualityScore(overall_score=60.0)
    }
    class_map = {
        "photo_01.jpg": PhotoClassificationResult(category=PhotoCategory.FRONT_3_4),
        "override_cover.jpg": PhotoClassificationResult(category=PhotoCategory.REAR)
    }

    vdata = VehicleData("Honda", "Civic", 2021, "R$ 90k", cover_image="override_cover.jpg")
    res = selector.select_cover(assets, quality_map, class_map, [], vdata)

    assert res.selected_file == "override_cover.jpg"
    assert "override" in res.reason.lower()
