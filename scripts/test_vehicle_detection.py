"""Diagnostic script for vehicle detection on input dataset (Sprint 2.3.2)."""

import os
import sys
import time
import json
import argparse
import psutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, ".")

from automedia.core.models import ImageAsset
from automedia.providers.grounding_dino_detector import GroundingDinoVehicleDetector


def load_config():
    cfg_path = Path("config/visual_intelligence.json")
    if cfg_path.exists():
        with open(cfg_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def run_vehicle_detection_test(dataset_dir: str, output_dir: str):
    print("=" * 60)
    print("AutoMedia AI — Diagnostic Test: Grounding DINO Vehicle Detection")
    print(f"Dataset Input:  {dataset_dir}")
    print(f"Output Directory: {output_dir}")
    print("=" * 60)

    dataset_path = Path(dataset_dir)
    out_path = Path(output_dir)
    annotated_dir = out_path / "annotated"
    annotated_dir.mkdir(parents=True, exist_ok=True)

    if not dataset_path.exists():
        print(f"[ERRO] Pasta do dataset não encontrada: '{dataset_path}'")
        sys.exit(1)

    image_files = sorted(
        [f for f in dataset_path.glob("*") if f.suffix.lower() in (".jpg", ".jpeg", ".png")]
    )
    if not image_files:
        print(f"[AVISO] Nenhuma imagem (.jpg/.png) encontrada em '{dataset_path}'")
        sys.exit(0)

    print(f"Total de fotografias a processar: {len(image_files)}")

    # Load configuration
    cfg = load_config()
    detector_cfg = cfg.get("vehicle_detector", {})
    detector = GroundingDinoVehicleDetector(detector_cfg)

    report_items = []
    latencies = []
    process = psutil.Process(os.getpid())
    ram_before = process.memory_info().rss / (1024 * 1024)

    for idx, img_file in enumerate(image_files, start=1):
        filename = img_file.name
        img = Image.open(img_file).convert("RGB")
        asset = ImageAsset(
            filename=filename,
            path=str(img_file),
            file_hash="",
            width=img.width,
            height=img.height,
            file_size_bytes=img_file.stat().st_size
        )

        t0 = time.time()
        res = detector.detect_vehicle(str(img_file), asset)
        lat_ms = (time.time() - t0) * 1000
        latencies.append(lat_ms)

        # Draw bounding boxes using Pillow
        draw_img = img.copy()
        draw = ImageDraw.Draw(draw_img)

        bbox_dict = res.bbox.to_dict() if res.bbox else None

        if res.detected and res.bbox:
            box = res.bbox
            # Draw green rectangle for selected vehicle box
            draw.rectangle(
                [(box.x1, box.y1), (box.x2, box.y2)],
                outline="green",
                width=5
            )
            # Add text label
            lbl_text = f"VEHICLE {res.confidence:.2f} (CropRisk: {res.possible_crop_risk})"
            draw.text((box.x1 + 10, box.y1 + 10), lbl_text, fill="green")

        # Save annotated image
        annotated_file = annotated_dir / f"annotated_{filename}"
        draw_img.save(annotated_file)

        item = {
            "index": idx,
            "filename": filename,
            "detected": res.detected,
            "label": res.label,
            "confidence": round(res.confidence, 4),
            "bbox": bbox_dict,
            "image_dimensions": {"width": res.image_width, "height": res.image_height},
            "edge_touches": {
                "left": res.touches_left_edge,
                "right": res.touches_right_edge,
                "top": res.touches_top_edge,
                "bottom": res.touches_bottom_edge
            },
            "possible_crop_risk": res.possible_crop_risk,
            "source_already_cropped": res.source_already_cropped,
            "detected_boxes_count": res.detected_boxes_count,
            "latency_ms": round(lat_ms, 2),
            "annotated_image": str(annotated_file.relative_to(out_path)),
            "audit_metadata": res.audit_metadata
        }
        report_items.append(item)

        print(
            f"[{idx}/{len(image_files)}] {filename:<20} | Detected: {res.detected!s:<5} | "
            f"Conf: {res.confidence:.3f} | Latency: {lat_ms:6.1f}ms | CropRisk: {res.possible_crop_risk!s:<5}"
        )

    ram_after = process.memory_info().rss / (1024 * 1024)

    summary = {
        "dataset_dir": str(dataset_dir),
        "total_images": len(image_files),
        "detected_images": sum(1 for r in report_items if r["detected"]),
        "cold_latency_ms": round(latencies[0], 2) if latencies else 0.0,
        "average_warm_latency_ms": round(sum(latencies[1:]) / max(1, len(latencies) - 1), 2) if len(latencies) > 1 else round(latencies[0], 2),
        "ram_before_mb": round(ram_before, 2),
        "ram_after_mb": round(ram_after, 2),
        "detector_provider": detector_cfg.get("provider", "grounding_dino"),
        "model_id": detector_cfg.get("model_id", "IDEA-Research/grounding-dino-tiny"),
        "results": report_items
    }

    report_json_path = out_path / "detection_report.json"
    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("-" * 60)
    print(f"[SUCESSO] Relatório de diagnóstico gerado em: '{report_json_path}'")
    print(f"          Anotações visuais salvas em: '{annotated_dir}'")
    print(f"          Latência Fria: {summary['cold_latency_ms']} ms | Latência Quente Média: {summary['average_warm_latency_ms']} ms")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Diagnostic vehicle detection script.")
    parser.add_argument("--dataset", type=str, default="./input", help="Directory containing vehicle photos")
    parser.add_argument("--output", type=str, default="./validation_reports/vehicle_detection", help="Output directory for reports")
    args = parser.parse_args()

    run_vehicle_detection_test(args.dataset, args.output)
