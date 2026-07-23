"""Validator module for decoding images and enforcing quality limits."""

from typing import List, Tuple
from PIL import Image
from automedia.core.models import ImageAsset, PipelineConfig
from automedia.core.errors import EmptyBatchError, InvalidInputError, CorruptedImageError


class Validator:
    def __init__(self, pipeline_config: PipelineConfig):
        self.config = pipeline_config

    def validate_assets(self, assets: List[ImageAsset]) -> Tuple[List[ImageAsset], List[str]]:
        """Validate list of image assets and return (valid_assets, warnings_list)."""
        if not assets:
            raise EmptyBatchError("No image files found in input directory.")

        valid_assets: List[ImageAsset] = []
        warnings: List[str] = []

        for asset in assets:
            if asset.is_duplicate:
                warnings.append(f"Image '{asset.filename}' is a byte-for-byte duplicate. Skipping.")
                asset.is_valid = False
                asset.error_message = "Duplicate image"
                continue

            max_bytes = self.config.max_file_size_mb * 1024 * 1024
            if asset.file_size_bytes > max_bytes:
                msg = f"Image '{asset.filename}' exceeds max size of {self.config.max_file_size_mb}MB."
                warnings.append(msg)
                asset.is_valid = False
                asset.error_message = msg
                continue

            try:
                with Image.open(asset.path) as img:
                    img.verify()

                # Re-open for size and format info after verify()
                with Image.open(asset.path) as img:
                    width, height = img.size
                    mime_type = Image.MIME.get(img.format, "image/unknown")

                    asset.width = width
                    asset.height = height
                    asset.mime_type = mime_type

                    if width > height:
                        asset.orientation = "landscape"
                    elif height > width:
                        asset.orientation = "portrait"
                    else:
                        asset.orientation = "square"

                    if width < self.config.min_width or height < self.config.min_height:
                        msg = (
                            f"Image '{asset.filename}' resolution ({width}x{height}) is below "
                            f"minimum ({self.config.min_width}x{self.config.min_height})."
                        )
                        warnings.append(msg)
                        asset.is_valid = False
                        asset.error_message = msg
                        continue

                    asset.is_valid = True
                    valid_assets.append(asset)

            except Exception as e:
                msg = f"Corrupted or unreadable image '{asset.filename}': {str(e)}"
                warnings.append(msg)
                asset.is_valid = False
                asset.error_message = msg

        if not valid_assets:
            raise EmptyBatchError("No usable valid images remain after validation.")

        return valid_assets, warnings
