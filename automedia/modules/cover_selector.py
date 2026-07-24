"""Cover Selector module for intelligent automatic cover photo selection."""

from typing import List, Dict, Optional, Tuple
from automedia.core.models import (
    ImageAsset, VehicleData, PhotoQualityScore, PhotoClassificationResult,
    PhotoCategory, MacroCategory, CoverSelectionResult
)


class CoverSelector:
    CATEGORY_WEIGHTS = {
        PhotoCategory.FRONT_3_4: 40.0,
        PhotoCategory.FRONT: 35.0,
        PhotoCategory.REAR_3_4: 25.0,
        PhotoCategory.LEFT_SIDE: 20.0,
        PhotoCategory.RIGHT_SIDE: 20.0,
        PhotoCategory.REAR: 15.0,
        PhotoCategory.INTERIOR_FRONT: -50.0,
        PhotoCategory.INTERIOR_REAR: -55.0,
        PhotoCategory.DASHBOARD: -60.0,
        PhotoCategory.STEERING: -60.0,
        PhotoCategory.TRUNK: -70.0,
        PhotoCategory.ENGINE: -100.0,
        PhotoCategory.WHEEL: -100.0,
        PhotoCategory.KEY: -150.0,
        PhotoCategory.DOCUMENT: -500.0,
        PhotoCategory.UNKNOWN: -10.0
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
        has_exterior = any(
            MacroCategory.get_macro(class_map[a.filename].category if a.filename in class_map else PhotoCategory.UNKNOWN) == MacroCategory.EXTERIOR
            for a in valid_assets
        )

        for asset in valid_assets:
            fname = asset.filename
            q_score = quality_map.get(fname, PhotoQualityScore())
            cls_res = class_map.get(fname, PhotoClassificationResult())
            macro = cls_res.macro_category or MacroCategory.get_macro(cls_res.category)

            cat_weight = self.CATEGORY_WEIGHTS.get(cls_res.category, 0.0)
            total_rank = q_score.overall_score + cat_weight

            # Strict Rule: Non-exterior photos receive heavy penalty if valid exterior photos exist
            if has_exterior and macro != MacroCategory.EXTERIOR:
                total_rank -= 200.0

            # Document photo can never be cover
            if cls_res.category == PhotoCategory.DOCUMENT:
                total_rank -= 1000.0

            # Penalties
            if fname in duplicate_removed:
                total_rank -= 10.0
            if q_score.status == "BAD":
                total_rank -= 50.0
            elif q_score.status == "WARNING":
                total_rank -= 15.0
            if asset.orientation == "portrait":
                total_rank -= 15.0

            candidates.append({
                "file": fname,
                "total_rank_score": round(total_rank, 2),
                "category": cls_res.category,
                "macro_category": macro,
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
