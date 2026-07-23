"""Unit tests for Validator module."""

import os
import tempfile
import pytest
from PIL import Image
from automedia.core.models import ImageAsset, PipelineConfig
from automedia.modules.validator import Validator
from automedia.core.errors import EmptyBatchError


def test_validator_validates_and_detects_dimensions():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "valid.jpg")
        img = Image.new("RGB", (600, 400), color="red")
        img.save(path)

        asset = ImageAsset(path=path, filename="valid.jpg", file_hash="hash123")
        cfg = PipelineConfig(min_width=300, min_height=300)
        validator = Validator(cfg)

        valid_assets, warnings = validator.validate_assets([asset])
        assert len(valid_assets) == 1
        assert valid_assets[0].width == 600
        assert valid_assets[0].height == 400
        assert valid_assets[0].orientation == "landscape"


def test_validator_rejects_small_resolution():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "small.jpg")
        img = Image.new("RGB", (200, 200), color="red")
        img.save(path)

        asset = ImageAsset(path=path, filename="small.jpg", file_hash="hash123")
        cfg = PipelineConfig(min_width=300, min_height=300)
        validator = Validator(cfg)

        with pytest.raises(EmptyBatchError):
            validator.validate_assets([asset])


def test_validator_rejects_corrupted_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "corrupt.jpg")
        with open(path, "wb") as f:
            f.write(b"not an image data")

        asset = ImageAsset(path=path, filename="corrupt.jpg", file_hash="hash123")
        cfg = PipelineConfig()
        validator = Validator(cfg)

        with pytest.raises(EmptyBatchError):
            validator.validate_assets([asset])
