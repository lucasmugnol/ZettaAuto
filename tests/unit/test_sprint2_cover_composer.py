"""Unit tests for Cover Composer (Sprint 2 - Parte 1 & Parte 2)."""

import os
import tempfile
import pytest
from PIL import Image
from automedia.core.models import BrandConfig, VehicleData
from automedia.core.errors import CoverFailureError
from automedia.providers.local_image_provider import LocalImageProvider


def test_cover_composer_raises_error_for_nonexistent_image():
    provider = LocalImageProvider()
    brand_cfg = BrandConfig(company_name="Test Dealer")
    vdata = VehicleData(manufacturer="Fiat", model="Uno", year=2020, price="R$ 30.000")

    with pytest.raises(CoverFailureError) as excinfo:
        provider.compose_cover(
            main_image_path="/path/does/not/exist/fake_car.jpg",
            output_path="/tmp/output.jpg",
            brand_config=brand_cfg,
            vehicle_data=vdata,
            target_dimensions=(1080, 1080)
        )
    assert "missing" in str(excinfo.value).lower() or "not exist" in str(excinfo.value).lower()


def test_cover_composer_raises_error_for_corrupted_empty_image():
    provider = LocalImageProvider()
    brand_cfg = BrandConfig(company_name="Test Dealer")
    vdata = VehicleData(manufacturer="Fiat", model="Uno", year=2020, price="R$ 30.000")

    with tempfile.TemporaryDirectory() as tmpdir:
        corrupted_path = os.path.join(tmpdir, "corrupted.jpg")
        with open(corrupted_path, "wb") as f:
            f.write(b"not_an_image")

        with pytest.raises(CoverFailureError) as excinfo:
            provider.compose_cover(
                main_image_path=corrupted_path,
                output_path=os.path.join(tmpdir, "out.jpg"),
                brand_config=brand_cfg,
                vehicle_data=vdata,
                target_dimensions=(1080, 1080)
            )
        assert "corrupted" in str(excinfo.value).lower() or "error" in str(excinfo.value).lower()


def test_cover_composer_handles_various_image_aspects():
    provider = LocalImageProvider()
    brand_cfg = BrandConfig(company_name="Test Dealer")
    vdata = VehicleData(manufacturer="Toyota", model="Corolla", year=2023, price="R$ 140.000")

    aspect_test_cases = [
        ("very_small.jpg", (50, 50)),
        ("vertical.jpg", (600, 1200)),
        ("horizontal.jpg", (1200, 800)),
        ("panoramic.jpg", (1600, 500)),
        ("square.jpg", (800, 800))
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        for filename, (w, h) in aspect_test_cases:
            img_p = os.path.join(tmpdir, filename)
            out_p = os.path.join(tmpdir, f"cover_{filename}")

            img = Image.new("RGB", (w, h), color="blue")
            img.save(img_p)

            success = provider.compose_cover(
                main_image_path=img_p,
                output_path=out_p,
                brand_config=brand_cfg,
                vehicle_data=vdata,
                target_dimensions=(1080, 1080)
            )

            assert success is True
            assert os.path.exists(out_p)
            with Image.open(out_p) as result_img:
                assert result_img.size == (1080, 1080)


def test_cover_composer_off_center_vehicle_auto_offset():
    provider = LocalImageProvider()
    brand_cfg = BrandConfig(company_name="Test Dealer")
    vdata = VehicleData(manufacturer="BMW", model="M3", year=2024, price="R$ 600.000")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create image with off-center object (right side of photo)
        img_p = os.path.join(tmpdir, "off_center.jpg")
        out_p = os.path.join(tmpdir, "cover_off_center.jpg")

        img = Image.new("RGB", (1000, 600), color=(240, 240, 240))
        # Draw high-contrast subject on right side (x=600..900, y=200..500)
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.rectangle([600, 200, 900, 500], fill=(20, 20, 20))
        img.save(img_p)

        success = provider.compose_cover(
            main_image_path=img_p,
            output_path=out_p,
            brand_config=brand_cfg,
            vehicle_data=vdata,
            target_dimensions=(1080, 1080)
        )

        assert success is True
        assert os.path.exists(out_p)
