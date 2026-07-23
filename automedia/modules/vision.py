"""Vision module wrapping the vision provider."""

from typing import List
from automedia.core.interfaces import IVisionProvider
from automedia.core.models import ImageAsset, VehicleData, VisionAnalysis


class VisionModule:
    def __init__(self, provider: IVisionProvider):
        self.provider = provider

    def analyze(self, images: List[ImageAsset], vehicle_data: VehicleData) -> List[VisionAnalysis]:
        return self.provider.analyze_batch(images, vehicle_data)
