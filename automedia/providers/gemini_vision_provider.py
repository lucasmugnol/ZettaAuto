"""Gemini Multimodal Vision Provider with heuristic fallback and local caching."""

import os
import json
import time
import base64
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, Tuple

from PIL import Image

from automedia.core.interfaces import IMultimodalVisionProvider
from automedia.core.models import ImageAsset, PhotoCategory, MacroCategory
from automedia.core.vision_models import MultimodalAnalysisResult
from automedia.core.vision_schemas import AUTOMEDIA_VISION_PROMPT_V1, parse_and_validate_vision_json
from automedia.providers.local_photo_analyzer import LocalPhotoAnalyzer
from automedia.providers.local_photo_classifier import LocalPhotoClassifier
from automedia.providers.vision_cache_provider import VisionCacheProvider


class GeminiVisionProvider(IMultimodalVisionProvider):
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.mode = self.config.get("mode", "multimodal")
        self.model = self.config.get("model", "gemini-2.5-flash")
        self.timeout_seconds = self.config.get("timeout_seconds", 30)
        self.min_confidence = self.config.get("min_confidence", 0.70)
        self.fallback_to_heuristic = self.config.get("fallback_to_heuristic", True)
        self.cache_enabled = self.config.get("cache_enabled", True)
        self.prompt_version = self.config.get("prompt_version", "v1.0.0")

        self.analyzer = LocalPhotoAnalyzer()
        self.classifier = LocalPhotoClassifier()
        self.cache = VisionCacheProvider() if self.cache_enabled else None

    def analyze_image(
        self, image_path: str, asset: ImageAsset
    ) -> MultimodalAnalysisResult:
        t0 = time.time()

        # 1. Mode = "heuristic" override (offline / privacy mode)
        if self.mode == "heuristic":
            return self._heuristic_fallback(
                image_path, asset, t0, "Mode configured as 'heuristic'"
            )

        # 2. Check local SHA256 cache
        if self.cache:
            cached_data = self.cache.get(image_path, "gemini", self.model, self.prompt_version)
            if cached_data:
                cached_res = self._dict_to_result(cached_data)
                cached_res.inference_status = "CACHE_HIT"
                cached_res.latency_ms = round((time.time() - t0) * 1000.0, 2)
                return cached_res

        # 3. Check API Key (Load .env automatically if present)
        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        if not api_key and os.path.exists(".env"):
            try:
                with open(".env", "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("GEMINI_API_KEY="):
                            api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                            os.environ["GEMINI_API_KEY"] = api_key
                            break
            except Exception:
                pass

        if not api_key:
            if self.fallback_to_heuristic:
                return self._heuristic_fallback(
                    image_path, asset, t0, "GEMINI_API_KEY environment variable not found"
                )
            raise ValueError("GEMINI_API_KEY not set and fallback_to_heuristic is False")

        # 4. Multimodal API Inference
        try:
            raw_text, latency_ms = self._call_gemini_api(image_path, api_key)
            img_w, img_h = (asset.width, asset.height)

            validated_data, err_msg = parse_and_validate_vision_json(raw_text, img_w, img_h)

            if err_msg or not validated_data:
                if self.fallback_to_heuristic:
                    return self._heuristic_fallback(
                        image_path, asset, t0, f"Schema validation failed: {err_msg}"
                    )
                raise ValueError(f"Schema validation failed: {err_msg}")

            conf = validated_data.get("confidence", 0.0)
            if conf < self.min_confidence:
                if self.fallback_to_heuristic:
                    return self._heuristic_fallback(
                        image_path, asset, t0, f"Confidence {conf:.2f} below min threshold {self.min_confidence}"
                    )

            res = self._dict_to_result(validated_data)
            res.provider_used = "gemini"
            res.model_used = self.model
            res.prompt_version = self.prompt_version
            res.inference_status = "SUCCESS"
            res.fallback_used = False
            res.latency_ms = round(latency_ms, 2)
            res.estimated_cost_usd = 0.0001  # Token cost estimate

            # Save to cache
            if self.cache:
                self.cache.set(
                    image_path, "gemini", self.model, self.prompt_version, res.to_dict()
                )

            return res

        except Exception as e:
            # Obfuscate any potential API key leakage in exception messages
            clean_err = str(e).replace(api_key, "[REDACTED_API_KEY]")
            if self.fallback_to_heuristic:
                return self._heuristic_fallback(
                    image_path, asset, t0, f"API inference error: {clean_err}"
                )
            raise RuntimeError(f"Gemini vision inference failed: {clean_err}")

    def _call_gemini_api(self, image_path: str, api_key: str) -> Tuple[str, float]:
        t0 = time.time()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={api_key}"

        with open(image_path, "rb") as f:
            b64_data = base64.b64encode(f.read()).decode("utf-8")

        # Determine MIME type
        ext = os.path.splitext(image_path)[1].lower()
        mime_type = "image/jpeg"
        if ext in (".png",):
            mime_type = "image/png"
        elif ext in (".webp",):
            mime_type = "image/webp"

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": AUTOMEDIA_VISION_PROMPT_V1},
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": b64_data
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "response_mime_type": "application/json"
            }
        }

        json_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, data=json_bytes, headers={"Content-Type": "application/json"}
        )

        with urllib.request.urlopen(req, timeout=self.timeout_seconds) as resp:
            resp_body = resp.read().decode("utf-8")

        latency_ms = (time.time() - t0) * 1000.0
        resp_json = json.loads(resp_body)

        # Extract text from response candidates
        try:
            raw_text = resp_json["candidates"][0]["content"]["parts"][0]["text"]
            return raw_text, latency_ms
        except Exception as e:
            raise ValueError(f"Unexpected response structure from Gemini API: {str(e)}")

    def _heuristic_fallback(
        self, image_path: str, asset: ImageAsset, t0: float, reason: str
    ) -> MultimodalAnalysisResult:
        detailed_q = self.analyzer.analyze_quality(image_path, asset)
        classification = self.classifier.classify_photo(image_path, asset, detailed_q)

        cat = classification.category
        macro = classification.macro_category or MacroCategory.get_macro(cat)

        suitable = (cat in (PhotoCategory.FRONT_3_4, PhotoCategory.FRONT, PhotoCategory.REAR_3_4, PhotoCategory.LEFT_SIDE, PhotoCategory.RIGHT_SIDE))
        c_score = 80.0 if cat == PhotoCategory.FRONT_3_4 else (70.0 if cat == PhotoCategory.FRONT else 50.0)

        latency_ms = (time.time() - t0) * 1000.0

        return MultimodalAnalysisResult(
            category=cat,
            macro_category=macro,
            confidence=classification.confidence,
            suitable_for_cover=suitable,
            cover_score=c_score,
            quality_status=detailed_q.status,
            visual_issues=detailed_q.quality_issues,
            composition_score=detailed_q.composition_score,
            framing_score=detailed_q.orientation_score,
            vehicle_visibility=0.85,
            content_bbox_estimate=None,
            plate_visible=False,
            plate_bbox=None,
            reasoning_summary=f"Heuristic fallback analysis ({classification.reason})",
            provider_used="heuristic",
            model_used="local_photo_classifier",
            prompt_version=self.prompt_version,
            inference_status="FALLBACK_HEURISTIC",
            fallback_used=True,
            fallback_reason=reason,
            latency_ms=round(latency_ms, 2),
            estimated_cost_usd=0.0
        )

    def _dict_to_result(self, d: Dict[str, Any]) -> MultimodalAnalysisResult:
        meta = d.get("metadata", {})
        return MultimodalAnalysisResult(
            category=d.get("category", PhotoCategory.UNKNOWN),
            macro_category=d.get("macro_category", MacroCategory.UNKNOWN),
            confidence=float(d.get("confidence", 0.5)),
            suitable_for_cover=bool(d.get("suitable_for_cover", False)),
            cover_score=float(d.get("cover_score", 0.0)),
            quality_status=d.get("quality_status", "GOOD"),
            visual_issues=d.get("visual_issues", []),
            composition_score=float(d.get("composition_score", 50.0)),
            framing_score=float(d.get("framing_score", 50.0)),
            vehicle_visibility=float(d.get("vehicle_visibility", 0.8)),
            content_bbox_estimate=d.get("content_bbox_estimate"),
            plate_visible=bool(d.get("plate_visible", False)),
            plate_bbox=d.get("plate_bbox"),
            reasoning_summary=d.get("reasoning_summary", ""),
            provider_used=meta.get("provider_used", "gemini"),
            model_used=meta.get("model_used", self.model),
            prompt_version=meta.get("prompt_version", self.prompt_version),
            inference_status=meta.get("inference_status", "SUCCESS"),
            fallback_used=bool(meta.get("fallback_used", False)),
            fallback_reason=meta.get("fallback_reason"),
            latency_ms=float(meta.get("latency_ms", 0.0)),
            estimated_cost_usd=float(meta.get("estimated_cost_usd", 0.0))
        )
