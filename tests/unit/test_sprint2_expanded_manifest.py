"""Unit tests for Sprint 2 Module 8: Expanded Manifest Integration."""

import os
import json
import tempfile
from PIL import Image
from automedia.pipeline import LocalPipeline


def test_expanded_manifest_contains_all_sprint2_fields():
    with tempfile.TemporaryDirectory() as tmpdir:
        input_dir = os.path.join(tmpdir, "input")
        output_dir = os.path.join(tmpdir, "output")
        config_dir = os.path.join(tmpdir, "config")
        os.makedirs(input_dir, exist_ok=True)
        os.makedirs(config_dir, exist_ok=True)

        img1 = Image.new("RGB", (800, 600), color="blue")
        img1.save(os.path.join(input_dir, "car_front.jpg"))

        brand_p = os.path.join(config_dir, "brand.json")
        with open(brand_p, "w", encoding="utf-8") as f:
            json.dump({"company_name": "Manifest Motors"}, f)

        vehicle_p = os.path.join(config_dir, "vehicle.json")
        with open(vehicle_p, "w", encoding="utf-8") as f:
            json.dump({"manufacturer": "VW", "model": "Golf", "year": 2022, "price": "R$ 120k"}, f)

        pipe_p = os.path.join(config_dir, "pipeline.json")
        with open(pipe_p, "w", encoding="utf-8") as f:
            json.dump({"accepted_formats": [".jpg"]}, f)

        pipeline = LocalPipeline()
        job, res = pipeline.run(input_dir, output_dir, brand_p, vehicle_p, pipe_p)

        assert res.success is True
        assert os.path.exists(res.manifest_file)

        with open(res.manifest_file, "r", encoding="utf-8") as f:
            m = json.load(f)

        assert "selected_cover" in m
        assert "photo_scores" in m
        assert "photo_categories" in m
        assert "duplicates" in m
        assert "quality_report" in m
        assert "gallery_coverage" in m
        assert "providers_used" in m
        assert "photo_analyzer" in m["providers_used"]
