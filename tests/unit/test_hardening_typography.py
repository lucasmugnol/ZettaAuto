"""Unit tests for Typography and Font fallbacks."""

import os
import tempfile
from PIL import Image
from automedia.core.models import BrandConfig, VehicleData
from automedia.providers.local_image_provider import LocalImageProvider


def test_missing_font_fallback_and_text_truncation():
    provider = LocalImageProvider()
    brand_cfg = BrandConfig(
        company_name="Typography Dealer",
        font_path="/path/that/does/not/exist/custom_font.ttf"
    )
    vdata = VehicleData(
        manufacturer="Mercedes-Benz AMG",
        model="GT 63 S 4-Door Coupé Special Edition Long Name",
        year=2024,
        price="R$ 1.850.000,00"
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        img_path = os.path.join(tmpdir, "car.jpg")
        img = Image.new("RGB", (800, 600), color="silver")
        img.save(img_path)

        output_path = os.path.join(tmpdir, "cover.jpg")
        success = provider.compose_cover(
            main_image_path=img_path,
            output_path=output_path,
            brand_config=brand_cfg,
            vehicle_data=vdata,
            target_dimensions=(1080, 1080)
        )

        assert success is True
        assert os.path.exists(output_path)
