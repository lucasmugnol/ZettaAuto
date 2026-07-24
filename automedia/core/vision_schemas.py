"""Schema validation and prompt definitions for Multimodal Vision Provider."""

import json
from typing import Dict, Any, Tuple, Optional
from automedia.core.models import PhotoCategory, MacroCategory
from automedia.core.vision_models import MultimodalAnalysisResult

AUTOMEDIA_VISION_PROMPT_V1 = """You are an expert automotive media analyst AI.
Analyze the provided vehicle photograph and return ONLY a valid JSON object matching the exact schema below.

CRITICAL DIRECTIVES:
1. Analyze ONLY visual content in the image.
2. DO NOT guess, infer, or hallucinate vehicle specs (make, model, year, price, mileage, or features).
3. Classify the photo into EXACTLY ONE official category from this list:
   - FRONT (Direct front view of vehicle)
   - FRONT_3_4 (Front 3/4 perspective view - PREFERRED FOR COVER)
   - REAR (Direct rear view)
   - REAR_3_4 (Rear 3/4 perspective view)
   - LEFT_SIDE (Left side profile)
   - RIGHT_SIDE (Right side profile)
   - INTERIOR_FRONT (Front seats / cockpit view)
   - INTERIOR_REAR (Rear passenger seats)
   - DASHBOARD (Instrument cluster / dashboard gauges)
   - STEERING (Steering wheel close-up)
   - ENGINE (Engine compartment)
   - TRUNK (Boot / cargo trunk space)
   - WHEEL (Alloy wheel / tire close-up)
   - KEY (Vehicle key fob)
   - DOCUMENT (Vehicle papers / inspection report)
   - UNKNOWN (Unclear image)

4. Set macro_category to one of: EXTERIOR, INTERIOR, DETAIL, MECHANICAL, DOCUMENT, UNKNOWN.
5. Cover suitability (suitable_for_cover):
   - Set suitable_for_cover to TRUE ONLY for clean exterior views (FRONT_3_4, FRONT, REAR_3_4, SIDE).
   - Set suitable_for_cover to FALSE for ENGINE, WHEEL, KEY, DOCUMENT, TRUNK, INTERIOR, or DASHBOARD.
6. Provide scores between 0.0 and 100.0 for cover_score, composition_score, framing_score.
7. Provide vehicle_visibility as a float between 0.0 and 1.0 (portion of vehicle visible).
8. Estimate content_bbox_estimate as bounding box {"x": int, "y": int, "width": int, "height": int} around the main vehicle body.
9. Indicate if a license plate is visible (plate_visible: true/false) and provide plate_bbox if visible.
10. Return ONLY raw JSON without markdown formatting or introductory text.

REQUIRED JSON SCHEMA:
{
  "category": "FRONT_3_4",
  "macro_category": "EXTERIOR",
  "confidence": 0.95,
  "suitable_for_cover": true,
  "cover_score": 90.0,
  "quality_status": "GOOD",
  "visual_issues": [],
  "composition_score": 88.0,
  "framing_score": 90.0,
  "vehicle_visibility": 0.95,
  "content_bbox_estimate": {"x": 50, "y": 50, "width": 800, "height": 500},
  "plate_visible": false,
  "plate_bbox": null,
  "reasoning_summary": "Clean front 3/4 exterior photo of vehicle in bright daylight."
}
"""


def parse_and_validate_vision_json(
    raw_text: str, img_w: int = 0, img_h: int = 0
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Parses raw model output text into validated dictionary or returns error message."""
    if not raw_text or not raw_text.strip():
        return None, "Empty raw response from model"

    cleaned = raw_text.strip()
    if "{" in cleaned and "}" in cleaned:
        start_idx = cleaned.find("{")
        end_idx = cleaned.rfind("}")
        cleaned = cleaned[start_idx:end_idx + 1]

    try:
        data = json.loads(cleaned)
    except Exception as e:
        return None, f"Failed to parse JSON response: {str(e)}"

    if not isinstance(data, dict):
        return None, "Model response is not a JSON object"

    # Validate category
    cat = str(data.get("category", PhotoCategory.UNKNOWN)).upper()
    if cat not in PhotoCategory.ALL_CATEGORIES:
        cat = PhotoCategory.UNKNOWN
    data["category"] = cat

    # Validate macro_category
    macro = str(data.get("macro_category", MacroCategory.get_macro(cat))).upper()
    if macro not in MacroCategory.ALL_MACRO_CATEGORIES:
        macro = MacroCategory.get_macro(cat)
    data["macro_category"] = macro

    # Validate confidence & scores
    data["confidence"] = max(0.0, min(1.0, float(data.get("confidence", 0.5))))
    data["cover_score"] = max(0.0, min(100.0, float(data.get("cover_score", 50.0))))
    data["composition_score"] = max(0.0, min(100.0, float(data.get("composition_score", 50.0))))
    data["framing_score"] = max(0.0, min(100.0, float(data.get("framing_score", 50.0))))
    data["vehicle_visibility"] = max(0.0, min(1.0, float(data.get("vehicle_visibility", 0.8))))

    # Quality status
    qs = str(data.get("quality_status", "GOOD")).upper()
    if qs not in ("GOOD", "WARNING", "BAD"):
        qs = "GOOD"
    data["quality_status"] = qs

    # Suitable for cover check: Engine, Wheel, Key, Document, Interior CANNOT be suitable for cover!
    if cat in (
        PhotoCategory.ENGINE, PhotoCategory.WHEEL, PhotoCategory.KEY,
        PhotoCategory.DOCUMENT, PhotoCategory.TRUNK, PhotoCategory.INTERIOR_FRONT,
        PhotoCategory.INTERIOR_REAR, PhotoCategory.DASHBOARD, PhotoCategory.STEERING
    ):
        data["suitable_for_cover"] = False

    # Validate content_bbox_estimate
    bbox = data.get("content_bbox_estimate")
    if isinstance(bbox, dict) and all(k in bbox for k in ("x", "y", "width", "height")):
        if img_w > 0 and img_h > 0:
            bbox["x"] = max(0, min(int(bbox["x"]), img_w - 1))
            bbox["y"] = max(0, min(int(bbox["y"]), img_h - 1))
            bbox["width"] = max(1, min(int(bbox["width"]), img_w - bbox["x"]))
            bbox["height"] = max(1, min(int(bbox["height"]), img_h - bbox["y"]))
        data["content_bbox_estimate"] = bbox
    else:
        data["content_bbox_estimate"] = None

    # Validate plate_bbox
    plate_bbox = data.get("plate_bbox")
    if isinstance(plate_bbox, dict) and all(k in plate_bbox for k in ("x", "y", "width", "height")):
        if img_w > 0 and img_h > 0:
            plate_bbox["x"] = max(0, min(int(plate_bbox["x"]), img_w - 1))
            plate_bbox["y"] = max(0, min(int(plate_bbox["y"]), img_h - 1))
            plate_bbox["width"] = max(1, min(int(plate_bbox["width"]), img_w - plate_bbox["x"]))
            plate_bbox["height"] = max(1, min(int(plate_bbox["height"]), img_h - plate_bbox["y"]))
        data["plate_bbox"] = plate_bbox
        data["plate_visible"] = True
    else:
        data["plate_bbox"] = None
        data["plate_visible"] = False

    return data, None
