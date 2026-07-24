"""Pipeline orchestrator for AutoMedia AI Local Spike (Sprint 2 - Visual Intelligence)."""

import os
import json
import time
import uuid
import datetime
from typing import Dict, Any, Tuple, Optional, List

from automedia.core.models import (
    Job, ImageAsset, VehicleData, BrandConfig, PipelineConfig,
    PlateRegion, VisionAnalysis, ProcessingResult, StageResult, BenchmarkResult,
    PhotoQualityScore, PhotoClassificationResult, DuplicateGroup, GalleryCoverage,
    CoverSelectionResult, PhotoCategory
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

from automedia.modules.quality_analyzer import QualityAnalyzerModule
from automedia.modules.cover_selector import CoverSelector
from automedia.modules.gallery_coverage import GalleryCoverageAnalyzer

from automedia.providers.local_vision_provider import LocalVisionProvider
from automedia.providers.local_image_provider import LocalImageProvider
from automedia.providers.deterministic_text_provider import DeterministicTextProvider
from automedia.providers.local_storage_provider import LocalStorageProvider
from automedia.providers.local_photo_analyzer import LocalPhotoAnalyzer
from automedia.providers.local_photo_classifier import LocalPhotoClassifier
from automedia.providers.local_duplicate_detector import LocalDuplicateDetector


class LocalPipeline:
    def __init__(
        self,
        vision_provider=None,
        image_provider=None,
        text_provider=None,
        storage_provider=None,
        photo_analyzer=None,
        photo_classifier=None,
        duplicate_detector=None
    ):
        self.photo_analyzer = photo_analyzer or LocalPhotoAnalyzer()
        self.photo_classifier = photo_classifier or LocalPhotoClassifier()
        self.duplicate_detector = duplicate_detector or LocalDuplicateDetector()

        self.vision_provider = vision_provider or LocalVisionProvider(
            analyzer=self.photo_analyzer, classifier=self.photo_classifier
        )
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
            status="PENDING",
            started_at=datetime.datetime.now(datetime.timezone.utc).isoformat()
        )

        job.status = "RUNNING"
        benchmark = BenchmarkCollector()
        benchmark.start_measurement()

        warnings: List[str] = []
        errors: List[str] = []

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

            # Stage 3: Visual Intelligence & Quality Analysis
            t0 = time.time()
            quality_module = QualityAnalyzerModule(
                self.photo_analyzer, self.photo_classifier, self.duplicate_detector
            )
            quality_map, class_map, dup_groups, dup_removed = quality_module.analyze_batch(valid_assets)

            # Update duplicate flags on assets
            for asset in valid_assets:
                if asset.filename in dup_removed:
                    asset.is_duplicate = True

            # Vision Analysis
            vision_module = VisionModule(self.vision_provider)
            vision_results = vision_module.analyze(valid_assets, vehicle_data)
            benchmark.record_stage("visual_intelligence", time.time() - t0)

            # Stage 4: Intelligent Cover Selection
            t0 = time.time()
            cover_selector = CoverSelector()
            cover_selection = cover_selector.select_cover(
                valid_assets, quality_map, class_map, dup_removed, vehicle_data
            )
            benchmark.record_stage("cover_selection", time.time() - t0)

            cover_asset = next(a for a in valid_assets if a.filename.lower() == cover_selection.selected_file.lower())
            cover_analysis = next((r for r in vision_results if r.file.lower() == cover_asset.filename.lower()), vision_results[0])

            # Secondary photos (exclude selected cover photo)
            raw_gallery_assets = [a for a in valid_assets if a.filename.lower() != cover_asset.filename.lower()]
            gallery_analyses = [r for r in vision_results if r.file.lower() != cover_asset.filename.lower()]

            # Section 11: Category Hierarchy Gallery Ordering
            CATEGORY_GALLERY_ORDER = {
                PhotoCategory.FRONT_3_4: 1,
                PhotoCategory.FRONT: 2,
                PhotoCategory.LEFT_SIDE: 3,
                PhotoCategory.RIGHT_SIDE: 4,
                PhotoCategory.REAR_3_4: 5,
                PhotoCategory.REAR: 6,
                PhotoCategory.INTERIOR_FRONT: 7,
                PhotoCategory.DASHBOARD: 8,
                PhotoCategory.STEERING: 9,
                PhotoCategory.INTERIOR_REAR: 10,
                PhotoCategory.TRUNK: 11,
                PhotoCategory.ENGINE: 12,
                PhotoCategory.WHEEL: 13,
                PhotoCategory.KEY: 14,
                PhotoCategory.DOCUMENT: 15,
                PhotoCategory.UNKNOWN: 16
            }

            def _gallery_sort_key(asset):
                cat = class_map[asset.filename].category if asset.filename in class_map else PhotoCategory.UNKNOWN
                q_score = quality_map[asset.filename].overall_score if asset.filename in quality_map else 0.0
                order_idx = CATEGORY_GALLERY_ORDER.get(cat, 16)
                return (order_idx, -q_score)

            gallery_assets = sorted(raw_gallery_assets, key=_gallery_sort_key)

            # Stage 5: Gallery Coverage Analysis
            t0 = time.time()
            coverage_analyzer = GalleryCoverageAnalyzer()
            coverage = coverage_analyzer.analyze_coverage(list(class_map.values()))
            benchmark.record_stage("gallery_coverage", time.time() - t0)

            # Stage 6: Prepare Output Directory
            exporter = Exporter(self.storage_provider)
            job_output_dir = exporter.prepare_job_output(output_dir, job_id)
            photos_output_dir = os.path.join(job_output_dir, "photos")

            # Stage 7: Process Cover Image & Compose Layout
            t0 = time.time()
            image_processor = ImageProcessor(self.image_provider, pipeline_cfg)
            brand_composer = BrandComposer(self.image_provider, pipeline_cfg)

            cover_target_dims = (
                pipeline_cfg.cover_dimensions.get("width", 1080),
                pipeline_cfg.cover_dimensions.get("height", 1080)
            )

            temp_cover_path = os.path.join(job_output_dir, "temp_cover.jpg")
            final_cover_path = os.path.join(job_output_dir, "cover.jpg")

            try:
                image_processor.process_image(cover_asset, temp_cover_path, cover_target_dims)

                if cover_analysis.plate_regions:
                    image_processor.apply_plate_cover(
                        temp_cover_path, temp_cover_path, cover_analysis.plate_regions, brand_cfg.primary_color
                    )

                cover_ok = brand_composer.compose_cover(
                    main_image_path=temp_cover_path,
                    output_path=final_cover_path,
                    brand_config=brand_cfg,
                    vehicle_data=vehicle_data,
                    target_dimensions=cover_target_dims
                )

                if not cover_ok or not os.path.exists(final_cover_path):
                    raise CoverFailureError("Cover image composition failed completely.")
            finally:
                self._safe_remove(temp_cover_path, warnings)

            benchmark.record_stage("cover_processing", time.time() - t0)

            # Stage 8: Process Secondary Gallery Images
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
                temp_g_path = os.path.join(photos_output_dir, f"temp_{out_name}")

                try:
                    image_processor.process_image(g_asset, temp_g_path, sec_target_dims)

                    plate_regs = g_analysis.plate_regions if g_analysis else []
                    if plate_regs:
                        image_processor.apply_plate_cover(
                            temp_g_path, temp_g_path, plate_regs, brand_cfg.primary_color
                        )

                    brand_composer.apply_watermark(temp_g_path, out_path, brand_cfg)

                    exported_gallery_files.append(out_path)
                    successful_count += 1
                    benchmark.record_image(g_asset.filename, time.time() - t_img_start)
                except Exception as e:
                    msg = f"Failed processing secondary photo '{g_asset.filename}': {str(e)}"
                    warnings.append(msg)
                    job.failed_images += 1
                finally:
                    self._safe_remove(temp_g_path, warnings)

            job.successful_images = successful_count
            benchmark.record_stage("gallery_processing", time.time() - t0)

            # Stage 9: Text Generator
            t0 = time.time()
            text_gen = TextGenerator(self.text_provider)
            title, description = text_gen.generate(vehicle_data, brand_cfg)
            title_file, desc_file = exporter.export_text_artifacts(job_output_dir, title, description)
            benchmark.record_stage("text_generation", time.time() - t0)

            # Stage 10: Package Output ZIP
            t0 = time.time()
            zip_path = exporter.package_final_output(job_output_dir)
            benchmark.record_stage("export_and_packaging", time.time() - t0)

            # Determine Final Job Status
            if job.failed_images > 0:
                final_status = "PARTIAL"
                warnings.append(f"Job finished with status PARTIAL: {job.failed_images} image(s) failed processing.")
            else:
                final_status = "COMPLETED"

            job.status = final_status
            job.finished_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

            # Compile Quality Report
            good_photos = [f for f, q in quality_map.items() if q.status == "GOOD"]
            warning_photos = [f for f, q in quality_map.items() if q.status == "WARNING"]
            bad_photos = [f for f, q in quality_map.items() if q.status == "BAD"]

            quality_report = {
                "good": good_photos,
                "warning": warning_photos,
                "bad": bad_photos,
                "issues_summary": {
                    f: q.quality_issues for f, q in quality_map.items() if q.quality_issues
                }
            }

            # Stage 11: Write Manifest (Atomic & Expanded)
            manifest_data = {
                "job_id": job_id,
                "pipeline_version": job.pipeline_version,
                "status": final_status,
                "started_at": job.started_at,
                "finished_at": job.finished_at,
                "config_summary": {
                    "brand": brand_cfg.company_name,
                    "vehicle": f"{vehicle_data.manufacturer} {vehicle_data.model}",
                    "strategy": pipeline_cfg.plate_cover_strategy
                },
                "selected_cover": cover_selection.to_dict(),
                "photo_scores": {f: q.to_dict() for f, q in quality_map.items()},
                "photo_categories": {f: c.to_dict() for f, c in class_map.items()},
                "duplicates": {
                    "duplicate_groups": [g.to_dict() for g in dup_groups],
                    "duplicate_removed": dup_removed
                },
                "quality_report": quality_report,
                "gallery_coverage": coverage.to_dict(),
                "input_files": [a.filename for a in raw_assets],
                "input_hashes": {a.filename: a.file_hash for a in raw_assets},
                "output_files": [
                    "cover.jpg",
                    "title.txt",
                    "description.txt",
                    "manifest.json",
                    "benchmark.json",
                    "vehicle_media_package.zip"
                ] + [os.path.relpath(p, job_output_dir) for p in exported_gallery_files],
                "selected_cover_file": cover_asset.filename,
                "cover_selection_method": "vehicle_config" if (vehicle_data.cover_image and vehicle_data.cover_image.lower() == cover_asset.filename.lower()) else "intelligent_ranking",
                "plate_regions": [v.to_dict() for v in vision_results],
                "plate_identification_method": cover_analysis.plate_detection_method,
                "warnings": warnings,
                "errors": errors,
                "providers_used": {
                    "vision": self.vision_provider.__class__.__name__,
                    "image": self.image_provider.__class__.__name__,
                    "text": self.text_provider.__class__.__name__,
                    "storage": self.storage_provider.__class__.__name__,
                    "photo_analyzer": self.photo_analyzer.__class__.__name__,
                    "photo_classifier": self.photo_classifier.__class__.__name__,
                    "duplicate_detector": self.duplicate_detector.__class__.__name__
                }
            }

            manifest_writer = ManifestWriter()
            manifest_path = manifest_writer.write_manifest(job_output_dir, manifest_data)

            # Stage 12: Benchmark Measurement & Export (Atomic)
            total_input_bytes = sum(a.file_size_bytes for a in raw_assets)
            total_output_bytes = self._compute_folder_size(job_output_dir)

            bench_result = benchmark.finish_measurement(
                total_images=len(raw_assets),
                processed_images=successful_count,
                failed_images=job.failed_images,
                total_input_bytes=total_input_bytes,
                total_output_bytes=total_output_bytes
            )

            benchmark_path = benchmark.write_benchmark(job_output_dir, bench_result)

            job.warnings = warnings

            res = ProcessingResult(
                job_id=job_id,
                success=True,
                cover_file=final_cover_path,
                gallery_files=exported_gallery_files,
                text_title_file=title_file,
                text_desc_file=desc_file,
                manifest_file=manifest_path,
                benchmark_file=benchmark_path,
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

    def _safe_remove(self, file_path: str, warnings: List[str]):
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                warnings.append(f"Failed to remove temporary file '{file_path}': {str(e)}")

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
