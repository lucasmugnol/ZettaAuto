"""Unit tests for InputLoader module."""

import os
import tempfile
import pytest
from PIL import Image
from automedia.core.models import PipelineConfig
from automedia.modules.input_loader import InputLoader
from automedia.core.errors import InvalidInputError


def test_input_loader_finds_images():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create two sample image files
        img1 = Image.new("RGB", (400, 400), color="red")
        img1.save(os.path.join(tmpdir, "car1.jpg"))

        img2 = Image.new("RGB", (400, 400), color="blue")
        img2.save(os.path.join(tmpdir, "car2.png"))

        # Create a non-image file that should be ignored
        with open(os.path.join(tmpdir, "notes.txt"), "w") as f:
            f.write("text file")

        cfg = PipelineConfig()
        loader = InputLoader(cfg)
        assets = loader.load_input_images(tmpdir)

        assert len(assets) == 2
        assert [a.filename for a in assets] == ["car1.jpg", "car2.png"]
        assert all(a.file_hash != "" for a in assets)


def test_input_loader_detects_duplicates():
    with tempfile.TemporaryDirectory() as tmpdir:
        img = Image.new("RGB", (400, 400), color="green")
        path1 = os.path.join(tmpdir, "car1.jpg")
        path2 = os.path.join(tmpdir, "car2_copy.jpg")
        img.save(path1)
        img.save(path2)

        cfg = PipelineConfig()
        loader = InputLoader(cfg)
        assets = loader.load_input_images(tmpdir)

        assert len(assets) == 2
        assert assets[0].is_duplicate is False
        assert assets[1].is_duplicate is True


def test_input_loader_invalid_dir():
    cfg = PipelineConfig()
    loader = InputLoader(cfg)
    with pytest.raises(InvalidInputError):
        loader.load_input_images("/path/that/does/not/exist/12345")
