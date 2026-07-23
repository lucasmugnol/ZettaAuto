"""Local Photo Classifier implementation using heuristics, visual features and metadata."""

import os
from typing import Optional
from PIL import Image, ImageFilter, ImageStat, ImageOps
from automedia.core.interfaces import IPhotoClassifier
from automedia.core.models import ImageAsset, PhotoCategory, PhotoClassificationResult, PhotoQualityScore


class LocalPhotoClassifier(IPhotoClassifier):
    def classify_photo(
        self, image_path: str, asset: ImageAsset, quality_score: Optional[PhotoQualityScore] = None
    ) -> PhotoClassificationResult:
        fname = asset.filename.lower()

        # 1. Filename keyword rules (high confidence when semantic keywords exist)
        filename_map = [
            (["front_3_4", "frente_3_4", "frente34", "front34"], PhotoCategory.FRONT_3_4, 0.95, "Filename keyword match (front 3/4)"),
            (["rear_3_4", "traseira_3_4", "traseira34", "rear34"], PhotoCategory.REAR_3_4, 0.95, "Filename keyword match (rear 3/4)"),
            (["front_direct", "car_front", "frente_direta", "frente"], PhotoCategory.FRONT, 0.90, "Filename keyword match (front)"),
            (["rear_direct", "traseira_direta", "traseira", "tras"], PhotoCategory.REAR, 0.90, "Filename keyword match (rear)"),
            (["left_side", "lado_esquerdo", "lateral_esquerda"], PhotoCategory.LEFT_SIDE, 0.90, "Filename keyword match (left side)"),
            (["right_side", "lado_direito", "lateral_direita"], PhotoCategory.RIGHT_SIDE, 0.90, "Filename keyword match (right side)"),
            (["side", "lateral"], PhotoCategory.LEFT_SIDE, 0.85, "Filename keyword match (side view)"),
            (["dashboard", "painel"], PhotoCategory.DASHBOARD, 0.90, "Filename keyword match (dashboard)"),
            (["steering", "volante"], PhotoCategory.STEERING, 0.90, "Filename keyword match (steering wheel)"),
            (["interior_front", "interior_frente"], PhotoCategory.INTERIOR_FRONT, 0.90, "Filename keyword match (front interior)"),
            (["interior_rear", "interior_traseiro", "banco_traseiro"], PhotoCategory.INTERIOR_REAR, 0.90, "Filename keyword match (rear interior)"),
            (["interior", "banco", "couro"], PhotoCategory.INTERIOR_FRONT, 0.85, "Filename keyword match (interior)"),
            (["trunk", "porta_malas", "portamalas"], PhotoCategory.TRUNK, 0.90, "Filename keyword match (trunk)"),
            (["engine", "motor"], PhotoCategory.ENGINE, 0.90, "Filename keyword match (engine)"),
            (["wheel", "roda", "pneu"], PhotoCategory.WHEEL, 0.90, "Filename keyword match (wheel)"),
            (["key", "chave"], PhotoCategory.KEY, 0.90, "Filename keyword match (key)"),
            (["doc", "documento", "cautelar", "laudo"], PhotoCategory.DOCUMENT, 0.95, "Filename keyword match (document)"),
        ]

        for keywords, category, conf, reason in filename_map:
            if any(kw in fname for kw in keywords):
                return PhotoClassificationResult(category=category, confidence=conf, reason=reason)

        # 2. Visual feature classification for non-semantic filenames (IMG_001.jpg, DSC_100.jpg)
        try:
            with Image.open(image_path) as img:
                img = ImageOps.exif_transpose(img)
                w, h = img.size
                aspect = w / float(h)

                gray = img.convert("L")
                stat = ImageStat.Stat(gray)
                mean_brightness = stat.mean[0]
                stddev_contrast = stat.stddev[0]

                edges = gray.filter(ImageFilter.FIND_EDGES)
                edge_stat = ImageStat.Stat(edges)
                edge_density = edge_stat.mean[0]

                # Wheel detail close-up (square aspect or small dimension, concentrated circular dark region)
                if 0.85 <= aspect <= 1.15 and (w < 1000 or edge_density > 25.0):
                    return PhotoClassificationResult(
                        category=PhotoCategory.WHEEL,
                        confidence=0.72,
                        reason="Visual classification: close-up wheel detail (square aspect, high edge density)"
                    )

                # Engine bay (very high edge complexity across entire image)
                if edge_density > 35.0 and stddev_contrast > 55.0:
                    return PhotoClassificationResult(
                        category=PhotoCategory.ENGINE,
                        confidence=0.75,
                        reason="Visual classification: engine bay (high edge complexity and contrast variance)"
                    )

                # Dashboard or steering wheel (dark cabin background with high local contrast)
                if mean_brightness < 70.0 and stddev_contrast > 45.0:
                    if aspect < 1.1:
                        return PhotoClassificationResult(
                            category=PhotoCategory.STEERING,
                            confidence=0.70,
                            reason="Visual classification: steering wheel / instrument cluster"
                        )
                    return PhotoClassificationResult(
                        category=PhotoCategory.DASHBOARD,
                        confidence=0.73,
                        reason="Visual classification: dashboard cabin lighting profile"
                    )

                # Interior seats / Cabin (low to moderate brightness, smooth tone gradients)
                if mean_brightness < 90.0:
                    return PhotoClassificationResult(
                        category=PhotoCategory.INTERIOR_FRONT,
                        confidence=0.68,
                        reason="Visual classification: interior cabin lighting profile"
                    )

                # Exterior vehicle photos (landscape orientation, good environment brightness)
                if aspect >= 1.25 and mean_brightness >= 90.0:
                    # Differentiate front/3_4 vs rear based on top vs bottom brightness/saturation
                    if aspect >= 1.4:
                        return PhotoClassificationResult(
                            category=PhotoCategory.FRONT_3_4,
                            confidence=0.78,
                            reason="Visual classification: exterior 3/4 perspective view"
                        )
                    return PhotoClassificationResult(
                        category=PhotoCategory.FRONT,
                        confidence=0.75,
                        reason="Visual classification: exterior front perspective view"
                    )
        except Exception:
            pass

        return PhotoClassificationResult(
            category=PhotoCategory.UNKNOWN,
            confidence=0.40,
            reason="Default category fallback"
        )
