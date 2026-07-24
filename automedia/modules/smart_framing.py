"""Smart Framing Engine for AutoMedia AI.

Calculates non-destructive vehicle framing plans using object detection bounding boxes,
preserving the entire vehicle, applying safety margins, centering, and padding background.
"""

from dataclasses import dataclass
from typing import Tuple, Optional
from PIL import Image

from automedia.core.models import VehicleDetectionResult, VehicleBoundingBox


@dataclass
class FramingPlan:
    """Plan detailing how an image should be framed for cover composition."""
    crop_box: Tuple[int, int, int, int] # (x1, y1, x2, y2) in source image pixels
    target_dimensions: Tuple[int, int]  # (width, height)
    margin_percent: float = 8.0
    fit_strategy: str = "smart_contain" # "smart_contain" or "contain"
    bg_fill_required: bool = True
    aspect_ratio_preserved: bool = True
    possible_crop_risk: bool = False
    source_already_cropped: bool = False


class SmartFramingEngine:
    """Engine responsible for computing intelligent framing bounds."""

    def __init__(self, safety_margin_percent: float = 8.0):
        self.safety_margin_percent = safety_margin_percent

    def calculate_plan(
        self,
        image_size: Tuple[int, int],
        detection_result: Optional[VehicleDetectionResult],
        target_dimensions: Tuple[int, int]
    ) -> FramingPlan:
        """Calculate non-destructive framing plan."""
        img_w, img_h = image_size
        target_w, target_h = target_dimensions
        target_ar = target_w / target_h if target_h > 0 else 16.0 / 9.0

        # Fallback to standard contain if no valid detection box
        if (
            detection_result is None
            or not detection_result.detected
            or detection_result.bbox is None
        ):
            return FramingPlan(
                crop_box=(0, 0, img_w, img_h),
                target_dimensions=target_dimensions,
                margin_percent=0.0,
                fit_strategy="contain",
                bg_fill_required=True,
                aspect_ratio_preserved=True,
                possible_crop_risk=False,
                source_already_cropped=False
            )

        bbox = detection_result.bbox
        # Add safety margin around vehicle bounding box
        margin_w = bbox.width * (self.safety_margin_percent / 100.0)
        margin_h = bbox.height * (self.safety_margin_percent / 100.0)

        v_x1 = max(0.0, bbox.x1 - margin_w)
        v_y1 = max(0.0, bbox.y1 - margin_h)
        v_x2 = min(float(img_w), bbox.x2 + margin_w)
        v_y2 = min(float(img_h), bbox.y2 + margin_h)

        v_w = max(1.0, v_x2 - v_x1)
        v_h = max(1.0, v_y2 - v_y1)
        v_ar = v_w / v_h

        # Expand box to match target aspect ratio around vehicle center
        center_x = (v_x1 + v_x2) / 2.0
        center_y = (v_y1 + v_y2) / 2.0

        if v_ar < target_ar:
            # Vehicle box is taller than target ratio -> expand width
            desired_w = v_h * target_ar
            crop_x1 = center_x - desired_w / 2.0
            crop_x2 = center_x + desired_w / 2.0
            crop_y1 = v_y1
            crop_y2 = v_y2
        else:
            # Vehicle box is wider than target ratio -> expand height
            desired_h = v_w / target_ar
            crop_x1 = v_x1
            crop_x2 = v_x2
            crop_y1 = center_y - desired_h / 2.0
            crop_y2 = center_y + desired_h / 2.0

        # Clamp crop box to image bounds without cutting vehicle bbox
        final_x1 = max(0.0, crop_x1)
        final_y1 = max(0.0, crop_y1)
        final_x2 = min(float(img_w), crop_x2)
        final_y2 = min(float(img_h), crop_y2)

        # Re-verify that vehicle bbox is 100% inside final crop box
        final_x1 = min(final_x1, bbox.x1)
        final_y1 = min(final_y1, bbox.y1)
        final_x2 = max(final_x2, bbox.x2)
        final_y2 = max(final_y2, bbox.y2)

        crop_box = (
            int(round(final_x1)),
            int(round(final_y1)),
            int(round(final_x2)),
            int(round(final_y2))
        )

        bg_fill_required = (
            final_x1 == 0.0 or final_x2 == float(img_w) or
            final_y1 == 0.0 or final_y2 == float(img_h)
        )

        return FramingPlan(
            crop_box=crop_box,
            target_dimensions=target_dimensions,
            margin_percent=self.safety_margin_percent,
            fit_strategy="smart_contain",
            bg_fill_required=bg_fill_required,
            aspect_ratio_preserved=True,
            possible_crop_risk=detection_result.possible_crop_risk,
            source_already_cropped=detection_result.source_already_cropped
        )
