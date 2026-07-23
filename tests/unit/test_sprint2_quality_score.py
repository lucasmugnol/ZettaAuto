"""Unit tests for Sprint 2 Module 1: Quality Score analysis."""

import os
import tempfile
from PIL import Image
from automedia.core.models import ImageAsset
from automedia.providers.local_photo_analyzer import LocalPhotoAnalyzer


def test_quality_score_good_photo():
    analyzer = LocalPhotoAnalyzer()
    with tempfile.TemporaryDirectory() as tmpdir:
        img_path = os.path.join(tmpdir, "good_photo.jpg")
        img = Image.new("RGB", (1200, 800), color=(180, 180, 180))
        img.save(img_path)

        asset = ImageAsset(path=img_path, filename="good_photo.jpg", width=1200, height=800, orientation="landscape")
        score = analyzer.analyze_quality(img_path, asset)

        assert 0.0 <= score.overall_score <= 100.0
        assert score.status in ("GOOD", "WARNING", "BAD")
        assert isinstance(score.quality_issues, list)


def test_quality_score_dark_photo_issues():
    analyzer = LocalPhotoAnalyzer()
    with tempfile.TemporaryDirectory() as tmpdir:
        img_path = os.path.join(tmpdir, "dark_photo.jpg")
        img = Image.new("RGB", (400, 300), color=(10, 10, 10))
        img.save(img_path)

        asset = ImageAsset(path=img_path, filename="dark_photo.jpg", width=400, height=300, orientation="landscape")
        score = analyzer.analyze_quality(img_path, asset)

        assert "too_dark" in score.quality_issues
        assert "low_resolution" in score.quality_issues
        assert score.status in ("WARNING", "BAD")
