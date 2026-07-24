"""NoOp fallback provider for vehicle detection."""

from automedia.core.interfaces import IVehicleDetectorProvider
from automedia.core.models import ImageAsset, VehicleDetectionResult


class NoOpVehicleDetector(IVehicleDetectorProvider):
    """No-op vehicle detector that gracefully reports no detection."""

    def __init__(self, config: dict = None):
        self.config = config or {}

    def detect_vehicle(
        self, image_path: str, asset: ImageAsset
    ) -> VehicleDetectionResult:
        """Return empty detection result (fallback mode)."""
        width = getattr(asset, "width", 0) if asset else 0
        height = getattr(asset, "height", 0) if asset else 0
        return VehicleDetectionResult(
            detected=False,
            label="",
            confidence=0.0,
            bbox=None,
            image_width=width,
            image_height=height,
            touches_left_edge=False,
            touches_right_edge=False,
            touches_top_edge=False,
            touches_bottom_edge=False,
            possible_crop_risk=False,
            source_already_cropped=False,
            provider="none",
            model="none",
            latency_ms=0.0,
            fallback_used=True,
            error=None
        )
