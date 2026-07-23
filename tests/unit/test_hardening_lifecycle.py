"""Unit tests for Job Lifecycle Hardening (FAILED, PARTIAL, COMPLETED)."""

import os
import json
import tempfile
import pytest
from PIL import Image
from automedia.pipeline import LocalPipeline
from automedia.core.models import ProcessingResult
from automedia.core.errors import CoverFailureError, ExportError


class FailingCoverImageProvider:
    def process_and_adjust(self, *args, **kwargs):
        return True

    def apply_plate_cover(self, *args, **kwargs):
        return True

    def apply_watermark(self, *args, **kwargs):
        return True

    def compose_cover(self, *args, **kwargs):
        raise CoverFailureError("Simulated cover failure")


class FailingStorageProvider:
    def create_job_directory(self, base_output_path: str, job_id: str) -> str:
        job_dir = os.path.join(base_output_path, job_id)
        os.makedirs(os.path.join(job_dir, "photos"), exist_ok=True)
        return job_dir

    def save_file(self, destination_path: str, content: bytes) -> str:
        with open(destination_path, "wb") as f:
            f.write(content)
        return destination_path

    def create_zip_archive(self, folder_path: str, zip_output_path: str) -> str:
        raise ExportError("Simulated packaging ZIP failure")


class PartialImageProvider:
    def __init__(self):
        self.call_count = 0

    def process_and_adjust(self, *args, **kwargs):
        self.call_count += 1
        # Fail on 2nd photo call (secondary gallery photo)
        if self.call_count == 2:
            raise RuntimeError("Simulated secondary image processing error")
        return True

    def apply_plate_cover(self, *args, **kwargs):
        return True

    def apply_watermark(self, *args, **kwargs):
        return True

    def compose_cover(self, main_image_path, output_path, *args, **kwargs):
        # Create empty cover file to simulate success
        with open(output_path, "wb") as f:
            f.write(b"cover_bytes")
        return True


def test_cover_failure_results_in_failed_status():
    with tempfile.TemporaryDirectory() as tmpdir:
        input_dir = os.path.join(tmpdir, "input")
        output_dir = os.path.join(tmpdir, "output")
        config_dir = os.path.join(tmpdir, "config")
        os.makedirs(input_dir, exist_ok=True)
        os.makedirs(config_dir, exist_ok=True)

        img = Image.new("RGB", (400, 400), color="blue")
        img.save(os.path.join(input_dir, "car1.jpg"))

        brand_p, vehicle_p, pipe_p = _write_test_configs(config_dir)

        pipeline = LocalPipeline(image_provider=FailingCoverImageProvider())
        job, res = pipeline.run(input_dir, output_dir, brand_p, vehicle_p, pipe_p)

        assert job.status == "FAILED"
        assert res.success is False
        assert len(job.errors) > 0
        assert "Simulated cover failure" in job.errors[0]


def test_packaging_failure_results_in_failed_status():
    with tempfile.TemporaryDirectory() as tmpdir:
        input_dir = os.path.join(tmpdir, "input")
        output_dir = os.path.join(tmpdir, "output")
        config_dir = os.path.join(tmpdir, "config")
        os.makedirs(input_dir, exist_ok=True)
        os.makedirs(config_dir, exist_ok=True)

        img = Image.new("RGB", (400, 400), color="blue")
        img.save(os.path.join(input_dir, "car1.jpg"))

        brand_p, vehicle_p, pipe_p = _write_test_configs(config_dir)

        pipeline = LocalPipeline(storage_provider=FailingStorageProvider())
        job, res = pipeline.run(input_dir, output_dir, brand_p, vehicle_p, pipe_p)

        assert job.status == "FAILED"
        assert res.success is False
        assert any("Simulated packaging ZIP failure" in e for e in job.errors)


def test_secondary_image_failure_results_in_partial_status():
    with tempfile.TemporaryDirectory() as tmpdir:
        input_dir = os.path.join(tmpdir, "input")
        output_dir = os.path.join(tmpdir, "output")
        config_dir = os.path.join(tmpdir, "config")
        os.makedirs(input_dir, exist_ok=True)
        os.makedirs(config_dir, exist_ok=True)

        # 2 images: 1 cover + 1 secondary
        img1 = Image.new("RGB", (400, 400), color="blue")
        img1.save(os.path.join(input_dir, "car1.jpg"))
        img2 = Image.new("RGB", (400, 400), color="green")
        img2.save(os.path.join(input_dir, "car2.jpg"))

        brand_p, vehicle_p, pipe_p = _write_test_configs(config_dir)

        pipeline = LocalPipeline(image_provider=PartialImageProvider())
        job, res = pipeline.run(input_dir, output_dir, brand_p, vehicle_p, pipe_p)

        assert job.status == "PARTIAL"
        assert res.success is True
        assert job.failed_images == 1
        assert job.successful_images == 1
        assert any("PARTIAL" in w for w in job.warnings)

        # Verify manifest json declares PARTIAL
        manifest_path = os.path.join(output_dir, job.job_id, "manifest.json")
        with open(manifest_path, "r", encoding="utf-8") as f:
            m_data = json.load(f)
        assert m_data["status"] == "PARTIAL"


def _write_test_configs(config_dir):
    brand_p = os.path.join(config_dir, "brand.json")
    with open(brand_p, "w", encoding="utf-8") as f:
        json.dump({"company_name": "Test Motors"}, f)

    vehicle_p = os.path.join(config_dir, "vehicle.json")
    with open(vehicle_p, "w", encoding="utf-8") as f:
        json.dump({"manufacturer": "Fiat", "model": "Uno", "year": 2020, "price": "R$ 30.000"}, f)

    pipe_p = os.path.join(config_dir, "pipeline.json")
    with open(pipe_p, "w", encoding="utf-8") as f:
        json.dump({
            "accepted_formats": [".jpg"],
            "cover_dimensions": {"width": 400, "height": 400},
            "secondary_dimensions": {"width": 400, "height": 400},
            "min_width": 100,
            "min_height": 100
        }, f)

    return brand_p, vehicle_p, pipe_p
