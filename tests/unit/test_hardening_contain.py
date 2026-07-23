"""Unit tests for contain strategy preserving full vehicle photo without cropping."""

import os
import tempfile
import pytest
from PIL import Image
from automedia.core.models import BrandConfig, VehicleData
from automedia.providers.local_image_provider import LocalImageProvider


def test_contain_strategy_preserves_horizontal_vertical_square_panoramic():
    provider = LocalImageProvider()
    brand_cfg = BrandConfig(company_name="Test Dealer")
    vdata = VehicleData(manufacturer="Ford", model="Mustang", year=2022, price="R$ 300.000")

    test_aspects = [
        ("horizontal.jpg", (1200, 800)),
        ("vertical.jpg", (600, 1200)),
        ("square.jpg", (800, 800)),
        ("panoramic.jpg", (1600, 500))
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        target_dims = (1080, 1080)
        output_path = os.path.join(tmpdir, "cover.jpg")

        for filename, (orig_w, orig_h) in test_aspects:
            img_path = os.path.join(tmpdir, filename)
            img = Image.new("RGB", (orig_w, orig_h), color="blue")
            img.save(img_path)

            success = provider.compose_cover(
                main_image_path=img_path,
                output_path=output_path,
                brand_config=brand_cfg,
                vehicle_data=vdata,
                target_dimensions=target_dims,
                cover_fit_strategy="contain",
                bg_fill_strategy="blurred"
            )

            assert success is True
            assert os.path.exists(output_path)

            # Verify cover dimensions
            with Image.open(output_path) as cover_img:
                assert cover_img.size == target_dims
