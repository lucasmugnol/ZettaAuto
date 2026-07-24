"""Independent Heuristic Vision Provider (Sprint 2.3 Refactoring).

Processes vehicle photographs locally using rules, edge detection, color histograms, and heuristics.
Completely decoupled from Gemini and external network APIs.
"""

import time
from typing import Optional, Dict, Any

from automedia.core.interfaces import IMultimodalVisionProvider
from automedia.core.models import (
    ImageAsset, PhotoCategory, MacroCategory, VisionAnalysisResult
)
from automedia.providers.local_photo_analyzer import LocalPhotoAnalyzer
from automedia.providers.local_photo_classifier import LocalPhotoClassifier


class HeuristicVisionProvider(IMultimodalVisionProvider):
    """Concrete local vision provider based strictly on rules and heuristics."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.analyzer = LocalPhotoAnalyzer()
        self.classifier = LocalPhotoClassifier()

    def analyze_image(
        self, image_path: str, asset: ImageAsset
    ) -> VisionAnalysisResult:
        t0 = time.time()

        detailed_q = self.analyzer.analyze_quality(image_path, asset)
        classification = self.classifier.classify_photo(image_path, asset, detailed_q)

        cat = classification.category
        macro = classification.macro_category or MacroCategory.get_macro(cat)

        suitable = (cat in (
            PhotoCategory.FRONT_3_4, PhotoCategory.FRONT, PhotoCategory.REAR_3_4,
            PhotoCategory.LEFT_SIDE, PhotoCategory.RIGHT_SIDE, PhotoCategory.REAR
        ))
        
        # Calculate cover score from quality & category weight
        c_score = detailed_q.overall_score
        if cat == PhotoCategory.FRONT_3_4:
            c_score += 40.0
        elif cat == PhotoCategory.FRONT:
            c_score += 35.0
        elif cat in (PhotoCategory.REAR_3_4, PhotoCategory.LEFT_SIDE, PhotoCategory.RIGHT_SIDE):
            c_score += 20.0
        elif cat == PhotoCategory.REAR:
            c_score += 15.0
        else:
            c_score -= 50.0

        c_score = max(0.0, min(100.0, c_score))
        latency_ms = (time.time() - t0) * 1000.0

        return VisionAnalysisResult(
            filename=asset.filename,
            category=cat,
            macro_category=macro,
            quality_score=detailed_q.overall_score,
            suitable_for_cover=suitable,
            cover_score=round(c_score, 2),
            duplicate_flag=False,
            confidence=classification.confidence,
            plate_visible=False,
            plate_bbox=None,
            reasoning=f"Local heuristic classification ({classification.reason})",
            provider_used="heuristic",
            model_used="local_photo_classifier",
            latency_ms=round(latency_ms, 2),
            estimated_cost_usd=0.0,
            is_cost_estimated=False
        )
