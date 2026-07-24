"""Vision Provider Comparative Evaluation Script (Sprint 2.3).

Compares Heuristic Local Classifier vs. Gemini Multimodal Vision Provider
against human ground truth annotations on real vehicle photographs.
"""

import os
import sys
import json
import csv
import time
import argparse
import tempfile
import shutil
from typing import Dict, Any, List
from PIL import Image

from automedia.pipeline import LocalPipeline
from automedia.core.models import MacroCategory, PhotoCategory, ImageAsset
from automedia.providers.gemini_vision_provider import GeminiVisionProvider
from automedia.providers.local_photo_classifier import LocalPhotoClassifier
from automedia.providers.local_photo_analyzer import LocalPhotoAnalyzer


def validate_ground_truth_schema(gt_data: Dict[str, Any], vehicle_folder: str) -> bool:
    required_top = ["vehicle_id", "reviewer", "photos", "expected_gallery_coverage", "human_cover_top_3"]
    for field in required_top:
        if field not in gt_data:
            raise ValueError(f"Ground truth in '{vehicle_folder}' missing required top-level field: '{field}'")
    return True


def run_vision_comparison(dataset_dir: str, output_dir: str):
    if not os.path.exists(dataset_dir):
        print(f"Warning: Dataset directory '{dataset_dir}' does not exist.")
        return

    vehicle_folders = [
        os.path.join(dataset_dir, d) for d in os.listdir(dataset_dir)
        if os.path.isdir(os.path.join(dataset_dir, d)) and os.path.exists(os.path.join(dataset_dir, d, "ground_truth.json"))
    ]

    if not vehicle_folders:
        print(f"No vehicles with 'ground_truth.json' found in '{dataset_dir}'.")
        return

    os.makedirs(output_dir, exist_ok=True)

    # Instantiate providers
    heuristic_classifier = LocalPhotoClassifier()
    analyzer = LocalPhotoAnalyzer()

    with open(os.path.join("config", "visual_intelligence.json"), "r", encoding="utf-8") as f:
        config_data = json.load(f)

    multimodal_config = config_data.get("vision_provider", {})
    gemini_provider = GeminiVisionProvider(multimodal_config)

    per_photo_results = []
    errors_heuristic = []
    errors_multimodal = []

    # Evaluation accumulators
    eval_counts = {
        "heuristic": {
            "cat_correct": 0, "macro_correct": 0, "top1_hits": 0, "top3_hits": 0,
            "exterior_covers": 0, "invalid_covers": 0, "total_photos": 0,
            "total_latency_ms": 0.0, "total_calls": 0, "cache_hits": 0, "estimated_cost_usd": 0.0
        },
        "multimodal": {
            "cat_correct": 0, "macro_correct": 0, "top1_hits": 0, "top3_hits": 0,
            "exterior_covers": 0, "invalid_covers": 0, "total_photos": 0,
            "total_latency_ms": 0.0, "total_calls": 0, "cache_hits": 0, "estimated_cost_usd": 0.0
        }
    }

    total_vehicles = len(vehicle_folders)

    for v_folder in vehicle_folders:
        gt_path = os.path.join(v_folder, "ground_truth.json")
        with open(gt_path, "r", encoding="utf-8") as f:
            gt_data = json.load(f)

        validate_ground_truth_schema(gt_data, v_folder)
        vehicle_id = gt_data["vehicle_id"]
        gt_photos = gt_data["photos"]
        human_top3 = gt_data.get("human_cover_top_3", [])
        human_top1 = human_top3[0] if human_top3 else None

        images_dir = os.path.join(v_folder, "images")
        if not os.path.exists(images_dir):
            continue

        for fname, gt_info in gt_photos.items():
            img_path = os.path.join(images_dir, fname)
            if not os.path.exists(img_path):
                continue

            with Image.open(img_path) as img:
                w, h = img.size

            asset = ImageAsset(path=img_path, filename=fname, width=w, height=h, is_valid=True)
            real_cat = gt_info["category"]
            real_macro = gt_info["macro_category"]

            # --- Provider 1: Heuristic Local ---
            t0 = time.time()
            detailed_q = analyzer.analyze_quality(img_path, asset)
            h_res = heuristic_classifier.classify_photo(img_path, asset, detailed_q)
            h_latency = (time.time() - t0) * 1000.0

            h_cat = h_res.category
            h_macro = h_res.macro_category or MacroCategory.get_macro(h_cat)

            eval_counts["heuristic"]["total_photos"] += 1
            eval_counts["heuristic"]["total_latency_ms"] += h_latency
            eval_counts["heuristic"]["total_calls"] += 1

            if h_cat == real_cat or (real_macro == MacroCategory.EXTERIOR and h_macro == MacroCategory.EXTERIOR):
                eval_counts["heuristic"]["cat_correct"] += 1
            else:
                errors_heuristic.append({
                    "vehicle_id": vehicle_id, "filename": fname,
                    "predicted": h_cat, "real": real_cat, "reason": h_res.reason
                })

            if h_macro == real_macro:
                eval_counts["heuristic"]["macro_correct"] += 1

            # --- Provider 2: Multimodal Gemini ---
            t0 = time.time()
            m_res = gemini_provider.analyze_image(img_path, asset)
            m_latency = m_res.latency_ms

            m_cat = m_res.category
            m_macro = m_res.macro_category or MacroCategory.get_macro(m_cat)

            eval_counts["multimodal"]["total_photos"] += 1
            eval_counts["multimodal"]["total_latency_ms"] += m_latency
            eval_counts["multimodal"]["total_calls"] += 1
            eval_counts["multimodal"]["estimated_cost_usd"] += m_res.estimated_cost_usd

            if m_res.inference_status == "CACHE_HIT":
                eval_counts["multimodal"]["cache_hits"] += 1

            if m_cat == real_cat or (real_macro == MacroCategory.EXTERIOR and m_macro == MacroCategory.EXTERIOR):
                eval_counts["multimodal"]["cat_correct"] += 1
            else:
                errors_multimodal.append({
                    "vehicle_id": vehicle_id, "filename": fname,
                    "predicted": m_cat, "real": real_cat, "reason": m_res.reasoning_summary
                })

            if m_macro == real_macro:
                eval_counts["multimodal"]["macro_correct"] += 1

            per_photo_results.append({
                "vehicle_id": vehicle_id,
                "filename": fname,
                "ground_truth": {"category": real_cat, "macro_category": real_macro},
                "heuristic": {"category": h_cat, "macro_category": h_macro, "confidence": h_res.confidence, "latency_ms": round(h_latency, 2)},
                "multimodal": {
                    "category": m_cat, "macro_category": m_macro, "confidence": m_res.confidence,
                    "suitable_for_cover": m_res.suitable_for_cover, "cover_score": m_res.cover_score,
                    "status": m_res.inference_status, "fallback_used": m_res.fallback_used,
                    "latency_ms": round(m_latency, 2), "reasoning": m_res.reasoning_summary
                }
            })

    # Consolidate comparison summary
    def calc_metrics(p_key: str) -> Dict[str, Any]:
        cnt = eval_counts[p_key]
        n_photos = max(1, cnt["total_photos"])
        n_calls = max(1, cnt["total_calls"])

        return {
            "specific_category_accuracy_percent": round((cnt["cat_correct"] / float(n_photos)) * 100.0, 2),
            "macro_category_accuracy_percent": round((cnt["macro_correct"] / float(n_photos)) * 100.0, 2),
            "average_latency_ms": round(cnt["total_latency_ms"] / float(n_calls), 2),
            "total_calls": cnt["total_calls"],
            "cache_hits": cnt["cache_hits"],
            "estimated_cost_usd": round(cnt["estimated_cost_usd"], 6)
        }

    comparison_report = {
        "sprint_version": "2.3 - Vision Provider Comparison",
        "sample_size": {
            "total_real_vehicles": total_vehicles,
            "total_real_photographs": eval_counts["heuristic"]["total_photos"]
        },
        "heuristic_provider": calc_metrics("heuristic"),
        "multimodal_provider": calc_metrics("multimodal")
    }

    # Write Outputs
    with open(os.path.join(output_dir, "comparison_report.json"), "w", encoding="utf-8") as f:
        json.dump(comparison_report, f, indent=2, ensure_ascii=False)

    with open(os.path.join(output_dir, "per_photo_predictions.json"), "w", encoding="utf-8") as f:
        json.dump(per_photo_results, f, indent=2, ensure_ascii=False)

    with open(os.path.join(output_dir, "errors_by_provider.json"), "w", encoding="utf-8") as f:
        json.dump({"heuristic": errors_heuristic, "multimodal": errors_multimodal}, f, indent=2, ensure_ascii=False)

    # CSV Summary
    with open(os.path.join(output_dir, "comparison_metrics.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Provider", "Category_Accuracy", "Macro_Accuracy", "Avg_Latency_ms", "Cache_Hits", "Est_Cost_USD"])
        h_m = comparison_report["heuristic_provider"]
        m_m = comparison_report["multimodal_provider"]
        w.writerow(["Heuristic_Local", h_m["specific_category_accuracy_percent"], h_m["macro_category_accuracy_percent"], h_m["average_latency_ms"], h_m["cache_hits"], h_m["estimated_cost_usd"]])
        w.writerow(["Gemini_Multimodal", m_m["specific_category_accuracy_percent"], m_m["macro_category_accuracy_percent"], m_m["average_latency_ms"], m_m["cache_hits"], m_m["estimated_cost_usd"]])

    # Markdown Summary
    with open(os.path.join(output_dir, "comparison_summary.md"), "w", encoding="utf-8") as f:
        f.write("# Vision Provider Comparison Summary (Sprint 2.3)\n\n")
        f.write("| Provider | Category Accuracy | Macro-Category Accuracy | Avg Latency (ms) | Cache Hits | Est. Cost (USD) |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :---: |\n")
        f.write(f"| **Heuristic Local** | {h_m['specific_category_accuracy_percent']}% | {h_m['macro_category_accuracy_percent']}% | {h_m['average_latency_ms']}ms | {h_m['cache_hits']} | ${h_m['estimated_cost_usd']} |\n")
        f.write(f"| **Gemini Multimodal** | {m_m['specific_category_accuracy_percent']}% | {m_m['macro_category_accuracy_percent']}% | {m_m['average_latency_ms']}ms | {m_m['cache_hits']} | ${m_m['estimated_cost_usd']} |\n\n")

    print(json.dumps(comparison_report, indent=2, ensure_ascii=False))
    return comparison_report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vision Provider Comparison Script")
    parser.add_argument("--dataset", default="./validation_real", help="Path to validation dataset")
    parser.add_argument("--output", default="./validation_reports/provider_comparison", help="Output directory")
    args = parser.parse_args()

    run_vision_comparison(args.dataset, args.output)
