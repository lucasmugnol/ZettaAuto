"""Core dataclass models for the AutoMedia AI pipeline."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class PlateRegion:
    file: str
    x: int
    y: int
    width: int
    height: int
    source: str = "manual"  # "manual", "auto", "not_found"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file": self.file,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "source": self.source
        }


@dataclass
class ImageAsset:
    path: str
    filename: str
    file_hash: str = ""
    width: int = 0
    height: int = 0
    file_size_bytes: int = 0
    mime_type: str = ""
    orientation: str = "landscape"  # "landscape", "portrait", "square"
    is_valid: bool = True
    error_message: Optional[str] = None
    is_duplicate: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "filename": self.filename,
            "path": self.path,
            "file_hash": self.file_hash,
            "width": self.width,
            "height": self.height,
            "file_size_bytes": self.file_size_bytes,
            "mime_type": self.mime_type,
            "orientation": self.orientation,
            "is_valid": self.is_valid,
            "is_duplicate": self.is_duplicate,
            "error_message": self.error_message
        }


@dataclass
class VehicleData:
    manufacturer: str
    model: str
    year: Any
    price: Any
    description: Optional[str] = None
    optional_features: List[str] = field(default_factory=list)
    cover_image: Optional[str] = None
    plate_regions: List[PlateRegion] = field(default_factory=list)

@dataclass
class BrandConfig:
    company_name: str
    primary_color: str = "#1E3A8A"
    secondary_color: str = "#F97316"
    text_color: str = "#FFFFFF"
    logo_path: Optional[str] = None
    watermark_opacity: float = 0.35
    contact: str = ""
    cta: str = ""


@dataclass
class PipelineConfig:
    accepted_formats: List[str] = field(default_factory=lambda: [".jpg", ".jpeg", ".png", ".webp"])
    export_quality: int = 90
    cover_dimensions: Dict[str, int] = field(default_factory=lambda: {"width": 1080, "height": 1080})
    secondary_dimensions: Dict[str, int] = field(default_factory=lambda: {"width": 1080, "height": 1080})
    adjustment_intensity: float = 0.1
    plate_cover_strategy: str = "solid_cover"  # "solid_cover", "blur"
    watermark_policy: Dict[str, Any] = field(default_factory=lambda: {
        "position": "bottom_right",
        "margin_pixels": 25,
        "scale_ratio": 0.18
    })
    min_width: int = 300
    min_height: int = 300
    max_file_size_mb: float = 25.0
    ttl_hours: int = 24


@dataclass
class VisionAnalysis:
    file: str
    vehicle_bbox: Dict[str, int] = field(default_factory=lambda: {"x": 0, "y": 0, "width": 0, "height": 0})
    plate_regions: List[PlateRegion] = field(default_factory=list)
    quality_score: float = 0.0
    sharpness_score: float = 0.0
    brightness_score: float = 0.0
    contrast_score: float = 0.0
    recommended_as_cover: bool = False
    low_confidence: bool = False
    plate_detection_method: str = "not_found"  # "manual", "auto", "not_found"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file": self.file,
            "vehicle_bbox": self.vehicle_bbox,
            "plate_regions": [p.to_dict() for p in self.plate_regions],
            "quality_score": round(self.quality_score, 2),
            "sharpness_score": round(self.sharpness_score, 2),
            "brightness_score": round(self.brightness_score, 2),
            "contrast_score": round(self.contrast_score, 2),
            "recommended_as_cover": self.recommended_as_cover,
            "low_confidence": self.low_confidence,
            "plate_detection_method": self.plate_detection_method
        }


@dataclass
class StageResult:
    stage_name: str
    success: bool
    duration_seconds: float
    warning: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stage_name": self.stage_name,
            "success": self.success,
            "duration_seconds": round(self.duration_seconds, 4),
            "warning": self.warning,
            "error": self.error
        }


@dataclass
class Job:
    job_id: str
    input_path: str
    output_path: str
    status: str = "DRAFT"  # "DRAFT", "RUNNING", "COMPLETED", "FAILED", "CANCELLED"
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    total_images: int = 0
    successful_images: int = 0
    failed_images: int = 0
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    pipeline_version: str = "1.0.0"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "status": self.status,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "input_path": self.input_path,
            "output_path": self.output_path,
            "total_images": self.total_images,
            "successful_images": self.successful_images,
            "failed_images": self.failed_images,
            "warnings": self.warnings,
            "errors": self.errors,
            "pipeline_version": self.pipeline_version
        }


@dataclass
class BenchmarkResult:
    total_duration_seconds: float
    duration_by_stage: Dict[str, float]
    duration_per_image: Dict[str, float]
    average_duration_per_image: float
    total_images: int
    processed_images: int
    failed_images: int
    initial_memory_mb: Optional[float] = None
    peak_memory_mb: Optional[float] = None
    cpu_usage_percent: Optional[float] = None
    total_input_bytes: int = 0
    total_output_bytes: int = 0
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_duration_seconds": round(self.total_duration_seconds, 4),
            "duration_by_stage": {k: round(v, 4) for k, v in self.duration_by_stage.items()},
            "duration_per_image": {k: round(v, 4) for k, v in self.duration_per_image.items()},
            "average_duration_per_image": round(self.average_duration_per_image, 4),
            "total_images": self.total_images,
            "processed_images": self.processed_images,
            "failed_images": self.failed_images,
            "initial_memory_mb": round(self.initial_memory_mb, 2) if self.initial_memory_mb is not None else None,
            "peak_memory_mb": round(self.peak_memory_mb, 2) if self.peak_memory_mb is not None else None,
            "cpu_usage_percent": round(self.cpu_usage_percent, 2) if self.cpu_usage_percent is not None else None,
            "total_input_bytes": self.total_input_bytes,
            "total_output_bytes": self.total_output_bytes,
            "warnings": self.warnings
        }


@dataclass
class ProcessingResult:
    job_id: str
    success: bool
    cover_file: Optional[str] = None
    gallery_files: List[str] = field(default_factory=list)
    text_title_file: Optional[str] = None
    text_desc_file: Optional[str] = None
    manifest_file: Optional[str] = None
    benchmark_file: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
