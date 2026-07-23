"""Unit tests for Sprint 2 Module 2: Photo Classification."""

import os
import tempfile
from PIL import Image
from automedia.core.models import ImageAsset, PhotoCategory
from automedia.providers.local_photo_classifier import LocalPhotoClassifier


def test_photo_classifier_keywords():
    classifier = LocalPhotoClassifier()
    dummy_asset = ImageAsset(path="", filename="car_front_3_4.jpg")
    res = classifier.classify_photo("", dummy_asset)
    assert res.category == PhotoCategory.FRONT_3_4

    dummy_dashboard = ImageAsset(path="", filename="painel_dashboard.jpg")
    res_dash = classifier.classify_photo("", dummy_dashboard)
    assert res_dash.category == PhotoCategory.DASHBOARD


def test_photo_classifier_visual_fallback():
    classifier = LocalPhotoClassifier()
    with tempfile.TemporaryDirectory() as tmpdir:
        img_path = os.path.join(tmpdir, "photo_01.jpg")
        img = Image.new("RGB", (1200, 800), color="blue")
        img.save(img_path)

        asset = ImageAsset(path=img_path, filename="photo_01.jpg", width=1200, height=800)
        res = classifier.classify_photo(img_path, asset)

        assert res.category in PhotoCategory.ALL_CATEGORIES
        assert res.confidence > 0.0
