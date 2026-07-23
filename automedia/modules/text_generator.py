"""Text Generator module for creating deterministic title and description."""

from typing import Tuple
from automedia.core.interfaces import ITextProvider
from automedia.core.models import VehicleData, BrandConfig


class TextGenerator:
    def __init__(self, provider: ITextProvider):
        self.provider = provider

    def generate(
        self, vehicle_data: VehicleData, brand_config: BrandConfig
    ) -> Tuple[str, str]:
        return self.provider.generate_ad_text(vehicle_data, brand_config)
