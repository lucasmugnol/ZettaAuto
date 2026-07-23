"""Cover Selector module for intelligent automatic cover photo selection."""

from typing import List, Dict, Optional, Tuple
from automedia.core.models import (
    ImageAsset, VehicleData, PhotoQualityScore, PhotoClassificationResult,
    PhotoCategory, CoverSelectionResult
)


class CoverSelector:
    CATEGORY_WEIGHTS = {
        PhotoCategory.FRONT_3_4: 40.0,
        PhotoCategory.FRONT: 35.0,
        PhotoCategory.REAR_3_4: 25.0,
        PhotoCategory.LEFT_SIDE: 20.0,
        PhotoCategory.RIGHT_SIDE: 20.0,
        PhotoCategory.REAR: 15.0,
        PhotoCategory.INTERIOR_FRONT: -35.0,
        PhotoCategory.INTERIOR_REAR: -40.0,
        PhotoCategory.DASHBOARD: -45.0,
        PhotoCategory.STEERING: -45.0,
        PhotoCategory.TRUNK: -60.0,
        PhotoCategory.ENGINE: -60.0,
        PhotoCategory.WHEEL: -60.0,
        PhotoCategory.KEY: -80.0,
        PhotoCategory.DOCUMENT: -100.0,
        PhotoCategory.UNKNOWN: 0.0
    }

    def select_cover(
        self,
        assets: List[ImageAsset],
        quality_map: Dict[str, PhotoQualityScore],
        class_map: Dict[str, PhotoClassificationResult],
        duplicate_removed: List[str],
        vehicle_data: VehicleData
    ) -> CoverSelectionResult:
        valid_assets = [a for a in assets if a.is_valid]
        if not valid_assets:
            raise ValueError("No valid image assets available for cover selection.")

        # Check explicit override in vehicle_data
        if vehicle_data and vehicle_data.cover_image:
            target = vehicle_data.cover_image.lower()
            match = next((a for a in valid_assets if a.filename.lower() == target), None)
            if match:
                return CoverSelectionResult(
                    selected_file=match.filename,
                    score=100.0,
                    rank=1,
                    reason="Explicit user override in vehicle configuration (cover_image)",
                    ranking_candidates=[{
                        "file": match.filename,
                        "total_rank_score": 100.0,
                        "category": class_map[match.filename].category if match.filename in class_map else PhotoCategory.UNKNOWN,
                        "overall_quality": quality_map[match.filename].overall_score if match.filename in quality_map else 0.0
                    }]
                )

        # Automatic ranking
        candidates = []
        for asset in valid_assets:
            fname = asset.filename
            q_score = quality_map.get(fname, PhotoQualityScore())
            cls_res = class_map.get(fname, PhotoClassificationResult())

            cat_weight = self.CATEGORY_WEIGHTS.get(cls_res.category, 0.0)
            total_rank = q_score.overall_score + cat_weight

            # Penalties
            if fname in duplicate_removed:
                total_rank -= 40.0
            if q_score.status == "BAD":
                total_rank -= 30.0
            elif q_score.status == "WARNING":
                total_rank -= 15.0
            if asset.orientation == "portrait":
                total_rank -= 15.0

            candidates.append({
                "file": fname,
                "total_rank_score": round(total_rank, 2),
                "category": cls_res.category,
                "overall_quality": q_score.overall_score,
                "is_duplicate_removed": fname in duplicate_removed,
                "status": q_score.status
            })

        candidates_sorted = sorted(candidates, key=lambda c: c["total_rank_score"], reverse=True)
        for rank_idx, c in enumerate(candidates_sorted, start=1):
            c["rank"] = rank_idx

        top_choice = candidates_sorted[0]
        reason = (
            f"Selected automatically as rank #1 ({top_choice['category']} view, "
            f"quality score {top_choice['overall_quality']}/100, rank score {top_choice['total_rank_score']})"
        )

        return CoverSelectionResult(
            selected_file=top_choice["file"],
            score=top_choice["total_rank_score"],
            rank=1,
            reason=reason,
            ranking_candidates=candidates_sorted
        )
