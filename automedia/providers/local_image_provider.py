"""Local image provider implementation for Pillow-based processing."""

import os
from typing import Tuple, List, Dict, Any, Optional
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont, ImageOps
from automedia.core.interfaces import IImageProvider
from automedia.core.models import PlateRegion, BrandConfig, VehicleData
from automedia.core.errors import ProcessingError, CoverFailureError


class LocalImageProvider(IImageProvider):
    def process_and_adjust(
        self,
        image_path: str,
        output_path: str,
        target_dimensions: Tuple[int, int],
        adjustment_intensity: float,
        quality: int = 90
    ) -> bool:
        try:
            with Image.open(image_path) as img:
                # Fix EXIF orientation if present
                img = ImageOps.exif_transpose(img)
                if img.mode != "RGB":
                    img = img.convert("RGB")

                # Apply moderate adjustments (preserving original color fidelity)
                if adjustment_intensity > 0:
                    # Contrast adjustment
                    enhancer = ImageEnhance.Contrast(img)
                    img = enhancer.enhance(1.0 + (adjustment_intensity * 0.5))

                    # Brightness adjustment
                    enhancer = ImageEnhance.Brightness(img)
                    img = enhancer.enhance(1.0 + (adjustment_intensity * 0.2))

                    # Sharpness adjustment
                    enhancer = ImageEnhance.Sharpness(img)
                    img = enhancer.enhance(1.0 + (adjustment_intensity * 0.4))

                # Resize and crop to fill target dimensions
                img_fitted = ImageOps.fit(img, target_dimensions, Image.Resampling.LANCZOS)
                
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                img_fitted.save(output_path, quality=quality)
                return True
        except Exception as e:
            raise ProcessingError(f"Failed to process image '{image_path}': {str(e)}")

    def apply_plate_cover(
        self,
        image_path: str,
        output_path: str,
        plate_regions: List[PlateRegion],
        strategy: str,
        primary_color_hex: str = "#1E3A8A",
        quality: int = 90
    ) -> bool:
        if not plate_regions:
            # If no regions, just copy/save if target differs, or return True
            if image_path != output_path:
                with Image.open(image_path) as img:
                    img.save(output_path, quality=quality)
            return True

        try:
            with Image.open(image_path) as img:
                img = ImageOps.exif_transpose(img)
                if img.mode != "RGB":
                    img = img.convert("RGB")

                img_w, img_h = img.size

                for region in plate_regions:
                    # Clamp coordinates safely to image bounds
                    x1 = max(0, min(region.x, img_w - 1))
                    y1 = max(0, min(region.y, img_h - 1))
                    x2 = max(x1 + 1, min(region.x + region.width, img_w))
                    y2 = max(y1 + 1, min(region.y + region.height, img_h))

                    box = (x1, y1, x2, y2)
                    crop_w = x2 - x1
                    crop_h = y2 - y1

                    if crop_w <= 0 or crop_h <= 0:
                        continue

                    if strategy == "blur":
                        cropped = img.crop(box)
                        blurred = cropped.filter(ImageFilter.GaussianBlur(radius=15))
                        img.paste(blurred, box)
                    else:  # "solid_cover" or default
                        draw = ImageDraw.Draw(img)
                        # Draw solid rectangle
                        draw.rectangle(box, fill=primary_color_hex, outline="#FFFFFF", width=2)

                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                img.save(output_path, quality=quality)
                return True
        except Exception as e:
            raise ProcessingError(f"Failed applying plate cover on '{image_path}': {str(e)}")

    def apply_watermark(
        self,
        image_path: str,
        output_path: str,
        logo_path: Optional[str],
        watermark_policy: Dict[str, Any],
        opacity: float = 0.35,
        quality: int = 90
    ) -> bool:
        try:
            with Image.open(image_path) as base_img:
                base_img = ImageOps.exif_transpose(base_img)
                base_rgba = base_img.convert("RGBA")
                w, h = base_rgba.size

                if logo_path and os.path.exists(logo_path):
                    with Image.open(logo_path) as logo:
                        logo_rgba = logo.convert("RGBA")
                        scale_ratio = watermark_policy.get("scale_ratio", 0.18)
                        target_logo_w = int(w * scale_ratio)
                        aspect = logo_rgba.height / float(logo_rgba.width)
                        target_logo_h = int(target_logo_w * aspect)

                        logo_resized = logo_rgba.resize((target_logo_w, target_logo_h), Image.Resampling.LANCZOS)

                        # Apply opacity
                        alpha = logo_resized.split()[3]
                        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
                        logo_resized.putalpha(alpha)

                        margin = watermark_policy.get("margin_pixels", 25)
                        pos = watermark_policy.get("position", "bottom_right")

                        if pos == "bottom_left":
                            pos_x, pos_y = margin, h - target_logo_h - margin
                        elif pos == "top_right":
                            pos_x, pos_y = w - target_logo_w - margin, margin
                        elif pos == "top_left":
                            pos_x, pos_y = margin, margin
                        else:  # bottom_right
                            pos_x, pos_y = w - target_logo_w - margin, h - target_logo_h - margin

                        pos_x = max(0, min(pos_x, w - target_logo_w))
                        pos_y = max(0, min(pos_y, h - target_logo_h))

                        base_rgba.paste(logo_resized, (pos_x, pos_y), logo_resized)

                final_rgb = base_rgba.convert("RGB")
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                final_rgb.save(output_path, quality=quality)
                return True
        except Exception as e:
            raise ProcessingError(f"Failed applying watermark to '{image_path}': {str(e)}")

    def compose_cover(
        self,
        main_image_path: str,
        output_path: str,
        brand_config: BrandConfig,
        vehicle_data: VehicleData,
        target_dimensions: Tuple[int, int],
        quality: int = 90
    ) -> bool:
        try:
            tw, th = target_dimensions
            canvas = Image.new("RGB", (tw, th), color=brand_config.primary_color)

            # Fit main vehicle image in upper 75% of the cover
            photo_height = int(th * 0.72)
            with Image.open(main_image_path) as main_img:
                main_img = ImageOps.exif_transpose(main_img)
                main_rgb = main_img.convert("RGB")
                fitted_photo = ImageOps.fit(main_rgb, (tw, photo_height), Image.Resampling.LANCZOS)
                canvas.paste(fitted_photo, (0, 0))

            # Bottom brand bar (28% of height)
            draw = ImageDraw.Draw(canvas)
            bar_y = photo_height
            bar_h = th - bar_y

            # Accent line (secondary color)
            accent_height = 8
            draw.rectangle([0, bar_y, tw, bar_y + accent_height], fill=brand_config.secondary_color)

            # Text & Info Overlay
            content_y = bar_y + accent_height + 15
            padding_x = 35

            title_str = f"{vehicle_data.manufacturer} {vehicle_data.model}".upper()
            sub_str = f"ANO {vehicle_data.year}"
            price_str = f"{vehicle_data.price}"
            cta_str = brand_config.cta if brand_config.cta else "Consulte condições de financiamento!"

            # Try loading default font
            font_title = ImageFont.load_default()
            font_price = ImageFont.load_default()

            draw.text((padding_x, content_y), title_str, fill=brand_config.text_color, font=font_title)
            draw.text((padding_x, content_y + 30), sub_str, fill="#CBD5E1", font=font_title)
            draw.text((padding_x, content_y + 60), price_str, fill=brand_config.secondary_color, font=font_price)
            draw.text((padding_x, content_y + 100), cta_str, fill="#94A3B8", font=font_title)

            # Add logo if specified and valid
            if brand_config.logo_path and os.path.exists(brand_config.logo_path):
                try:
                    with Image.open(brand_config.logo_path) as logo:
                        logo_rgba = logo.convert("RGBA")
                        max_logo_w, max_logo_h = 180, 80
                        logo_rgba.thumbnail((max_logo_w, max_logo_h), Image.Resampling.LANCZOS)
                        
                        logo_x = tw - logo_rgba.width - padding_x
                        logo_y = content_y + 10
                        
                        canvas_rgba = canvas.convert("RGBA")
                        canvas_rgba.paste(logo_rgba, (logo_x, logo_y), logo_rgba)
                        canvas = canvas_rgba.convert("RGB")
                except Exception as e:
                    raise CoverFailureError(f"Logo image error in brand config: {str(e)}")

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            canvas.save(output_path, quality=quality)
            return True
        except CoverFailureError:
            raise
        except Exception as e:
            raise CoverFailureError(f"Failed to compose cover image: {str(e)}")
