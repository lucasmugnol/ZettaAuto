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
                    enhancer = ImageEnhance.Contrast(img)
                    img = enhancer.enhance(1.0 + (adjustment_intensity * 0.5))

                    enhancer = ImageEnhance.Brightness(img)
                    img = enhancer.enhance(1.0 + (adjustment_intensity * 0.2))

                    enhancer = ImageEnhance.Sharpness(img)
                    img = enhancer.enhance(1.0 + (adjustment_intensity * 0.4))

                # Resize and fit to target dimensions using contain/pad
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
        quality: int = 90,
        cover_fit_strategy: str = "contain",
        bg_fill_strategy: str = "blurred"
    ) -> bool:
        try:
            tw, th = target_dimensions
            canvas = Image.new("RGB", (tw, th), color=brand_config.primary_color)

            # Reserved photo area (upper 72% of cover)
            photo_height = int(th * 0.72)

            with Image.open(main_image_path) as main_img:
                main_img = ImageOps.exif_transpose(main_img)
                main_rgb = main_img.convert("RGB")
                orig_w, orig_h = main_rgb.size

                if cover_fit_strategy == "crop":
                    fitted_photo = ImageOps.fit(main_rgb, (tw, photo_height), Image.Resampling.LANCZOS)
                else:
                    # DEFAULT: contain strategy (preserves entire vehicle without cropping)
                    scale = min(tw / float(orig_w), photo_height / float(orig_h))
                    scaled_w = max(1, int(orig_w * scale))
                    scaled_h = max(1, int(orig_h * scale))
                    scaled_img = main_rgb.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)

                    if bg_fill_strategy == "blurred":
                        # Blurred background container derived from the image itself
                        bg_img = ImageOps.fit(main_rgb, (tw, photo_height), Image.Resampling.LANCZOS)
                        bg_blurred = bg_img.filter(ImageFilter.GaussianBlur(radius=35))
                        fitted_photo = bg_blurred
                    else:
                        fitted_photo = Image.new("RGB", (tw, photo_height), color=brand_config.primary_color)

                    offset_x = (tw - scaled_w) // 2
                    offset_y = (photo_height - scaled_h) // 2
                    fitted_photo.paste(scaled_img, (offset_x, offset_y))

                canvas.paste(fitted_photo, (0, 0))

            # Bottom brand bar (28% of height)
            draw = ImageDraw.Draw(canvas)
            bar_y = photo_height

            # Accent line (secondary color)
            accent_height = max(4, int(th * 0.008))
            draw.rectangle([0, bar_y, tw, bar_y + accent_height], fill=brand_config.secondary_color)

            content_y = bar_y + accent_height + int(th * 0.015)
            padding_x = int(tw * 0.035)

            # Determine reserved logo width
            max_logo_w = int(tw * 0.22)
            max_logo_h = int((th - bar_y) * 0.55)

            logo_space = max_logo_w + padding_x if (brand_config.logo_path and os.path.exists(brand_config.logo_path)) else 0
            text_max_w = tw - (padding_x * 2) - logo_space

            # Typography loading with safe fallbacks
            font_title_size = max(16, int(th * 0.035))
            font_sub_size = max(13, int(th * 0.024))
            font_price_size = max(18, int(th * 0.040))
            font_cta_size = max(12, int(th * 0.022))

            font_title = self._load_font(brand_config.font_path, font_title_size)
            font_sub = self._load_font(brand_config.font_path, font_sub_size)
            font_price = self._load_font(brand_config.font_path, font_price_size)
            font_cta = self._load_font(brand_config.font_path, font_cta_size)

            title_str = f"{vehicle_data.manufacturer} {vehicle_data.model}".upper()
            title_str = self._truncate_text(draw, title_str, font_title, text_max_w)

            sub_str = f"ANO {vehicle_data.year}"
            sub_str = self._truncate_text(draw, sub_str, font_sub, text_max_w)

            price_str = f"{vehicle_data.price}"
            price_str = self._truncate_text(draw, price_str, font_price, text_max_w)

            # Draw lines
            curr_y = content_y
            draw.text((padding_x, curr_y), title_str, fill=brand_config.text_color, font=font_title)
            curr_y += font_title_size + 4

            draw.text((padding_x, curr_y), sub_str, fill="#CBD5E1", font=font_sub)
            curr_y += font_sub_size + 6

            draw.text((padding_x, curr_y), price_str, fill=brand_config.secondary_color, font=font_price)
            curr_y += font_price_size + 6

            # Render CTA ONLY if brand_config.cta is non-empty!
            if brand_config.cta and brand_config.cta.strip():
                cta_str = self._truncate_text(draw, brand_config.cta.strip(), font_cta, text_max_w)
                draw.text((padding_x, curr_y), cta_str, fill="#94A3B8", font=font_cta)

            # Render Logo if present
            if brand_config.logo_path and os.path.exists(brand_config.logo_path):
                try:
                    with Image.open(brand_config.logo_path) as logo:
                        logo_rgba = logo.convert("RGBA")
                        logo_rgba.thumbnail((max_logo_w, max_logo_h), Image.Resampling.LANCZOS)
                        
                        logo_x = tw - logo_rgba.width - padding_x
                        logo_y = content_y + int((th - bar_y - logo_rgba.height) * 0.3)
                        
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

    def _load_font(self, font_path: Optional[str], size: int) -> ImageFont.ImageFont:
        if font_path and os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                pass

        # Try common OS TrueType system fonts
        system_fonts = [
            "arial.ttf", "DejaVuSans.ttf", "segoeui.ttf",
            "helvetica.ttf", "Calibri.ttf", "FreeSans.ttf"
        ]
        for sys_font in system_fonts:
            try:
                return ImageFont.truetype(sys_font, size)
            except Exception:
                continue

        # Fallback to PIL default
        return ImageFont.load_default()

    def _truncate_text(self, draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_w: int) -> str:
        if max_w <= 0:
            return text
        
        def get_w(t: str) -> int:
            try:
                bbox = draw.textbbox((0, 0), t, font=font)
                return bbox[2] - bbox[0]
            except Exception:
                return len(t) * 8

        if get_w(text) <= max_w:
            return text

        ellipsis = "..."
        truncated = text
        while len(truncated) > 1 and get_w(truncated + ellipsis) > max_w:
            truncated = truncated[:-1]

        return truncated + ellipsis if len(truncated) > 1 else truncated
