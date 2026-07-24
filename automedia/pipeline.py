"""Pipeline orchestrator for AutoMedia AI Local Spike (Sprint 2.3 Refactored)."""

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
    CoverSelectionResult, PhotoCategory, MacroCategory, VisionAnalysisResult
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

from automedia.providers.vision_provider_factory import VisionProviderFactory
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

        self._injected_vision_provider = vision_provider
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

            # Resolve Vision Provider
            if self._injected_vision_provider:
                active_vision_provider = self._injected_vision_provider
            else:
                config_file = os.path.join("config", "visual_intelligence.json")
                cfg_data = {}
                if os.path.exists(config_file):
                    with open(config_file, "r", encoding="utf-8") as f:
                        cfg_data = json.load(f).get("vision_provider", {})
                active_vision_provider = VisionProviderFactory.create_provider(cfg_data)

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

            # Stage 3: Visual Intelligence (Selected Provider + Local Duplicate Detection)
            t0 = time.time()
            vision_analysis_map: Dict[str, VisionAnalysisResult] = {}
            class_result_list: List[PhotoClassificationResult] = []
            quality_map_legacy: Dict[str, PhotoQualityScore] = {}
            class_map_legacy: Dict[str, PhotoClassificationResult] = {}

            for asset in valid_assets:
                analysis_res = active_vision_provider.analyze_image(asset.path, asset)
                vision_analysis_map[asset.filename] = analysis_res

                q_score = PhotoQualityScore(overall_score=analysis_res.quality_score, status="GOOD" if analysis_res.quality_score >= 60 else "WARNING")
                c_res = PhotoClassificationResult(category=analysis_res.category, macro_category=analysis_res.macro_category, confidence=analysis_res.confidence)
                
                quality_map_legacy[asset.filename] = q_score
                class_map_legacy[asset.filename] = c_res
                class_result_list.append(c_res)

            # Local duplicate detection
            dup_groups, dup_removed = self.duplicate_detector.detect_duplicates(valid_assets, quality_map_legacy)
            for asset in valid_assets:
                if asset.filename in dup_removed:
                    asset.is_duplicate = True
                    if asset.filename in vision_analysis_map:
                        vision_analysis_map[asset.filename].duplicate_flag = True

            # Vision Analysis objects for plate regions
            vision_results = []
            for asset in valid_assets:
                va_res = vision_analysis_map[asset.filename]
                plate_regs = []
                if va_res.plate_visible and va_res.plate_bbox:
                    pb = dict(va_res.plate_bbox)
                    pb.setdefault("file", asset.filename)
                    plate_regs.append(PlateRegion(**pb))
                vision_results.append(VisionAnalysis(file=asset.filename, category=va_res.category, confidence=va_res.confidence, plate_regions=plate_regs))

            benchmark.record_stage("visual_intelligence", time.time() - t0)

            # Stage 4: Intelligent Cover Selection (Consumes Selected Provider's VisionAnalysisResult)
            t0 = time.time()
            cover_selector = CoverSelector()
            cover_selection = cover_selector.select_cover(
                assets=valid_assets,
                analyses=vision_analysis_map,
                duplicate_files=dup_removed,
                vehicle_data=vehicle_data
            )
            benchmark.record_stage("cover_selection", time.time() - t0)

            cover_asset = next(a for a in valid_assets if a.filename.lower() == cover_selection.selected_file.lower())
            cover_analysis = next((r for r in vision_results if r.file.lower() == cover_asset.filename.lower()), vision_results[0])

            # Secondary photos (exclude selected cover photo and duplicates)
            raw_gallery_assets = [a for a in valid_assets if a.filename.lower() != cover_asset.filename.lower() and a.filename not in dup_removed]
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
                cat = vision_analysis_map[asset.filename].category if asset.filename in vision_analysis_map else PhotoCategory.UNKNOWN
                q_score = vision_analysis_map[asset.filename].quality_score if asset.filename in vision_analysis_map else 0.0
                order_idx = CATEGORY_GALLERY_ORDER.get(cat, 16)
                return (order_idx, -q_score)

            gallery_assets = sorted(raw_gallery_assets, key=_gallery_sort_key)

            # Stage 5: Gallery Coverage Analysis
            t0 = time.time()
            coverage_analyzer = GalleryCoverageAnalyzer()
            coverage = coverage_analyzer.analyze_coverage(class_result_list)
            benchmark.record_stage("gallery_coverage", time.time() - t0)

            # Stage 6: Prepare Output Directory
            exporter = Exporter(self.storage_provider)
            job_output_dir = exporter.prepare_job_output(output_dir, job_id)
            photos_output_dir = os.path.join(job_output_dir, "photos")
            os.makedirs(photos_output_dir, exist_ok=True)

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

                    if os.path.exists(out_path):
                        exported_gallery_files.append(out_name)
                        successful_count += 1
                        benchmark.record_image(g_asset.filename, time.time() - t_img_start)
                    else:
                        warnings.append(f"Gallery image '{g_asset.filename}' failed export.")
                except Exception as e:
                    warnings.append(f"PARTIAL processing: Failed secondary image '{g_asset.filename}': {str(e)}")
                finally:
                    self._safe_remove(temp_g_path, warnings)

            benchmark.record_stage("secondary_processing", time.time() - t0)

            # Stage 9: Generate Ad Copy Texts
            t0 = time.time()
            title_text, desc_text = self.text_provider.generate_ad_text(vehicle_data, brand_cfg)

            title_file_path = os.path.join(job_output_dir, "title.txt")
            desc_file_path = os.path.join(job_output_dir, "description.txt")

            self.storage_provider.save_file(title_file_path, title_text.encode("utf-8"))
            self.storage_provider.save_file(desc_file_path, desc_text.encode("utf-8"))
            benchmark.record_stage("text_generation", time.time() - t0)

            # Determine status
            job.warnings = list(warnings)
            if len(exported_gallery_files) < len(gallery_assets):
                job.status = "PARTIAL"
            else:
                job.status = "COMPLETED"

            # Stage 10: Generate Manifest JSON & Benchmark Metrics
            t0 = time.time()
            manifest_writer = ManifestWriter(self.storage_provider)
            manifest_file_path = manifest_writer.write_manifest(
                job_output_dir=job_output_dir,
                job_id=job_id,
                job_status=job.status,
                brand_cfg=brand_cfg,
                vehicle_data=vehicle_data,
                pipeline_cfg=pipeline_cfg,
                cover_selection=cover_selection,
                valid_assets=valid_assets,
                quality_map=quality_map_legacy,
                class_map=class_map_legacy,
                dup_groups=dup_groups,
                dup_removed=dup_removed,
                coverage=coverage,
                warnings=warnings
            )

            job.successful_images = successful_count
            job.processed_images = successful_count
            job.failed_images = job.total_images - successful_count

            total_in = sum(getattr(a, "file_size_bytes", 0) for a in valid_assets)
            total_out = self._compute_folder_size(job_output_dir)

            benchmark_metric_data = benchmark.finish_measurement(
                total_images=job.total_images,
                processed_images=job.processed_images,
                failed_images=job.failed_images,
                total_input_bytes=total_in,
                total_output_bytes=total_out
            )

            benchmark_file_path = benchmark.write_benchmark(job_output_dir, benchmark_metric_data)
            benchmark.record_stage("manifest_generation", time.time() - t0)

            # Stage 11: Package ZIP Archive
            t0 = time.time()
            zip_filename = f"{job_id}.zip"
            zip_output_path = os.path.join(output_dir, zip_filename)
            job_zip_path = os.path.join(job_output_dir, "vehicle_media_package.zip")

            try:
                self.storage_provider.create_zip_archive(job_output_dir, zip_output_path)
                self.storage_provider.create_zip_archive(job_output_dir, job_zip_path)
            except Exception as e:
                raise ExportError(f"ZIP packaging failed: {str(e)}")

            benchmark.record_stage("zip_packaging", time.time() - t0)
            job.ended_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

            res = ProcessingResult(
                job_id=job_id,
                success=True,
                cover_file=final_cover_path,
                gallery_files=[os.path.join(photos_output_dir, f) for f in exported_gallery_files],
                text_title_file=title_file_path,
                text_desc_file=desc_file_path,
                manifest_file=manifest_file_path,
                benchmark_file=benchmark_file_path,
                warnings=warnings,
                errors=errors
            )
            return job, res

        except Exception as e:
            job.status = "FAILED"
            job.ended_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
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
