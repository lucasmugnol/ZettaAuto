"""Brand Composer module for generating cover and watermarked gallery photos."""

from typing import Tuple
from automedia.core.interfaces import IImageProvider
from automedia.core.models import BrandConfig, VehicleData, PipelineConfig


class BrandComposer:
    def __init__(self, provider: IImageProvider, pipeline_config: PipelineConfig):
        self.provider = provider
        self.config = pipeline_config

    def compose_cover(
        self,
        main_image_path: str,
        output_path: str,
        brand_config: BrandConfig,
        vehicle_data: VehicleData,
        target_dimensions: Tuple[int, int]
    ) -> bool:
        return self.provider.compose_cover(
            main_image_path=main_image_path,
            output_path=output_path,
            brand_config=brand_config,
            vehicle_data=vehicle_data,
            target_dimensions=target_dimensions,
            quality=self.config.export_quality,
            cover_fit_strategy=getattr(self.config, "cover_fit_strategy", "contain"),
            bg_fill_strategy=getattr(self.config, "bg_fill_strategy", "blurred")
        )

    def apply_watermark(
        self, image_path: str, output_path: str, brand_config: BrandConfig
    ) -> bool:
        return self.provider.apply_watermark(
            image_path=image_path,
            output_path=output_path,
            logo_path=brand_config.logo_path,
            watermark_policy=self.config.watermark_policy,
            opacity=brand_config.watermark_opacity,
            quality=self.config.export_quality
        )
