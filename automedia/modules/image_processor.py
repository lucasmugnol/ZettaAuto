"""Image Processor module wrapping image provider operations."""

from typing import List, Tuple
from automedia.core.interfaces import IImageProvider
from automedia.core.models import ImageAsset, PipelineConfig, VisionAnalysis, PlateRegion


class ImageProcessor:
    def __init__(self, provider: IImageProvider, pipeline_config: PipelineConfig):
        self.provider = provider
        self.config = pipeline_config

    def process_image(
        self, asset: ImageAsset, temp_output_path: str, target_dimensions: Tuple[int, int]
    ) -> bool:
        return self.provider.process_and_adjust(
            image_path=asset.path,
            output_path=temp_output_path,
            target_dimensions=target_dimensions,
            adjustment_intensity=self.config.adjustment_intensity,
            quality=self.config.export_quality
        )

    def apply_plate_cover(
        self, image_path: str, output_path: str, plate_regions: List[PlateRegion], primary_color: str
    ) -> bool:
        return self.provider.apply_plate_cover(
            image_path=image_path,
            output_path=output_path,
            plate_regions=plate_regions,
            strategy=self.config.plate_cover_strategy,
            primary_color_hex=primary_color,
            quality=self.config.export_quality
        )
