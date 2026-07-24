"""Single Photo Gemini Vision API Test Script (Sprint 2.3 Hardening Step 4)."""

import os
import sys
import json
import time
from PIL import Image

from automedia.config_loader import load_dotenv, get_vision_provider_startup_status
from automedia.core.models import ImageAsset
from automedia.providers.vision_provider_factory import VisionProviderFactory


def run_single_photo_test(photo_path: str):
    load_dotenv()

    # Step 2 Startup Announcement (never prints API key)
    print(get_vision_provider_startup_status())
    print("-" * 50)

    if not os.path.exists(photo_path):
        print(f"Error: Target photo '{photo_path}' does not exist.")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("CRITICAL ERROR: GEMINI_API_KEY is not set in environment or .env file.")

    # Instantiate via Factory (Step 3) with fallback_to_heuristic=False for strict API verification
    provider_config = {
        "mode": "multimodal",
        "provider": "gemini",
        "model": "gemini-2.5-flash",
        "fallback_to_heuristic": False,
        "cache_enabled": False  # Force real network API call
    }

    vision_provider = VisionProviderFactory.create_provider(provider_config)

    with Image.open(photo_path) as img:
        w, h = img.size

    asset = ImageAsset(path=photo_path, filename=os.path.basename(photo_path), width=w, height=h, is_valid=True)

    t0 = time.time()
    result = vision_provider.analyze_image(photo_path, asset)
    latency_ms = (time.time() - t0) * 1000.0

    # Step 4 Output Format
    test_summary = {
        "provider_requested": "gemini",
        "provider_used": result.provider_used,
        "fallback_used": result.fallback_used,
        "model": result.model_used,
        "latency_ms": round(result.latency_ms or latency_ms, 2),
        "success": (result.inference_status == "SUCCESS"),
        "category": result.category,
        "macro_category": result.macro_category,
        "suitable_for_cover": result.suitable_for_cover,
        "cover_score": result.cover_score,
        "reasoning_summary": result.reasoning_summary
    }

    print(json.dumps(test_summary, indent=2, ensure_ascii=False))

    if result.fallback_used:
        raise RuntimeError("ERROR: Fallback occurred during single photo test!")
    
    return test_summary


if __name__ == "__main__":
    photo_file = os.path.join("validation_real", "vehicle_01_mobi", "images", "IMG_001.jpg")
    run_single_photo_test(photo_file)
