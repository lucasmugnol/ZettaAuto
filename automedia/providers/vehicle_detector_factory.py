"""Factory for instantiating vehicle detector providers."""

from typing import Dict, Any
from automedia.core.interfaces import IVehicleDetectorProvider
from automedia.providers.noop_vehicle_detector import NoOpVehicleDetector
from automedia.providers.grounding_dino_detector import GroundingDinoVehicleDetector


class VehicleDetectorFactory:
    """Factory to build concrete IVehicleDetectorProvider instances."""

    @staticmethod
    def create_detector(config: Dict[str, Any]) -> IVehicleDetectorProvider:
        """Create detector based on config dictionary."""
        provider_type = config.get("provider", "grounding_dino").lower()

        if provider_type in ("none", "noop", "off", "false"):
            return NoOpVehicleDetector(config)

        if provider_type in ("grounding_dino", "groundingdino", "dino"):
            return GroundingDinoVehicleDetector(config)

        raise ValueError(
            f"Provedor de detecção de veículo não suportado: '{provider_type}'. "
            f"Opções válidas: 'grounding_dino', 'none'."
        )
