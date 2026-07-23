"""Unit tests for Sprint 2 Module 6: Gallery Coverage Analysis."""

from automedia.core.models import PhotoClassificationResult, PhotoCategory
from automedia.modules.gallery_coverage import GalleryCoverageAnalyzer


def test_gallery_coverage_analysis():
    analyzer = GalleryCoverageAnalyzer()
    class_results = [
        PhotoClassificationResult(category=PhotoCategory.FRONT_3_4),
        PhotoClassificationResult(category=PhotoCategory.REAR_3_4),
        PhotoClassificationResult(category=PhotoCategory.DASHBOARD),
        PhotoClassificationResult(category=PhotoCategory.WHEEL)
    ]

    coverage = analyzer.analyze_coverage(class_results)

    assert coverage.coverage_score > 0.0
    assert isinstance(coverage.present_categories, list)
    assert isinstance(coverage.missing_categories, list)
    assert len(coverage.present_categories) > 0
    assert len(coverage.missing_categories) > 0
