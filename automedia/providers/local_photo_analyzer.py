"""Local Photo Analyzer implementation using Pillow image heuristics."""

import math
from PIL import Image, ImageFilter, ImageStat
from automedia.core.interfaces import IPhotoAnalyzer
from automedia.core.models import ImageAsset, PhotoQualityScore


class LocalPhotoAnalyzer(IPhotoAnalyzer):
    def analyze_quality(self, image_path: str, asset: ImageAsset) -> PhotoQualityScore:
        try:
            with Image.open(image_path) as img:
                w, h = img.size
                gray = img.convert("L")
                stat = ImageStat.Stat(gray)

                mean_val = stat.mean[0]
                stddev_val = stat.stddev[0]

                # 1. Sharpness via edge magnitude variance
                edges = gray.filter(ImageFilter.FIND_EDGES)
                edge_stat = ImageStat.Stat(edges)
                sharpness_raw = edge_stat.var[0] ** 0.5
                sharpness = min(100.0, max(0.0, (sharpness_raw / 40.0) * 100.0))

                # 2. Brightness (ideal mean around 128)
                brightness = min(100.0, max(0.0, 100.0 - abs(mean_val - 128.0) / 1.28))

                # 3. Contrast (ideal stddev around 50-70)
                contrast = min(100.0, max(0.0, (stddev_val / 65.0) * 100.0))

                # 4. Exposure (histogram clipping analysis)
                hist = gray.histogram()
                under_clipped = sum(hist[:15]) / float(w * h)
                over_clipped = sum(hist[240:]) / float(w * h)
                exposure_penalty = (under_clipped + over_clipped) * 100.0
                exposure = min(100.0, max(0.0, 100.0 - exposure_penalty * 1.5))

                # 5. Noise estimation (high frequency residual)
                blurred = gray.filter(ImageFilter.GaussianBlur(radius=2))
                # Diff between original and blurred
                diff_stat = ImageStat.Stat(gray)
                noise = min(100.0, max(0.0, 100.0 - (diff_stat.stddev[0] * 0.5)))

                # 6. Reflection score (ratio of extreme specular highlights)
                specular_ratio = sum(hist[250:]) / float(w * h)
                reflection_score = min(100.0, max(0.0, 100.0 - (specular_ratio * 400.0)))

                # 7. Composition score (aspect ratio, resolution, central detail)
                res_score = min(1.0, (w * h) / (1920.0 * 1080.0)) * 50.0
                aspect_ratio = w / float(h)
                aspect_score = 50.0 if (1.2 <= aspect_ratio <= 1.8) else 30.0
                composition_score = min(100.0, res_score + aspect_score)

                # 8. Orientation score
                orientation_score = 100.0 if asset.orientation == "landscape" else (80.0 if asset.orientation == "square" else 60.0)

                # 9. Color balance (RGB channel symmetry)
                if img.mode != "RGB":
                    img_rgb = img.convert("RGB")
                else:
                    img_rgb = img
                rgb_stats = ImageStat.Stat(img_rgb)
                r_m, g_m, b_m = rgb_stats.mean[:3]
                color_diff = (abs(r_m - g_m) + abs(g_m - b_m) + abs(b_m - r_m)) / 3.0
                color_balance = min(100.0, max(0.0, 100.0 - color_diff * 1.2))

                # Overall Score (Weighted Average)
                overall_score = (
                    sharpness * 0.25 +
                    brightness * 0.15 +
                    contrast * 0.15 +
                    exposure * 0.10 +
                    composition_score * 0.15 +
                    orientation_score * 0.10 +
                    color_balance * 0.10
                )
                overall_score = round(min(100.0, max(0.0, overall_score)), 2)

                # Quality Issues Identification
                issues = []
                if mean_val < 60:
                    issues.append("too_dark")
                if mean_val > 200:
                    issues.append("too_bright")
                if sharpness < 30:
                    issues.append("blurry")
                if contrast < 25:
                    issues.append("low_contrast")
                if w < 600 or h < 400:
                    issues.append("low_resolution")
                if asset.orientation == "portrait":
                    issues.append("incorrect_orientation")

                if overall_score >= 60.0 and not issues:
                    status = "GOOD"
                elif overall_score >= 35.0:
                    status = "WARNING"
                else:
                    status = "BAD"

                return PhotoQualityScore(
                    overall_score=overall_score,
                    sharpness=round(sharpness, 2),
                    brightness=round(brightness, 2),
                    contrast=round(contrast, 2),
                    exposure=round(exposure, 2),
                    noise=round(noise, 2),
                    reflection_score=round(reflection_score, 2),
                    composition_score=round(composition_score, 2),
                    orientation_score=round(orientation_score, 2),
                    color_balance=round(color_balance, 2),
                    status=status,
                    quality_issues=issues
                )
        except Exception:
            return PhotoQualityScore(
                overall_score=20.0,
                status="BAD",
                quality_issues=["corrupted_or_unreadable"]
            )
