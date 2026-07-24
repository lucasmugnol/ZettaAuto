"""Factory for creating vision providers according to pipeline configuration."""

import os
from typing import Dict, Any, Optional
from automedia.config_loader import load_dotenv
from automedia.core.interfaces import IMultimodalVisionProvider
from automedia.providers.gemini_vision_provider import GeminiVisionProvider


class VisionProviderFactory:
    @staticmethod
    def create_provider(
        config: Optional[Dict[str, Any]] = None
    ) -> IMultimodalVisionProvider:
        load_dotenv()
        cfg = config or {}

        # Allow environment variable override if specified
        env_provider = os.environ.get("VISION_PROVIDER")
        provider_type = (env_provider or cfg.get("provider", cfg.get("mode", "gemini"))).lower()

        if provider_type in ("gemini", "multimodal"):
            gemini_cfg = {**cfg, "provider": "gemini", "mode": "multimodal"}
            return GeminiVisionProvider(gemini_cfg)
        elif provider_type in ("heuristic", "local"):
            heuristic_cfg = {**cfg, "provider": "heuristic", "mode": "heuristic"}
            return GeminiVisionProvider(heuristic_cfg)
        else:
            raise ValueError(f"Unsupported Vision Provider type: '{provider_type}'")
