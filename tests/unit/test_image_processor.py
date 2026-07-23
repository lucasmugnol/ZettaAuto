"""Unit tests for ImageProcessor and plate coverage clamping."""

import os
import tempfile
from PIL import Image
from automedia.core.models import PlateRegion, PipelineConfig
from automedia.providers.local_image_provider import LocalImageProvider
from automedia.modules.image_processor import ImageProcessor


def test_plate_cover_clamping_and_strategies():
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "car.jpg")
        img = Image.new("RGB", (500, 500), color="white")
        img.save(input_path)

        provider = LocalImageProvider()
        cfg = PipelineConfig(plate_cover_strategy="solid_cover")
        processor = ImageProcessor(provider, cfg)

        # Plate region with out-of-bounds coordinates (should be clamped)
        out_of_bounds_region = PlateRegion(
            file="car.jpg", x=-50, y=450, width=200, height=100
        )

        output_path = os.path.join(tmpdir, "car_covered.jpg")
        success = processor.apply_plate_cover(
            input_path, output_path, [out_of_bounds_region], primary_color="#1E3A8A"
        )

        assert success is True
        assert os.path.exists(output_path)

        # Verify output image is valid
        with Image.open(output_path) as out_img:
            assert out_img.size == (500, 500)


def test_blur_strategy():
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "car.jpg")
        img = Image.new("RGB", (500, 500), color="red")
        img.save(input_path)

        provider = LocalImageProvider()
        cfg = PipelineConfig(plate_cover_strategy="blur")
        processor = ImageProcessor(provider, cfg)

        region = PlateRegion(file="car.jpg", x=100, y=100, width=80, height=40)
        output_path = os.path.join(tmpdir, "car_blurred.jpg")
        success = processor.apply_plate_cover(
            input_path, output_path, [region], primary_color="#1E3A8A"
        )

        assert success is True
        assert os.path.exists(output_path)
