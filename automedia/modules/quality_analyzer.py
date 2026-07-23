"""Quality Analyzer module wrapping photo quality analysis, classification and duplicate detection."""

from typing import List, Dict, Tuple
from automedia.core.interfaces import IPhotoAnalyzer, IPhotoClassifier, IDuplicateDetector
from automedia.core.models import (
    ImageAsset, PhotoQualityScore, PhotoClassificationResult, DuplicateGroup
)


class QualityAnalyzerModule:
    def __init__(
        self,
        analyzer: IPhotoAnalyzer,
        classifier: IPhotoClassifier,
        duplicate_detector: IDuplicateDetector
    ):
        self.analyzer = analyzer
        self.classifier = classifier
        self.duplicate_detector = duplicate_detector

    def analyze_batch(
        self, assets: List[ImageAsset]
    ) -> Tuple[
        Dict[str, PhotoQualityScore],
        Dict[str, PhotoClassificationResult],
        List[DuplicateGroup],
        List[str]
    ]:
        quality_map: Dict[str, PhotoQualityScore] = {}
        class_map: Dict[str, PhotoClassificationResult] = {}

        valid_assets = [a for a in assets if a.is_valid]

        # 1. Quality Analysis
        for asset in valid_assets:
            q_score = self.analyzer.analyze_quality(asset.path, asset)
            quality_map[asset.filename] = q_score

        # 2. Category Classification
        for asset in valid_assets:
            cls_res = self.classifier.classify_photo(
                asset.path, asset, quality_map.get(asset.filename)
            )
            class_map[asset.filename] = cls_res

        # 3. Near-Duplicate Detection
        dup_groups, dup_removed = self.duplicate_detector.detect_duplicates(
            valid_assets, quality_map
        )

        return quality_map, class_map, dup_groups, dup_removed
