"""Pipeline orchestrator for AutoMedia AI Local Spike."""

import os
import json
import time
import uuid
import datetime
from typing import Dict, Any, Tuple, Optional, List

from automedia.core.models import (
    Job, ImageAsset, VehicleData, BrandConfig, PipelineConfig,
    PlateRegion, VisionAnalysis, ProcessingResult, StageResult, BenchmarkResult
)
from automedia.core.errors import (
    AutomediaError, ConfigurationError, InvalidInputError, EmptyBatchError,
    ProcessingError, CoverFailureError, ExportError
)
from automedia.modules.input_loader import InputLoader
from automedia.modules.validator import Validator
from automedia.modules.vision import VisionModule
from automedia.modules.image_processor import ImageProcessor
from automedia.modules.brand_composer import BrandComposer
from automedia.modules.text_generator import TextGenerator
from automedia.modules.exporter import Exporter
from automedia.modules.benchmark import BenchmarkCollector
from automedia.modules.manifest import ManifestWriter

from automedia.providers.local_vision_provider import LocalVisionProvider
from automedia.providers.local_image_provider import LocalImageProvider
from automedia.providers.deterministic_text_provider import DeterministicTextProvider
from automedia.providers.local_storage_provider import LocalStorageProvider


class LocalPipeline:
    def __init__(
        self,
        vision_provider=None,
        image_provider=None,
        text_provider=None,
        storage_provider=None
    ):
        self.vision_provider = vision_provider or LocalVisionProvider()
        self.image_provider = image_provider or LocalImageProvider()
        self.text_provider = text_provider or DeterministicTextProvider()
        self.storage_provider = storage_provider or LocalStorageProvider()

    def run(
        self,
        input_dir: str,
        output_dir: str,
        brand_config_path: str,
        vehicle_config_path: str,
        pipeline_config_path: str
    ) -> Tuple[Job, ProcessingResult]:
        job_id = f"job_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        job = Job(
            job_id=job_id,
            input_path=os.path.abspath(input_dir),
            output_path=os.path.abspath(output_dir),
            status="RUNNING",
            started_at=datetime.datetime.now(datetime.timezone.utc).isoformat()
        )

        benchmark = BenchmarkCollector()
        benchmark.start_measurement()

        warnings: List[str] = []
        errors: List[str] = []
        stages_executed: List[StageResult] = []

        try:
            # Stage 0: Load Configurations
            t0 = time.time()
            brand_cfg, vehicle_data, pipeline_cfg = self._load_configs(
                brand_config_path, vehicle_config_path, pipeline_config_path
            )
            benchmark.record_stage("load_configs", time.time() - t0)

            # Stage 1: Input Loader
            t0 = time.time()
            input_loader = InputLoader(pipeline_cfg)
            raw_assets = input_loader.load_input_images(input_dir)
            benchmark.record_stage("input_loader", time.time() - t0)
            job.total_images = len(raw_assets)

            # Stage 2: Validator
            t0 = time.time()
            validator = Validator(pipeline_cfg)
            valid_assets, val_warnings = validator.validate_assets(raw_assets)
            warnings.extend(val_warnings)
            benchmark.record_stage("validator", time.time() - t0)

            # Stage 3: Vision Analysis
            t0 = time.time()
            vision_module = VisionModule(self.vision_provider)
            vision_results = vision_module.analyze(valid_assets, vehicle_data)
            benchmark.record_stage("vision_analysis", time.time() - t0)

            # Determine cover image asset & secondary gallery assets
            cover_analysis = next((r for r in vision_results if r.recommended_as_cover), vision_results[0])
            cover_asset = next(a for a in valid_assets if a.filename.lower() == cover_analysis.file.lower())

            gallery_analyses = [r for r in vision_results if r.file.lower() != cover_analysis.file.lower()]
            gallery_assets = [a for a in valid_assets if a.filename.lower() != cover_analysis.file.lower()]

            # Stage 4: Prepare Output Directory
            exporter = Exporter(self.storage_provider)
            job_output_dir = exporter.prepare_job_output(output_dir, job_id)
            photos_output_dir = os.path.join(job_output_dir, "photos")

            # Stage 5: Process Cover Image & Compose Layout
            t0 = time.time()
            image_processor = ImageProcessor(self.image_provider, pipeline_cfg)
            brand_composer = BrandComposer(self.image_provider, pipeline_cfg)

            cover_target_dims = (
                pipeline_cfg.cover_dimensions.get("width", 1080),
                pipeline_cfg.cover_dimensions.get("height", 1080)
            )

            temp_cover_path = os.path.join(job_output_dir, "temp_cover.jpg")
            image_processor.process_image(cover_asset, temp_cover_path, cover_target_dims)

            if cover_analysis.plate_regions:
                image_processor.apply_plate_cover(
                    temp_cover_path, temp_cover_path, cover_analysis.plate_regions, brand_cfg.primary_color
                )

            final_cover_path = os.path.join(job_output_dir, "cover.jpg")
            cover_ok = brand_composer.compose_cover(
                main_image_path=temp_cover_path,
                output_path=final_cover_path,
                brand_config=brand_cfg,
                vehicle_data=vehicle_data,
                target_dimensions=cover_target_dims
            )

            if os.path.exists(temp_cover_path):
                os.remove(temp_cover_path)

            if not cover_ok or not os.path.exists(final_cover_path):
                raise CoverFailureError("Cover image composition failed completely.")

            benchmark.record_stage("cover_processing", time.time() - t0)

            # Stage 6: Process Secondary Gallery Images
            t0 = time.time()
            sec_target_dims = (
                pipeline_cfg.secondary_dimensions.get("width", 1080),
                pipeline_cfg.secondary_dimensions.get("height", 1080)
            )

            exported_gallery_files: List[str] = []
            successful_count = 1  # cover succeeded

            for idx, g_asset in enumerate(gallery_assets, start=1):
                t_img_start = time.time()
                g_analysis = next((r for r in gallery_analyses if r.file.lower() == g_asset.filename.lower()), None)
                out_name = f"photo_{idx:02d}.jpg"
                out_path = os.path.join(photos_output_dir, out_name)

                try:
                    # 1. Resize & Color adjust
                    temp_g_path = os.path.join(photos_output_dir, f"temp_{out_name}")
                    image_processor.process_image(g_asset, temp_g_path, sec_target_dims)

                    # 2. Plate Cover if any
                    plate_regs = g_analysis.plate_regions if g_analysis else []
                    if plate_regs:
                        image_processor.apply_plate_cover(
                            temp_g_path, temp_g_path, plate_regs, brand_cfg.primary_color
                        )

                    # 3. Watermark
                    brand_composer.apply_watermark(temp_g_path, out_path, brand_cfg)

                    if os.path.exists(temp_g_path):
                        os.remove(temp_g_path)

                    exported_gallery_files.append(out_path)
                    successful_count += 1
                    benchmark.record_image(g_asset.filename, time.time() - t_img_start)
                except Exception as e:
                    msg = f"Failed processing secondary photo '{g_asset.filename}': {str(e)}"
                    warnings.append(msg)
                    job.failed_images += 1

            job.successful_images = successful_count
            benchmark.record_stage("gallery_processing", time.time() - t0)

            # Stage 7: Text Generator
            t0 = time.time()
            text_gen = TextGenerator(self.text_provider)
            title, description = text_gen.generate(vehicle_data, brand_cfg)
            title_file, desc_file = exporter.export_text_artifacts(job_output_dir, title, description)
            benchmark.record_stage("text_generation", time.time() - t0)

            # Stage 8: Manifest & Benchmark Export
            t0 = time.time()
            total_input_bytes = sum(a.file_size_bytes for a in raw_assets)
            total_output_bytes = self._compute_folder_size(job_output_dir)

            bench_result = benchmark.finish_measurement(
                total_images=len(raw_assets),
                processed_images=successful_count,
                failed_images=job.failed_images,
                total_input_bytes=total_input_bytes,
                total_output_bytes=total_output_bytes
            )

            benchmark.write_benchmark(job_output_dir, bench_result)

            manifest_data = {
                "job_id": job_id,
                "pipeline_version": job.pipeline_version,
                "status": "COMPLETED",
                "started_at": job.started_at,
                "finished_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "duration_seconds": bench_result.total_duration_seconds,
                "config_summary": {
                    "brand": brand_cfg.company_name,
                    "vehicle": f"{vehicle_data.manufacturer} {vehicle_data.model}",
                    "strategy": pipeline_cfg.plate_cover_strategy
                },
                "input_files": [a.filename for a in raw_assets],
                "input_hashes": {a.filename: a.file_hash for a in raw_assets},
                "output_files": [
                    "cover.jpg",
                    "title.txt",
                    "description.txt",
                    "manifest.json",
                    "benchmark.json"
                ] + [os.path.relpath(p, job_output_dir) for p in exported_gallery_files],
                "selected_cover_file": cover_asset.filename,
                "cover_selection_method": "vehicle_config" if (vehicle_data.cover_image and vehicle_data.cover_image.lower() == cover_asset.filename.lower()) else "quality_score_rank",
                "plate_regions": [v.to_dict() for v in vision_results],
                "plate_identification_method": cover_analysis.plate_detection_method,
                "warnings": warnings,
                "errors": errors,
                "providers_used": {
                    "vision": self.vision_provider.__class__.__name__,
                    "image": self.image_provider.__class__.__name__,
                    "text": self.text_provider.__class__.__name__,
                    "storage": self.storage_provider.__class__.__name__
                }
            }

            manifest_writer = ManifestWriter()
            manifest_path = manifest_writer.write_manifest(job_output_dir, manifest_data)

            # Stage 9: Package Output ZIP
            zip_path = exporter.package_final_output(job_output_dir)
            benchmark.record_stage("export_and_packaging", time.time() - t0)

            job.status = "COMPLETED"
            job.finished_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
            job.warnings = warnings

            res = ProcessingResult(
                job_id=job_id,
                success=True,
                cover_file=final_cover_path,
                gallery_files=exported_gallery_files,
                text_title_file=title_file,
                text_desc_file=desc_file,
                manifest_file=manifest_path,
                benchmark_file=os.path.join(job_output_dir, "benchmark.json"),
                warnings=warnings,
                errors=[]
            )
            return job, res

        except Exception as e:
            job.status = "FAILED"
            job.finished_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
            err_msg = str(e)
            job.errors.append(err_msg)

            res = ProcessingResult(
                job_id=job_id,
                success=False,
                warnings=warnings,
                errors=[err_msg]
            )
            return job, res

    def _load_configs(
        self, brand_path: str, vehicle_path: str, pipeline_path: str
    ) -> Tuple[BrandConfig, VehicleData, PipelineConfig]:
        try:
            with open(brand_path, "r", encoding="utf-8") as f:
                b_raw = json.load(f)
            brand_cfg = BrandConfig(**b_raw)
        except Exception as e:
            raise ConfigurationError(f"Invalid brand configuration file '{brand_path}': {str(e)}")

        try:
            with open(vehicle_path, "r", encoding="utf-8") as f:
                v_raw = json.load(f)
            
            plate_regs = []
            if "plate_regions" in v_raw and isinstance(v_raw["plate_regions"], list):
                for pr in v_raw["plate_regions"]:
                    plate_regs.append(PlateRegion(**pr))

            v_dict = dict(v_raw)
            v_dict["plate_regions"] = plate_regs
            vehicle_data = VehicleData(**v_dict)
        except Exception as e:
            raise ConfigurationError(f"Invalid vehicle configuration file '{vehicle_path}': {str(e)}")

        try:
            with open(pipeline_path, "r", encoding="utf-8") as f:
                p_raw = json.load(f)
            pipeline_cfg = PipelineConfig(**p_raw)
        except Exception as e:
            raise ConfigurationError(f"Invalid pipeline configuration file '{pipeline_path}': {str(e)}")

        return brand_cfg, vehicle_data, pipeline_cfg

    def _compute_folder_size(self, folder_path: str) -> int:
        total = 0
        for root, _, files in os.walk(folder_path):
            for file in files:
                total += os.path.getsize(os.path.join(root, file))
        return total
