"""Factory for creating decoupled vision providers according to pipeline configuration."""

import os
from typing import Dict, Any, Optional
from automedia.config_loader import load_dotenv
from automedia.core.interfaces import IMultimodalVisionProvider
from automedia.providers.gemini_vision_provider import GeminiVisionProvider
from automedia.providers.heuristic_vision_provider import HeuristicVisionProvider


class VisionProviderFactory:
    @staticmethod
    def create_provider(
        config: Optional[Dict[str, Any]] = None
    ) -> IMultimodalVisionProvider:
        load_dotenv()
        cfg = config or {}

        # Check environment variable first, then config
        env_provider = os.environ.get("VISION_PROVIDER")
        provider_type = (env_provider or cfg.get("provider", cfg.get("mode", "gemini"))).lower()

        if provider_type == "gemini":
            return GeminiVisionProvider(cfg)
        elif provider_type in ("heuristic", "local"):
            return HeuristicVisionProvider(cfg)
        else:
            raise ValueError(f"Unsupported Vision Provider type: '{provider_type}'")
