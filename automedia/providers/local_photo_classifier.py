"""Local Photo Classifier implementation using heuristics and metadata."""

import os
from typing import Optional
from PIL import Image, ImageStat
from automedia.core.interfaces import IPhotoClassifier
from automedia.core.models import ImageAsset, PhotoCategory, PhotoClassificationResult, PhotoQualityScore


class LocalPhotoClassifier(IPhotoClassifier):
    def classify_photo(
        self, image_path: str, asset: ImageAsset, quality_score: Optional[PhotoQualityScore] = None
    ) -> PhotoClassificationResult:
        fname = asset.filename.lower()

        # 1. Filename keyword rules (high confidence)
        filename_map = [
            (["front_3_4", "frente_3_4", "frente34", "front34"], PhotoCategory.FRONT_3_4, 0.95, "Filename matches front 3/4"),
            (["rear_3_4", "traseira_3_4", "traseira34", "rear34"], PhotoCategory.REAR_3_4, 0.95, "Filename matches rear 3/4"),
            (["front", "frente", "car_front"], PhotoCategory.FRONT, 0.90, "Filename matches front"),
            (["rear", "traseira", "tras"], PhotoCategory.REAR, 0.90, "Filename matches rear"),
            (["left_side", "lado_esquerdo", "lateral_esquerda"], PhotoCategory.LEFT_SIDE, 0.90, "Filename matches left side"),
            (["right_side", "lado_direito", "lateral_direita"], PhotoCategory.RIGHT_SIDE, 0.90, "Filename matches right side"),
            (["side", "lateral"], PhotoCategory.LEFT_SIDE, 0.85, "Filename matches side view"),
            (["dashboard", "painel"], PhotoCategory.DASHBOARD, 0.90, "Filename matches dashboard"),
            (["steering", "volante"], PhotoCategory.STEERING, 0.90, "Filename matches steering wheel"),
            (["interior_front", "interior_frente"], PhotoCategory.INTERIOR_FRONT, 0.90, "Filename matches front interior"),
            (["interior_rear", "interior_traseiro", "banco_traseiro"], PhotoCategory.INTERIOR_REAR, 0.90, "Filename matches rear interior"),
            (["interior", "banco", "couro"], PhotoCategory.INTERIOR_FRONT, 0.85, "Filename matches interior"),
            (["trunk", "porta_malas", "portamalas"], PhotoCategory.TRUNK, 0.90, "Filename matches trunk"),
            (["engine", "motor"], PhotoCategory.ENGINE, 0.90, "Filename matches engine"),
            (["wheel", "roda", "pneu"], PhotoCategory.WHEEL, 0.90, "Filename matches wheel"),
            (["key", "chave"], PhotoCategory.KEY, 0.90, "Filename matches key"),
            (["doc", "documento", "cautelar", "laudo"], PhotoCategory.DOCUMENT, 0.95, "Filename matches document"),
        ]

        for keywords, category, conf, reason in filename_map:
            if any(kw in fname for kw in keywords):
                return PhotoClassificationResult(category=category, confidence=conf, reason=reason)

        # 2. Visual heuristics when filename is generic (e.g. photo_01.jpg, img001.jpg)
        try:
            with Image.open(image_path) as img:
                w, h = img.size
                aspect = w / float(h)
                gray = img.convert("L")
                stat = ImageStat.Stat(gray)
                mean_b = stat.mean[0]

                # Square image with low/dark corners often indicates wheel or detail
                if 0.9 <= aspect <= 1.1 and w < 1000:
                    return PhotoClassificationResult(
                        category=PhotoCategory.WHEEL,
                        confidence=0.60,
                        reason="Visual heuristic: square close-up aspect ratio"
                    )

                # Dark interior profile with horizontal landscape orientation
                if mean_b < 85 and aspect > 1.3:
                    return PhotoClassificationResult(
                        category=PhotoCategory.INTERIOR_FRONT,
                        confidence=0.65,
                        reason="Visual heuristic: interior cabin lighting profile"
                    )

                # Standard landscape photo with balanced brightness is assumed exterior
                if aspect >= 1.2:
                    return PhotoClassificationResult(
                        category=PhotoCategory.FRONT_3_4,
                        confidence=0.70,
                        reason="Visual heuristic: landscape exterior vehicle photo"
                    )
        except Exception:
            pass

        return PhotoClassificationResult(
            category=PhotoCategory.UNKNOWN,
            confidence=0.40,
            reason="Default category fallback"
        )
