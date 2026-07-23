"""Gallery Coverage module for analyzing category completeness."""

from typing import List, Dict
from automedia.core.models import PhotoCategory, PhotoClassificationResult, GalleryCoverage


class GalleryCoverageAnalyzer:
    ESSENTIAL_CHECKLIST = [
        ("Front View", [PhotoCategory.FRONT, PhotoCategory.FRONT_3_4]),
        ("Rear View", [PhotoCategory.REAR, PhotoCategory.REAR_3_4]),
        ("Side View", [PhotoCategory.LEFT_SIDE, PhotoCategory.RIGHT_SIDE]),
        ("Dashboard", [PhotoCategory.DASHBOARD]),
        ("Interior", [PhotoCategory.INTERIOR_FRONT, PhotoCategory.INTERIOR_REAR, PhotoCategory.STEERING]),
        ("Trunk", [PhotoCategory.TRUNK]),
        ("Engine", [PhotoCategory.ENGINE]),
        ("Wheel", [PhotoCategory.WHEEL])
    ]

    def analyze_coverage(
        self, class_results: List[PhotoClassificationResult]
    ) -> GalleryCoverage:
        category_counts: Dict[str, int] = {}
        for res in class_results:
            cat = res.category
            category_counts[cat] = category_counts.get(cat, 0) + 1

        present: List[str] = []
        missing: List[str] = []

        total_checklist_items = len(self.ESSENTIAL_CHECKLIST)
        fulfilled_items = 0

        for label, cat_list in self.ESSENTIAL_CHECKLIST:
            has_item = any(category_counts.get(c, 0) > 0 for c in cat_list)
            if has_item:
                fulfilled_items += 1
                present.append(label)
            else:
                missing.append(label)

        coverage_score = round((fulfilled_items / float(total_checklist_items)) * 100.0, 2)

        return GalleryCoverage(
            present_categories=present,
            missing_categories=missing,
            coverage_score=coverage_score,
            category_counts=category_counts
        )
