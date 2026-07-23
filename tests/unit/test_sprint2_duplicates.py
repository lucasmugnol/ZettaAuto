"""Unit tests for Sprint 2 Module 4: Near-Duplicate Detection."""

import os
import tempfile
from PIL import Image
from automedia.core.models import ImageAsset, PhotoQualityScore
from automedia.providers.local_duplicate_detector import LocalDuplicateDetector


def test_duplicate_detector_identifies_identical_images():
    detector = LocalDuplicateDetector(hamming_threshold=10)

    with tempfile.TemporaryDirectory() as tmpdir:
        p1 = os.path.join(tmpdir, "car_a.jpg")
        p2 = os.path.join(tmpdir, "car_b_copy.jpg")

        img = Image.new("RGB", (400, 300), color="red")
        img.save(p1)
        img.save(p2)

        assets = [
            ImageAsset(path=p1, filename="car_a.jpg"),
            ImageAsset(path=p2, filename="car_b_copy.jpg")
        ]

        quality_map = {
            "car_a.jpg": PhotoQualityScore(overall_score=80.0),
            "car_b_copy.jpg": PhotoQualityScore(overall_score=70.0)
        }

        groups, dups_removed = detector.detect_duplicates(assets, quality_map)

        assert len(groups) == 1
        assert groups[0].primary_file == "car_a.jpg"
        assert "car_b_copy.jpg" in dups_removed
