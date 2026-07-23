"""Local Duplicate Detector implementation using perceptual dHash and Color Histogram Correlation."""

import os
import math
from typing import List, Tuple, Dict, Optional
from PIL import Image, ImageStat
from automedia.core.interfaces import IDuplicateDetector
from automedia.core.models import ImageAsset, PhotoQualityScore, DuplicateGroup


class LocalDuplicateDetector(IDuplicateDetector):
    def __init__(self, hamming_threshold: int = 3, histogram_threshold: float = 0.94):
        self.hamming_threshold = hamming_threshold
        self.histogram_threshold = histogram_threshold

    def detect_duplicates(
        self, assets: List[ImageAsset], quality_scores: Dict[str, PhotoQualityScore]
    ) -> Tuple[List[DuplicateGroup], List[str]]:
        hashes: Dict[str, int] = {}
        histograms: Dict[str, List[int]] = {}
        valid_assets = [a for a in assets if a.is_valid and not a.is_duplicate]

        for asset in valid_assets:
            h = self._compute_dhash(asset.path)
            hist = self._compute_color_histogram(asset.path)
            if h is not None:
                hashes[asset.filename] = h
            if hist is not None:
                histograms[asset.filename] = hist

        groups: List[DuplicateGroup] = []
        duplicate_removed: List[str] = []
        visited = set()

        filenames = [a.filename for a in valid_assets if a.filename in hashes]

        group_idx = 1
        for i in range(len(filenames)):
            f1 = filenames[i]
            if f1 in visited:
                continue

            cluster = [f1]
            for j in range(i + 1, len(filenames)):
                f2 = filenames[j]
                if f2 in visited:
                    continue

                dist = self._hamming_distance(hashes[f1], hashes[f2])
                hist_sim = self._histogram_similarity(histograms.get(f1), histograms.get(f2))

                # Require BOTH low hamming distance AND high color histogram similarity
                if dist <= self.hamming_threshold and hist_sim >= self.histogram_threshold:
                    cluster.append(f2)

            if len(cluster) > 1:
                cluster_sorted = sorted(
                    cluster,
                    key=lambda f: quality_scores[f].overall_score if f in quality_scores else 0.0,
                    reverse=True
                )

                primary = cluster_sorted[0]
                dups = cluster_sorted[1:]

                for f in cluster:
                    visited.add(f)

                duplicate_removed.extend(dups)

                sim_score = round(self._histogram_similarity(histograms.get(primary), histograms.get(dups[0])) * 100.0, 2)
                group = DuplicateGroup(
                    group_id=f"group_{group_idx:02d}",
                    primary_file=primary,
                    duplicate_files=dups,
                    similarity_score=sim_score
                )
                groups.append(group)
                group_idx += 1

        return groups, duplicate_removed

    def _compute_dhash(self, image_path: str, hash_size: int = 8) -> Optional[int]:
        try:
            with Image.open(image_path) as img:
                resized = img.convert("L").resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
                if hasattr(resized, "get_flattened_data"):
                    pixels = list(resized.get_flattened_data())
                else:
                    pixels = list(resized.getdata())

                difference = []
                for row in range(hash_size):
                    for col in range(hash_size):
                        pixel_left = pixels[row * (hash_size + 1) + col]
                        pixel_right = pixels[row * (hash_size + 1) + col + 1]
                        difference.append(pixel_left > pixel_right)

                decimal_value = 0
                for bit in difference:
                    decimal_value = (decimal_value << 1) | int(bit)

                return decimal_value
        except Exception:
            return None

    def _compute_color_histogram(self, image_path: str) -> Optional[List[int]]:
        try:
            with Image.open(image_path) as img:
                img_rgb = img.convert("RGB").resize((128, 128), Image.Resampling.LANCZOS)
                return img_rgb.histogram()
        except Exception:
            return None

    def _histogram_similarity(self, h1: Optional[List[int]], h2: Optional[List[int]]) -> float:
        if not h1 or not h2 or len(h1) != len(h2):
            return 0.0
        sum1 = sum(h1)
        sum2 = sum(h2)
        if sum1 == 0 or sum2 == 0:
            return 0.0

        n1 = [x / float(sum1) for x in h1]
        n2 = [x / float(sum2) for x in h2]

        intersection = sum(min(a, b) for a, b in zip(n1, n2))
        return intersection

    def _hamming_distance(self, h1: int, h2: int) -> int:
        x = h1 ^ h2
        set_bits = 0
        while x > 0:
            set_bits += x & 1
            x >>= 1
        return set_bits
