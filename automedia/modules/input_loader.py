"""Input Loader module for discovering and indexing raw image files."""

import os
import hashlib
from typing import List
from automedia.core.models import ImageAsset, PipelineConfig
from automedia.core.errors import InvalidInputError


class InputLoader:
    def __init__(self, pipeline_config: PipelineConfig):
        self.config = pipeline_config

    def load_input_images(self, input_dir: str) -> List[ImageAsset]:
        if not os.path.exists(input_dir):
            raise InvalidInputError(f"Input directory does not exist: {input_dir}")
        if not os.path.isdir(input_dir):
            raise InvalidInputError(f"Input path is not a directory: {input_dir}")

        entries = sorted(os.listdir(input_dir))
        assets: List[ImageAsset] = []
        seen_hashes = set()

        for entry in entries:
            file_path = os.path.join(input_dir, entry)
            if not os.path.isfile(file_path):
                continue

            ext = os.path.splitext(entry)[1].lower()
            if ext not in self.config.accepted_formats:
                continue

            file_hash = self._compute_sha256(file_path)
            file_size = os.path.getsize(file_path)

            is_duplicate = file_hash in seen_hashes
            if not is_duplicate:
                seen_hashes.add(file_hash)

            asset = ImageAsset(
                path=file_path,
                filename=entry,
                file_hash=file_hash,
                file_size_bytes=file_size,
                is_duplicate=is_duplicate
            )
            assets.append(asset)

        return assets

    def _compute_sha256(self, file_path: str) -> str:
        sha = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                sha.update(chunk)
        return sha.hexdigest()
