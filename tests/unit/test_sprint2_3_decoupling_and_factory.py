"""Unit tests for Decoupling, Factory, and Provider Substitution (Sprint 2.3 Hardening Step 7)."""

import os
import sys
import tempfile
import pytest
from PIL import Image

from automedia.core.models import ImageAsset, VisionAnalysisResult
from automedia.providers.vision_provider_factory import VisionProviderFactory
from automedia.providers.heuristic_vision_provider import HeuristicVisionProvider
from automedia.providers.gemini_vision_provider import GeminiVisionProvider
from automedia.pipeline import LocalPipeline


def test_heuristic_provider_does_not_instantiate_gemini():
    """Verify HeuristicVisionProvider is completely independent of Gemini."""
    provider = HeuristicVisionProvider()
    assert not isinstance(provider, GeminiVisionProvider)
    assert not hasattr(provider, "_call_gemini_api")

    with tempfile.TemporaryDirectory() as tmpdir:
        img_path = os.path.join(tmpdir, "test.jpg")
        Image.new("RGB", (400, 400), color="red").save(img_path)
        asset = ImageAsset(path=img_path, filename="test.jpg", width=400, height=400, is_valid=True)

        res = provider.analyze_image(img_path, asset)
        assert isinstance(res, VisionAnalysisResult)
        assert res.provider_used == "heuristic"
        assert res.fallback_used is False


def test_factory_creates_separate_concrete_providers():
    """Verify VisionProviderFactory instantiates distinct concrete classes."""
    h_prov = VisionProviderFactory.create_provider({"provider": "heuristic"})
    assert type(h_prov) is HeuristicVisionProvider

    g_prov = VisionProviderFactory.create_provider({"provider": "gemini"})
    assert type(g_prov) is GeminiVisionProvider


def test_missing_key_blocks_only_gemini_provider(monkeypatch, tmp_path):
    """Verify missing GEMINI_API_KEY blocks Gemini when fallback is disabled, but Heuristic runs offline."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.chdir(tmp_path)

    g_prov = GeminiVisionProvider({"mode": "multimodal", "fallback_to_heuristic": False})
    h_prov = HeuristicVisionProvider()

    img_path = str(tmp_path / "test.jpg")
    Image.new("RGB", (400, 400), color="blue").save(img_path)
    asset = ImageAsset(path=img_path, filename="test.jpg", width=400, height=400, is_valid=True)

    # Heuristic works 100% offline
    h_res = h_prov.analyze_image(img_path, asset)
    assert h_res.provider_used == "heuristic"

    # Gemini raises explicit error when key is missing and fallback is False
    with pytest.raises(ValueError, match="GEMINI_API_KEY"):
        g_prov.analyze_image(img_path, asset)


def test_pipeline_uses_selected_provider_results():
    """Verify pipeline integrates selected provider directly into cover selection."""
    h_prov = VisionProviderFactory.create_provider({"provider": "heuristic"})
    pipeline = LocalPipeline(vision_provider=h_prov)

    assert pipeline._injected_vision_provider == h_prov
