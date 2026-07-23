"""Unit test ensuring no data leakage between Ground Truth and Inference pipeline."""

import os
import pytest
from automedia.providers.local_photo_classifier import LocalPhotoClassifier
from automedia.core.models import ImageAsset


def test_no_data_leakage_for_anonymous_filenames():
    classifier = LocalPhotoClassifier()
    # Anonymous non-semantic asset with no hint in filename
    asset = ImageAsset(path="/dummy/path/IMG_001.jpg", filename="IMG_001.jpg")

    # Classification should depend solely on visual features or return fallback, never hallucinate ground truth
    result = classifier.classify_photo("/dummy/path/IMG_001.jpg", asset)
    assert result.confidence <= 0.85
    assert "Filename keyword match" not in result.reason
