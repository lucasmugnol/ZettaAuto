"""Unit tests for ManifestWriter and BenchmarkCollector."""

import os
import json
import tempfile
from automedia.modules.manifest import ManifestWriter
from automedia.modules.benchmark import BenchmarkCollector


def test_manifest_writer_creates_valid_json():
    with tempfile.TemporaryDirectory() as tmpdir:
        writer = ManifestWriter()
        data = {
            "job_id": "job_test_123",
            "status": "COMPLETED",
            "input_files": ["car1.jpg"],
            "selected_cover_file": "car1.jpg"
        }

        path = writer.write_manifest(tmpdir, data)
        assert os.path.exists(path)

        with open(path, "r", encoding="utf-8") as f:
            loaded = json.load(f)

        assert loaded["job_id"] == "job_test_123"
        assert loaded["status"] == "COMPLETED"
        assert loaded["selected_cover_file"] == "car1.jpg"


def test_benchmark_collector_records_metrics():
    with tempfile.TemporaryDirectory() as tmpdir:
        collector = BenchmarkCollector()
        collector.start_measurement()

        collector.record_stage("stage1", 0.05)
        collector.record_stage("stage2", 0.10)
        collector.record_image("car1.jpg", 0.04)
        collector.record_image("car2.jpg", 0.06)

        result = collector.finish_measurement(
            total_images=2,
            processed_images=2,
            failed_images=0,
            total_input_bytes=1000,
            total_output_bytes=2000
        )

        assert result.total_images == 2
        assert result.processed_images == 2
        assert result.average_duration_per_image > 0
        assert "stage1" in result.duration_by_stage
        assert "car1.jpg" in result.duration_per_image

        bench_path = collector.write_benchmark(tmpdir, result)
        assert os.path.exists(bench_path)
