"""Image Processor module wrapping image provider operations and Smart Framing rendering."""

import os
from typing import List, Tuple, Optional
from PIL import Image, ImageOps, ImageEnhance
from automedia.core.interfaces import IImageProvider
from automedia.core.models import ImageAsset, PipelineConfig, PlateRegion
from automedia.modules.smart_framing import FramingPlan


class ImageProcessor:
    def __init__(self, provider: IImageProvider, pipeline_config: PipelineConfig):
        self.provider = provider
        self.config = pipeline_config

    def process_image(
        self,
        asset: ImageAsset,
        temp_output_path: str,
        target_dimensions: Tuple[int, int],
        framing_plan: Optional[FramingPlan] = None
    ) -> bool:
        """Process image applying Smart Framing crop if present and strategy is smart_contain."""
        if framing_plan and framing_plan.fit_strategy == "smart_contain":
            return self._process_smart_framing(asset, temp_output_path, target_dimensions, framing_plan)

        return self.provider.process_and_adjust(
            image_path=asset.path,
            output_path=temp_output_path,
            target_dimensions=target_dimensions,
            adjustment_intensity=self.config.adjustment_intensity,
            quality=self.config.export_quality
        )

    def _process_smart_framing(
        self,
        asset: ImageAsset,
        temp_output_path: str,
        target_dimensions: Tuple[int, int],
        framing_plan: FramingPlan
    ) -> bool:
        """Render cropped vehicle sub-image centered on canvas preserving bounding box."""
        with Image.open(asset.path) as img:
            img = ImageOps.exif_transpose(img)
            if img.mode != "RGB":
                img = img.convert("RGB")

            # Crop sub-image according to framing_plan.crop_box [x1, y1, x2, y2]
            c_x1, c_y1, c_x2, c_y2 = map(int, framing_plan.crop_box)
            img_w, img_h = img.size

            c_x1 = max(0, min(c_x1, img_w - 1))
            c_y1 = max(0, min(c_y1, img_h - 1))
            c_x2 = max(c_x1 + 1, min(c_x2, img_w))
            c_y2 = max(c_y1 + 1, min(c_y2, img_h))

            cropped = img.crop((c_x1, c_y1, c_x2, c_y2))

            target_w, target_h = target_dimensions
            crop_w, crop_h = cropped.size

            # Scale to fit inside target_dimensions maintaining aspect ratio
            scale = min(target_w / float(crop_w), target_h / float(crop_h))
            new_w = max(1, int(crop_w * scale))
            new_h = max(1, int(crop_h * scale))

            resized = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)

            # Create clean background canvas and paste centered
            canvas = Image.new("RGB", target_dimensions, color=(240, 240, 240))
            paste_x = (target_w - new_w) // 2
            paste_y = (target_h - new_h) // 2
            canvas.paste(resized, (paste_x, paste_y))

            if self.config.adjustment_intensity > 0:
                enhancer = ImageEnhance.Contrast(canvas)
                canvas = enhancer.enhance(1.0 + (self.config.adjustment_intensity * 0.5))

            os.makedirs(os.path.dirname(temp_output_path), exist_ok=True)
            canvas.save(temp_output_path, quality=self.config.export_quality)
            return True

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
