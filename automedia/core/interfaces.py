"""Abstract provider interfaces (Ports) for the AutoMedia AI pipeline."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple, Optional
from automedia.core.models import (
    ImageAsset, VehicleData, BrandConfig, PipelineConfig, VisionAnalysis, PlateRegion
)


class IVisionProvider(ABC):
    """Port for vision & image semantic analysis."""

    @abstractmethod
    def analyze_batch(
        self, images: List[ImageAsset], vehicle_data: VehicleData
    ) -> List[VisionAnalysis]:
        """Analyze a batch of images and return vision analysis metadata for each."""
        pass


class IImageProvider(ABC):
    """Port for image processing, color correction, plate coverage and layout composition."""

    @abstractmethod
    def process_and_adjust(
        self,
        image_path: str,
        output_path: str,
        target_dimensions: Tuple[int, int],
        adjustment_intensity: float,
        quality: int = 90
    ) -> bool:
        """Apply moderate color/light adjustments and resize/crop to target dimensions."""
        pass

    @abstractmethod
    def apply_plate_cover(
        self,
        image_path: str,
        output_path: str,
        plate_regions: List[PlateRegion],
        strategy: str,
        primary_color_hex: str = "#1E3A8A",
        quality: int = 90
    ) -> bool:
        """Apply blur or solid cover on specified plate regions."""
        pass

    @abstractmethod
    def apply_watermark(
        self,
        image_path: str,
        output_path: str,
        logo_path: Optional[str],
        watermark_policy: Dict[str, Any],
        opacity: float = 0.35,
        quality: int = 90
    ) -> bool:
        """Apply discrete watermark to a secondary gallery photo."""
        pass

    @abstractmethod
    def compose_cover(
        self,
        main_image_path: str,
        output_path: str,
        brand_config: BrandConfig,
        vehicle_data: VehicleData,
        target_dimensions: Tuple[int, int],
        quality: int = 90,
        cover_fit_strategy: str = "contain",
        bg_fill_strategy: str = "blurred"
    ) -> bool:
        """Compose the primary cover image with brand layout and vehicle data."""
        pass


class ITextProvider(ABC):
    """Port for text generation."""

    @abstractmethod
    def generate_ad_text(
        self, vehicle_data: VehicleData, brand_config: BrandConfig
    ) -> Tuple[str, str]:
        """Generate (title, description) tuple without hallucinating data."""
        pass


class IStorageProvider(ABC):
    """Port for storage operations."""

    @abstractmethod
    def create_job_directory(self, base_output_path: str, job_id: str) -> str:
        """Create job-specific output directory."""
        pass

    @abstractmethod
    def save_file(self, destination_path: str, content: bytes) -> str:
        """Save raw bytes to destination path."""
        pass

    @abstractmethod
    def create_zip_archive(self, folder_path: str, zip_output_path: str) -> str:
        """Package a folder into a ZIP archive."""
        pass
