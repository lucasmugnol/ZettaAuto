"""Unit tests for atomic JSON writing in ManifestWriter and BenchmarkCollector."""

import os
import json
import tempfile
import pytest
from automedia.modules.manifest import ManifestWriter
from automedia.modules.benchmark import BenchmarkCollector, BenchmarkResult


def test_manifest_writer_atomic_write():
    writer = ManifestWriter()
    with tempfile.TemporaryDirectory() as tmpdir:
        data = {"job_id": "job_atomic_test", "status": "COMPLETED"}
        manifest_path = writer.write_manifest(tmpdir, data)

        assert os.path.exists(manifest_path)
        assert not os.path.exists(manifest_path + ".tmp")

        with open(manifest_path, "r", encoding="utf-8") as f:
            read_data = json.load(f)
        assert read_data["job_id"] == "job_atomic_test"


def test_benchmark_collector_atomic_write():
    collector = BenchmarkCollector()
    result = BenchmarkResult(
        total_duration_seconds=1.23,
        duration_by_stage={"stage1": 1.0},
        duration_per_image={"img1.jpg": 0.5},
        average_duration_per_image=0.5,
        total_images=1,
        processed_images=1,
        failed_images=0
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        bench_path = collector.write_benchmark(tmpdir, result)
        assert os.path.exists(bench_path)
        assert not os.path.exists(bench_path + ".tmp")

        with open(bench_path, "r", encoding="utf-8") as f:
            read_data = json.load(f)
        assert read_data["total_duration_seconds"] == 1.23
