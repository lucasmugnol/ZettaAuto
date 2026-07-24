"""Grounding DINO vehicle detector provider using Hugging Face Transformers."""

import os
import time
import json
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from PIL import Image

from automedia.core.interfaces import IVehicleDetectorProvider
from automedia.core.models import ImageAsset, VehicleBoundingBox, VehicleDetectionResult


class GroundingDinoVehicleDetector(IVehicleDetectorProvider):
    """Zero-shot vehicle detector powered by IDEA-Research/grounding-dino-tiny via Transformers."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.model_id = self.config.get("model_id", "IDEA-Research/grounding-dino-tiny")
        self.local_model_path = self.config.get(
            "local_model_path", "models/grounding_dino/grounding-dino-tiny"
        )
        self.device = self.config.get("device", "cpu")
        self.box_threshold = float(self.config.get("box_threshold", 0.30))
        self.text_threshold = float(self.config.get("text_threshold", 0.25))
        self.prompts = self.config.get(
            "prompts", ["car", "pickup truck", "sport utility vehicle", "van"]
        )
        self.edge_tolerance_percent = float(self.config.get("edge_tolerance_percent", 2.5))
        self.cache_enabled = bool(self.config.get("cache_enabled", True))
        self.local_files_only = bool(self.config.get("local_files_only", True))
        self.cache_dir = Path("vehicle_detection_cache")

        if self.cache_enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

        self._processor = None
        self._model = None

    def _lazy_load_model(self):
        """Lazy load model and processor from local directory."""
        if self._model is not None and self._processor is not None:
            return

        from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection

        model_path = (
            self.local_model_path
            if os.path.exists(self.local_model_path)
            else self.model_id
        )

        try:
            self._processor = AutoProcessor.from_pretrained(
                model_path, local_files_only=self.local_files_only
            )
            self._model = AutoModelForZeroShotObjectDetection.from_pretrained(
                model_path, local_files_only=self.local_files_only
            )
            self._model.to(self.device)
            self._model.eval()
        except Exception as e:
            raise RuntimeError(
                f"Falha ao carregar Grounding DINO local de '{model_path}'. "
                f"Execute '.venv\\Scripts\\python.exe scripts\\setup_grounding_dino.py' primeiro. Erro: {e}"
            )

    def _calculate_file_sha256(self, file_path: str) -> str:
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()

    def detect_vehicle(
        self, image_path: str, asset: ImageAsset
    ) -> VehicleDetectionResult:
        """Detect vehicle in image and return detection result."""
        t0 = time.time()

        if not os.path.exists(image_path):
            return VehicleDetectionResult(
                detected=False,
                provider="grounding_dino",
                model=self.model_id,
                error=f"Arquivo não encontrado: '{image_path}'"
            )

        # Check local SHA256 cache
        file_hash = self._calculate_file_sha256(image_path)
        cache_file = self.cache_dir / f"{file_hash}.json"

        if self.cache_enabled and cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    cdata = json.load(f)
                bbox_dict = cdata.get("bbox")
                bbox = VehicleBoundingBox(**bbox_dict) if bbox_dict else None
                return VehicleDetectionResult(
                    detected=cdata.get("detected", False),
                    label=cdata.get("label", ""),
                    confidence=cdata.get("confidence", 0.0),
                    bbox=bbox,
                    image_width=cdata.get("image_width", 0),
                    image_height=cdata.get("image_height", 0),
                    touches_left_edge=cdata.get("edge_touches", {}).get("left", False),
                    touches_right_edge=cdata.get("edge_touches", {}).get("right", False),
                    touches_top_edge=cdata.get("edge_touches", {}).get("top", False),
                    touches_bottom_edge=cdata.get("edge_touches", {}).get("bottom", False),
                    possible_crop_risk=cdata.get("possible_crop_risk", False),
                    source_already_cropped=cdata.get("source_already_cropped", False),
                    provider="grounding_dino",
                    model=self.model_id,
                    latency_ms=(time.time() - t0) * 1000,
                    fallback_used=False,
                    detected_boxes_count=cdata.get("detected_boxes_count", 0),
                    audit_metadata=cdata.get("audit_metadata", {})
                )
            except Exception:
                pass # Cache read error, proceed to inference

        self._lazy_load_model()

        import torch

        image = Image.open(image_path).convert("RGB")
        img_w, img_h = image.size

        # Format prompt according to Hugging Face Grounding DINO documentation
        text_prompt = ". ".join(self.prompts) + "."

        inputs = self._processor(images=image, text=text_prompt, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self._model(**inputs)

        raw_results = self._processor.post_process_grounded_object_detection(
            outputs,
            inputs.input_ids,
            threshold=self.box_threshold,
            text_threshold=self.text_threshold,
            target_sizes=[(img_h, img_w)]
        )

        boxes = raw_results[0].get("boxes", [])
        scores = raw_results[0].get("scores", [])
        # GroundingDinoProcessor provides labels as strings or text_labels
        labels = raw_results[0].get("text_labels", raw_results[0].get("labels", []))

        detected_count = len(boxes)
        if detected_count == 0:
            res = VehicleDetectionResult(
                detected=False,
                image_width=img_w,
                image_height=img_h,
                provider="grounding_dino",
                model=self.model_id,
                latency_ms=(time.time() - t0) * 1000
            )
            self._write_cache(cache_file, res)
            return res

        # Rank bounding boxes combining confidence + area + centrality - edge penalty - tiny box penalty
        candidates = []
        center_x_img, center_y_img = img_w / 2.0, img_h / 2.0
        img_area = img_w * img_h

        for idx, (box, score, raw_lbl) in enumerate(zip(boxes, scores, labels)):
            x1, y1, x2, y2 = [float(val) for val in box.tolist()]

            # Clamp coordinates to image boundaries
            x1 = max(0.0, min(x1, float(img_w)))
            y1 = max(0.0, min(y1, float(img_h)))
            x2 = max(0.0, min(x2, float(img_w)))
            y2 = max(0.0, min(y2, float(img_h)))

            w = max(0.0, x2 - x1)
            h = max(0.0, y2 - y1)
            box_area = w * h
            area_ratio = box_area / img_area if img_area > 0 else 0.0

            # Distance from image center
            box_cx, box_cy = x1 + w / 2.0, y1 + h / 2.0
            dist_center = (((box_cx - center_x_img) / img_w) ** 2 + ((box_cy - center_y_img) / img_h) ** 2) ** 0.5
            centrality_score = max(0.0, 1.0 - dist_center)

            # Composite heuristic score
            conf = float(score)
            composite_score = (conf * 0.45) + (min(1.0, area_ratio * 1.5) * 0.35) + (centrality_score * 0.20)

            # Heavy penalty if area ratio < 5% (small detail box, e.g., wheel/handle)
            if area_ratio < 0.05:
                composite_score -= 0.40

            candidates.append({
                "idx": idx,
                "score": composite_score,
                "confidence": conf,
                "raw_label": str(raw_lbl),
                "bbox": VehicleBoundingBox(x1=x1, y1=y1, x2=x2, y2=y2),
                "area_ratio": area_ratio
            })

        # Sort candidate boxes descending by composite score
        candidates.sort(key=lambda c: c["score"], reverse=True)
        best = candidates[0]

        best_bbox = best["bbox"]
        x1, y1, x2, y2 = best_bbox.x1, best_bbox.y1, best_bbox.x2, best_bbox.y2

        # Check edge touch with edge_tolerance_percent (e.g., 2.5%)
        tol_w = img_w * (self.edge_tolerance_percent / 100.0)
        tol_h = img_h * (self.edge_tolerance_percent / 100.0)

        t_left = x1 <= tol_w
        t_right = (img_w - x2) <= tol_w
        t_top = y1 <= tol_h
        t_bottom = (img_h - y2) <= tol_h

        touches_count = sum([t_left, t_right, t_top, t_bottom])
        possible_crop_risk = touches_count > 0

        # source_already_cropped requires COMBINED strong signals (Item 4)
        w_ratio = best_bbox.width / img_w if img_w > 0 else 0
        h_ratio = best_bbox.height / img_h if img_h > 0 else 0
        source_already_cropped = (touches_count >= 2) or (touches_count >= 1 and (w_ratio > 0.85 or h_ratio > 0.85))

        res = VehicleDetectionResult(
            detected=True,
            label="vehicle", # Normalized internal label
            confidence=best["confidence"],
            bbox=best_bbox,
            image_width=img_w,
            image_height=img_h,
            touches_left_edge=t_left,
            touches_right_edge=t_right,
            touches_top_edge=t_top,
            touches_bottom_edge=t_bottom,
            possible_crop_risk=possible_crop_risk,
            source_already_cropped=source_already_cropped,
            provider="grounding_dino",
            model=self.model_id,
            latency_ms=(time.time() - t0) * 1000,
            fallback_used=False,
            detected_boxes_count=detected_count,
            audit_metadata={
                "raw_label": best["raw_label"],
                "composite_score": round(best["score"], 4),
                "area_ratio": round(best["area_ratio"], 4),
                "all_boxes_count": detected_count,
                "prompts_used": self.prompts
            }
        )

        self._write_cache(cache_file, res)
        return res

    def _write_cache(self, cache_file: Path, res: VehicleDetectionResult):
        if not self.cache_enabled:
            return
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(res.to_dict(), f, indent=2)
        except Exception:
            pass
