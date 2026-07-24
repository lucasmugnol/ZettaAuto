"""Cover Selector module consuming normalized VisionAnalysisResult objects."""

from typing import List, Dict, Optional, Union, Any
from automedia.core.models import (
    ImageAsset, VehicleData, PhotoQualityScore, PhotoClassificationResult,
    PhotoCategory, MacroCategory, CoverSelectionResult, VisionAnalysisResult
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
        analyses: Any,
        class_map: Any = None,
        duplicate_removed: List[str] = None,
        vehicle_data: VehicleData = None,
        duplicate_files: List[str] = None
    ) -> CoverSelectionResult:
        valid_assets = [a for a in assets if a.is_valid]
        if not valid_assets:
            raise ValueError("No valid image assets available for cover selection.")

        # Normalize positional/keyword arguments
        if isinstance(duplicate_removed, VehicleData) and vehicle_data is None:
            vehicle_data = duplicate_removed
            duplicate_removed = class_map if isinstance(class_map, list) else []

        dup_list = duplicate_files or duplicate_removed or []

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
                        "category": PhotoCategory.UNKNOWN,
                        "overall_quality": 100.0
                    }]
                )

        # Normalize input to Dict[str, VisionAnalysisResult]
        analysis_map: Dict[str, VisionAnalysisResult] = {}
        for a in valid_assets:
            fname = a.filename
            if isinstance(analyses, dict) and fname in analyses and isinstance(analyses[fname], VisionAnalysisResult):
                analysis_map[fname] = analyses[fname]
            elif isinstance(class_map, dict) and fname in class_map:
                q_score = analyses.get(fname, PhotoQualityScore()) if isinstance(analyses, dict) else PhotoQualityScore()
                cls_res = class_map[fname]
                analysis_map[fname] = VisionAnalysisResult(
                    filename=fname,
                    category=cls_res.category,
                    macro_category=cls_res.macro_category or MacroCategory.get_macro(cls_res.category),
                    quality_score=q_score.overall_score,
                    suitable_for_cover=(cls_res.macro_category == MacroCategory.EXTERIOR),
                    cover_score=q_score.overall_score
                )
            else:
                analysis_map[fname] = VisionAnalysisResult(filename=fname)

        # Check if ANY valid exterior photo exists
        has_exterior = any(
            v.macro_category == MacroCategory.EXTERIOR for v in analysis_map.values()
        )

        candidates = []
        for asset in valid_assets:
            fname = asset.filename
            v_res = analysis_map[fname]
            cat = v_res.category
            macro = v_res.macro_category or MacroCategory.get_macro(cat)

            cat_weight = self.CATEGORY_WEIGHTS.get(cat, 0.0)
            
            # Combine vision provider cover_score with quality_score and category weight
            base_score = (v_res.cover_score * 0.6) + (v_res.quality_score * 0.4)
            total_rank = base_score + cat_weight

            # Strict Rule 1: Non-exterior photos receive heavy penalty if valid exterior photos exist
            if has_exterior and macro != MacroCategory.EXTERIOR:
                total_rank -= 200.0

            # Strict Rule 2: Document photo can never be cover
            if cat == PhotoCategory.DOCUMENT:
                total_rank -= 1000.0

            # Penalties
            if fname in dup_list:
                total_rank -= 10.0
            if asset.orientation == "portrait":
                total_rank -= 15.0

            candidates.append({
                "file": fname,
                "total_rank_score": round(total_rank, 2),
                "category": cat,
                "macro_category": macro,
                "overall_quality": v_res.quality_score,
                "cover_score": v_res.cover_score,
                "is_duplicate_removed": fname in dup_list,
                "status": "GOOD" if v_res.quality_score >= 60 else "WARNING"
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
