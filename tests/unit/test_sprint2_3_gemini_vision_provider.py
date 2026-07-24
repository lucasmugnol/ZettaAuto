"""Unit tests for GeminiVisionProvider, JSON schema validation, cache and fallback behavior."""

import os
import json
import tempfile
import pytest
from PIL import Image

from automedia.core.models import ImageAsset, PhotoCategory, MacroCategory
from automedia.core.vision_schemas import parse_and_validate_vision_json
from automedia.providers.gemini_vision_provider import GeminiVisionProvider
from automedia.providers.vision_cache_provider import VisionCacheProvider


def test_parse_and_validate_vision_json_valid_input():
    raw_json = """
    ```json
    {
      "category": "FRONT_3_4",
      "macro_category": "EXTERIOR",
      "confidence": 0.95,
      "suitable_for_cover": true,
      "cover_score": 92.0,
      "quality_status": "GOOD",
      "visual_issues": [],
      "composition_score": 90.0,
      "framing_score": 88.0,
      "vehicle_visibility": 0.95,
      "content_bbox_estimate": {"x": 10, "y": 10, "width": 800, "height": 600},
      "plate_visible": true,
      "plate_bbox": {"x": 100, "y": 400, "width": 150, "height": 50},
      "reasoning_summary": "Clean front 3/4 view"
    }
    ```
    """
    data, err = parse_and_validate_vision_json(raw_json, 1000, 800)
    assert err is None
    assert data["category"] == "FRONT_3_4"
    assert data["macro_category"] == "EXTERIOR"
    assert data["suitable_for_cover"] is True
    assert data["plate_visible"] is True


def test_parse_and_validate_vision_json_rejects_invalid_json():
    raw_text = "This is not json at all."
    data, err = parse_and_validate_vision_json(raw_text)
    assert data is None
    assert "Failed to parse JSON" in err


def test_gemini_vision_provider_fallback_when_api_key_missing(monkeypatch, tmp_path):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.chdir(tmp_path)
    provider = GeminiVisionProvider({"mode": "multimodal", "fallback_to_heuristic": True})

    img_path = str(tmp_path / "test.jpg")
    Image.new("RGB", (800, 600), color="blue").save(img_path)

    asset = ImageAsset(path=img_path, filename="test.jpg", width=800, height=600, is_valid=True)
    res = provider.analyze_image(img_path, asset)

    assert res.fallback_used is True
    assert "GEMINI_API_KEY" in res.fallback_reason
    assert res.inference_status == "FALLBACK_HEURISTIC"


def test_gemini_vision_provider_heuristic_mode_override():
    provider = GeminiVisionProvider({"mode": "heuristic"})

    with tempfile.TemporaryDirectory() as tmpdir:
        img_path = os.path.join(tmpdir, "test.jpg")
        Image.new("RGB", (800, 600), color="blue").save(img_path)

        asset = ImageAsset(path=img_path, filename="test.jpg", width=800, height=600, is_valid=True)
        res = provider.analyze_image(img_path, asset)

        assert res.fallback_used is True
        assert "Mode configured as 'heuristic'" in res.fallback_reason


def test_vision_cache_provider_atomic_set_and_get():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_provider = VisionCacheProvider(cache_dir=tmpdir)
        img_path = os.path.join(tmpdir, "test_cache.jpg")
        Image.new("RGB", (100, 100), color="red").save(img_path)

        test_data = {"category": "FRONT_3_4", "confidence": 0.9}
        saved = cache_provider.set(img_path, "gemini", "gemini-2.5-flash", "v1.0.0", test_data)
        assert saved is True

        cached = cache_provider.get(img_path, "gemini", "gemini-2.5-flash", "v1.0.0")
        assert cached is not None
        assert cached["category"] == "FRONT_3_4"
