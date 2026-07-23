"""Local Duplicate Detector implementation using perceptual hashing."""

import os
from typing import List, Tuple, Dict, Optional
from PIL import Image
from automedia.core.interfaces import IDuplicateDetector
from automedia.core.models import ImageAsset, PhotoQualityScore, DuplicateGroup


class LocalDuplicateDetector(IDuplicateDetector):
    def __init__(self, hamming_threshold: int = 8):
        self.hamming_threshold = hamming_threshold

    def detect_duplicates(
        self, assets: List[ImageAsset], quality_scores: Dict[str, PhotoQualityScore]
    ) -> Tuple[List[DuplicateGroup], List[str]]:
        hashes: Dict[str, int] = {}
        valid_assets = [a for a in assets if a.is_valid and not a.is_duplicate]

        for asset in valid_assets:
            h = self._compute_dhash(asset.path)
            if h is not None:
                hashes[asset.filename] = h

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
                if dist <= self.hamming_threshold:
                    cluster.append(f2)

            if len(cluster) > 1:
                # Rank cluster members by overall quality score
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

                sim_score = round((1.0 - (self._hamming_distance(hashes[primary], hashes[dups[0]]) / 64.0)) * 100.0, 2)
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
                # Resize to (hash_size + 1, hash_size) and convert to grayscale
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

    def _hamming_distance(self, h1: int, h2: int) -> int:
        x = h1 ^ h2
        set_bits = 0
        while x > 0:
            set_bits += x & 1
            x >>= 1
        return set_bits
