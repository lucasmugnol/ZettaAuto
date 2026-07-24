"""Integration test for full end-to-end local pipeline execution."""

import os
import json
import tempfile
import pytest
from PIL import Image
from automedia.pipeline import LocalPipeline


def test_full_pipeline_end_to_end_integration():
    with tempfile.TemporaryDirectory() as tmpdir:
        input_dir = os.path.join(tmpdir, "input")
        output_dir = os.path.join(tmpdir, "output")
        config_dir = os.path.join(tmpdir, "config")
        os.makedirs(input_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(config_dir, exist_ok=True)

        # 1. Generate synthetic test images
        img1 = Image.new("RGB", (800, 600), color="blue")
        img1_path = os.path.join(input_dir, "car_front.jpg")
        img1.save(img1_path)

        img2 = Image.new("RGB", (800, 600), color="silver")
        img2_path = os.path.join(input_dir, "car_side.jpg")
        img2.save(img2_path)

        logo_img = Image.new("RGBA", (100, 50), color=(255, 0, 0, 200))
        logo_path = os.path.join(config_dir, "logo.png")
        logo_img.save(logo_path)

        # 2. Generate config JSON files
        brand_path = os.path.join(config_dir, "brand.json")
        with open(brand_path, "w", encoding="utf-8") as f:
            json.dump({
                "company_name": "Integration Test Motors",
                "primary_color": "#10B981",
                "secondary_color": "#F59E0B",
                "text_color": "#FFFFFF",
                "logo_path": logo_path,
                "watermark_opacity": 0.4,
                "contact": "(11) 97777-6666",
                "cta": "Test CTA"
            }, f)

        vehicle_path = os.path.join(config_dir, "vehicle.json")
        with open(vehicle_path, "w", encoding="utf-8") as f:
            json.dump({
                "manufacturer": "Volkswagen",
                "model": "Nivus Highline",
                "year": 2023,
                "price": "R$ 125.000",
                "description": "Nivus estado de zero km.",
                "optional_features": ["Painel digital Active Info Display", "ACC"],
                "cover_image": "car_front.jpg",
                "plate_regions": [
                    {
                        "file": "car_front.jpg",
                        "x": 300,
                        "y": 400,
                        "width": 100,
                        "height": 40
                    }
                ]
            }, f)

        pipeline_cfg_path = os.path.join(config_dir, "pipeline.json")
        with open(pipeline_cfg_path, "w", encoding="utf-8") as f:
            json.dump({
                "accepted_formats": [".jpg", ".png"],
                "export_quality": 85,
                "cover_dimensions": {"width": 600, "height": 600},
                "secondary_dimensions": {"width": 600, "height": 600},
                "adjustment_intensity": 0.1,
                "plate_cover_strategy": "solid_cover",
                "watermark_policy": {"position": "bottom_right", "margin_pixels": 15, "scale_ratio": 0.2},
                "min_width": 200,
                "min_height": 200,
                "max_file_size_mb": 10.0,
                "ttl_hours": 12
            }, f)

        # 3. Execute pipeline
        pipeline = LocalPipeline()
        job, res = pipeline.run(
            input_dir=input_dir,
            output_dir=output_dir,
            brand_config_path=brand_path,
            vehicle_config_path=vehicle_path,
            pipeline_config_path=pipeline_cfg_path
        )

        # 4. Assertions
        assert job.status == "COMPLETED"
        assert res.success is True
        assert job.successful_images == 2
        assert job.failed_images == 0

        job_dir = os.path.join(output_dir, job.job_id)
        assert os.path.exists(job_dir)
        assert os.path.exists(os.path.join(job_dir, "cover.jpg"))
        assert len(os.listdir(os.path.join(job_dir, "photos"))) > 0
        assert os.path.exists(os.path.join(job_dir, "title.txt"))
        assert os.path.exists(os.path.join(job_dir, "description.txt"))
        assert os.path.exists(os.path.join(job_dir, "manifest.json"))
        assert os.path.exists(os.path.join(job_dir, "benchmark.json"))
        assert os.path.exists(os.path.join(job_dir, "vehicle_media_package.zip"))

        # Verify title file content
        with open(os.path.join(job_dir, "title.txt"), "r", encoding="utf-8") as f:
            title_text = f.read()
        assert title_text == "Volkswagen Nivus Highline 2023 — R$ 125.000"

        # Verify manifest json content
        with open(os.path.join(job_dir, "manifest.json"), "r", encoding="utf-8") as f:
            manifest_json = json.load(f)
        assert manifest_json["status"] == "COMPLETED"
        assert manifest_json["selected_cover_file"] == "car_front.jpg"
