"""Local vision provider implementation for basic visual analysis."""

import math
from typing import List, Optional
from PIL import Image, ImageFilter, ImageStat
from automedia.core.interfaces import IVisionProvider
from automedia.core.models import ImageAsset, VehicleData, VisionAnalysis, PlateRegion


class LocalVisionProvider(IVisionProvider):
    def analyze_batch(
        self, images: List[ImageAsset], vehicle_data: VehicleData
    ) -> List[VisionAnalysis]:
        results: List[VisionAnalysis] = []

        # Find manual plate regions from vehicle_data if any
        manual_plate_map = {}
        if vehicle_data and vehicle_data.plate_regions:
            for pr in vehicle_data.plate_regions:
                manual_plate_map[pr.file.lower()] = pr

        for asset in images:
            if not asset.is_valid:
                continue

            analysis = self._analyze_single_image(asset, manual_plate_map.get(asset.filename.lower()))
            results.append(analysis)

        # Cover selection logic
        selected_cover = None
        if vehicle_data and vehicle_data.cover_image:
            # Look for explicit cover image match
            target = vehicle_data.cover_image.lower()
            for res in results:
                if res.file.lower() == target:
                    res.recommended_as_cover = True
                    selected_cover = res
                    break

        if not selected_cover and results:
            # Recommend image with highest quality_score
            best_res = max(results, key=lambda r: r.quality_score)
            best_res.recommended_as_cover = True

        return results

    def _analyze_single_image(self, asset: ImageAsset, manual_plate: Optional[PlateRegion]) -> VisionAnalysis:
        vehicle_bbox = {"x": 0, "y": 0, "width": asset.width, "height": asset.height}
        plate_regions: List[PlateRegion] = []
        detection_method = "not_found"

        if manual_plate:
            plate_regions.append(manual_plate)
            detection_method = "manual"

        sharpness, brightness, contrast = self._calculate_image_metrics(asset.path)

        # Quality score composite:
        # Ideal brightness ~ 128 (scale 0-100)
        brightness_penalty = abs(brightness - 128) / 128.0 * 30.0
        contrast_score = min(contrast, 100.0) / 100.0 * 35.0
        sharpness_score = min(sharpness, 100.0) / 100.0 * 35.0
        quality_score = max(0.0, min(100.0, sharpness_score + contrast_score + 30.0 - brightness_penalty))

        # Horizontal/Landscape photos generally get a slight preference for cover
        if asset.orientation == "landscape":
            quality_score = min(100.0, quality_score * 1.1)

        low_confidence = quality_score < 30.0

        return VisionAnalysis(
            file=asset.filename,
            vehicle_bbox=vehicle_bbox,
            plate_regions=plate_regions,
            quality_score=quality_score,
            sharpness_score=sharpness,
            brightness_score=brightness,
            contrast_score=contrast,
            recommended_as_cover=False,
            low_confidence=low_confidence,
            plate_detection_method=detection_method
        )

    def _calculate_image_metrics(self, image_path: str):
        try:
            with Image.open(image_path) as img:
                gray = img.convert("L")
                stat = ImageStat.Stat(gray)

                brightness = stat.mean[0]
                contrast = stat.stddev[0]

                # Sharpness estimation via edge magnitude variance
                edges = gray.filter(ImageFilter.FIND_EDGES)
                edge_stat = ImageStat.Stat(edges)
                sharpness = edge_stat.var[0] ** 0.5

                return sharpness, brightness, contrast
        except Exception:
            return 10.0, 128.0, 20.0
