"""Benchmark Collector module for execution telemetry and resource measurement."""

import os
import time
import json
from typing import Dict, Any, List, Optional
from automedia.core.models import BenchmarkResult

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class BenchmarkCollector:
    def __init__(self):
        self.start_time: float = 0.0
        self.end_time: float = 0.0
        self.stage_durations: Dict[str, float] = {}
        self.image_durations: Dict[str, float] = {}
        self.warnings: List[str] = []
        self.initial_memory_mb: Optional[float] = None
        self.peak_memory_mb: Optional[float] = None
        self.cpu_usage_percent: Optional[float] = None

    def start_measurement(self):
        self.start_time = time.time()
        if PSUTIL_AVAILABLE:
            try:
                process = psutil.Process()
                self.initial_memory_mb = process.memory_info().rss / (1024 * 1024)
                self.peak_memory_mb = self.initial_memory_mb
                self.cpu_usage_percent = psutil.cpu_percent(interval=None)
            except Exception as e:
                self.warnings.append(f"Memory/CPU measurement warning: {str(e)}")
        else:
            self.warnings.append("psutil library not available; system memory/CPU metrics set to null.")

    def record_stage(self, stage_name: str, duration_seconds: float):
        self.stage_durations[stage_name] = duration_seconds
        self._update_peak_memory()

    def record_image(self, image_filename: str, duration_seconds: float):
        self.image_durations[image_filename] = duration_seconds
        self._update_peak_memory()

    def finish_measurement(
        self,
        total_images: int,
        processed_images: int,
        failed_images: int,
        total_input_bytes: int,
        total_output_bytes: int
    ) -> BenchmarkResult:
        self.end_time = time.time()
        total_duration = self.end_time - self.start_time
        self._update_peak_memory()

        avg_duration = (
            total_duration / processed_images
            if processed_images > 0
            else (total_duration / total_images if total_images > 0 else 0.0)
        )

        return BenchmarkResult(
            total_duration_seconds=total_duration,
            duration_by_stage=self.stage_durations,
            duration_per_image=self.image_durations,
            average_duration_per_image=avg_duration,
            total_images=total_images,
            processed_images=processed_images,
            failed_images=failed_images,
            initial_memory_mb=self.initial_memory_mb,
            peak_memory_mb=self.peak_memory_mb,
            cpu_usage_percent=self.cpu_usage_percent,
            total_input_bytes=total_input_bytes,
            total_output_bytes=total_output_bytes,
            warnings=self.warnings
        )

    def _update_peak_memory(self):
        if PSUTIL_AVAILABLE:
            try:
                process = psutil.Process()
                mem = process.memory_info().rss / (1024 * 1024)
                if self.peak_memory_mb is None or mem > self.peak_memory_mb:
                    self.peak_memory_mb = mem
            except Exception:
                pass

    def write_benchmark(self, job_dir: str, result: BenchmarkResult) -> str:
        benchmark_path = os.path.join(job_dir, "benchmark.json")
        with open(benchmark_path, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
        return benchmark_path
