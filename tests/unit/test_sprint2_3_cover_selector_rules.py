"""Unit tests for CoverSelector rules (Section 10)."""

import pytest
from automedia.modules.cover_selector import CoverSelector
from automedia.core.models import (
    ImageAsset, VehicleData, PhotoQualityScore, PhotoClassificationResult,
    PhotoCategory, MacroCategory
)


def test_cover_selector_engine_and_wheel_never_beat_valid_exterior():
    selector = CoverSelector()

    assets = [
        ImageAsset(path="/path/engine.jpg", filename="engine.jpg", is_valid=True),
        ImageAsset(path="/path/wheel.jpg", filename="wheel.jpg", is_valid=True),
        ImageAsset(path="/path/exterior.jpg", filename="exterior.jpg", is_valid=True)
    ]

    quality_map = {
        "engine.jpg": PhotoQualityScore(overall_score=99.0, status="GOOD"),
        "wheel.jpg": PhotoQualityScore(overall_score=98.0, status="GOOD"),
        "exterior.jpg": PhotoQualityScore(overall_score=70.0, status="GOOD")
    }

    class_map = {
        "engine.jpg": PhotoClassificationResult(category=PhotoCategory.ENGINE, macro_category=MacroCategory.MECHANICAL),
        "wheel.jpg": PhotoClassificationResult(category=PhotoCategory.WHEEL, macro_category=MacroCategory.DETAIL),
        "exterior.jpg": PhotoClassificationResult(category=PhotoCategory.FRONT_3_4, macro_category=MacroCategory.EXTERIOR)
    }

    vdata = VehicleData(manufacturer="Fiat", model="Mobi", year=2023, price="60.000")

    result = selector.select_cover(assets, quality_map, class_map, [], vdata)
    assert result.selected_file == "exterior.jpg"
