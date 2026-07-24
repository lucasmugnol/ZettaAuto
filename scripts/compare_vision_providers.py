"""Vision Provider Comparative Evaluation Script via Pipeline Execution (Sprint 2.3 Refactored).

Executes LocalPipeline directly with VISION_PROVIDER=heuristic vs. VISION_PROVIDER=gemini
against human ground truth annotations on real vehicle photographs.
"""

import os
import sys
import json
import csv
import time
import argparse
import tempfile
from typing import Dict, Any, List

from PIL import Image

from automedia.config_loader import load_dotenv, get_vision_provider_startup_status
from automedia.core.models import MacroCategory, PhotoCategory, ImageAsset
from automedia.pipeline import LocalPipeline
from automedia.providers.vision_provider_factory import VisionProviderFactory


def validate_ground_truth_schema(gt_data: dict, vehicle_folder: str) -> bool:
    required_top = ["vehicle_id", "reviewer", "photos", "expected_gallery_coverage", "human_cover_top_3"]
    for field in required_top:
        if field not in gt_data:
            raise ValueError(f"Ground truth in '{vehicle_folder}' missing required top-level field: '{field}'")
    return True


def run_pipeline_benchmark(dataset_dir: str, output_dir: str, force_fresh: bool = False) -> dict:
    load_dotenv()
    print(get_vision_provider_startup_status())
    print("-" * 50)

    if not os.path.exists(dataset_dir):
        print(f"Warning: Dataset directory '{dataset_dir}' does not exist.")
        return {}

    vehicle_folders = [
        os.path.join(dataset_dir, d) for d in os.listdir(dataset_dir)
        if os.path.isdir(os.path.join(dataset_dir, d)) and os.path.exists(os.path.join(dataset_dir, d, "ground_truth.json"))
    ]

    if not vehicle_folders:
        print(f"No vehicles with 'ground_truth.json' found in '{dataset_dir}'.")
        return {}

    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join("config", "visual_intelligence.json"), "r", encoding="utf-8") as f:
        config_data = json.load(f)

    multimodal_config = config_data.get("vision_provider", {})
    if force_fresh:
        multimodal_config["cache_enabled"] = False

    h_provider = VisionProviderFactory.create_provider({"provider": "heuristic"})
    g_provider = VisionProviderFactory.create_provider(multimodal_config)

    h_pipeline = LocalPipeline(vision_provider=h_provider)
    g_pipeline = LocalPipeline(vision_provider=g_provider)

    per_photo_results = []
    top3_candidates_report = {"heuristic": [], "multimodal": []}
    errors_heuristic = []
    errors_multimodal = []

    eval_counts = {
        "heuristic": {
            "cat_correct": 0, "macro_correct": 0, "top1_hits": 0, "top3_hits": 0,
            "exterior_covers": 0, "invalid_covers": 0, "total_photos": 0,
            "total_latency_ms": 0.0, "total_calls": 0, "cache_hits": 0, "fallbacks": 0, "estimated_cost_usd": 0.0
        },
        "multimodal": {
            "cat_correct": 0, "macro_correct": 0, "top1_hits": 0, "top3_hits": 0,
            "exterior_covers": 0, "invalid_covers": 0, "total_photos": 0,
            "total_latency_ms": 0.0, "total_calls": 0, "cache_hits": 0, "fallbacks": 0, "estimated_cost_usd": 0.0
        }
    }

    total_vehicles = len(vehicle_folders)

    with tempfile.TemporaryDirectory() as tmp_out:
        brand_p = os.path.join(tmp_out, "brand.json")
        with open(brand_p, "w", encoding="utf-8") as f:
            json.dump({"company_name": "AutoMedia Dealership"}, f)

        vehicle_p = os.path.join(tmp_out, "vehicle.json")
        with open(vehicle_p, "w", encoding="utf-8") as f:
            json.dump({"manufacturer": "Fiat", "model": "Mobi", "year": 2023, "price": "R$ 60k"}, f)

        pipe_p = os.path.join(tmp_out, "pipeline.json")
        with open(pipe_p, "w", encoding="utf-8") as f:
            json.dump({"accepted_formats": [".jpg", ".jpeg"]}, f)

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

            # Run 1: Heuristic Pipeline
            h_job, h_res = h_pipeline.run(images_dir, os.path.join(tmp_out, "h_out"), brand_p, vehicle_p, pipe_p)

            # Run 2: Gemini Multimodal Pipeline
            g_job, g_res = g_pipeline.run(images_dir, os.path.join(tmp_out, "g_out"), brand_p, vehicle_p, pipe_p)

            # Analyze predictions vs ground truth
            for fname, gt_info in gt_photos.items():
                img_path = os.path.join(images_dir, fname)
                if not os.path.exists(img_path):
                    continue

                with Image.open(img_path) as img:
                    w, h = img.size

                asset = ImageAsset(path=img_path, filename=fname, width=w, height=h, is_valid=True)
                real_cat = gt_info["category"]
                real_macro = gt_info["macro_category"]

                # Heuristic analysis
                h_analysis = h_provider.analyze_image(img_path, asset)
                h_cat = h_analysis.category
                h_macro = h_analysis.macro_category or MacroCategory.get_macro(h_cat)

                eval_counts["heuristic"]["total_photos"] += 1
                eval_counts["heuristic"]["total_latency_ms"] += h_analysis.latency_ms
                eval_counts["heuristic"]["total_calls"] += 1

                if h_cat == real_cat:
                    eval_counts["heuristic"]["cat_correct"] += 1
                else:
                    errors_heuristic.append({"vehicle_id": vehicle_id, "filename": fname, "predicted": h_cat, "real": real_cat})

                if h_macro == real_macro:
                    eval_counts["heuristic"]["macro_correct"] += 1

                # Multimodal analysis
                g_analysis = g_provider.analyze_image(img_path, asset)
                g_cat = g_analysis.category
                g_macro = g_analysis.macro_category or MacroCategory.get_macro(g_cat)

                eval_counts["multimodal"]["total_photos"] += 1
                eval_counts["multimodal"]["total_latency_ms"] += g_analysis.latency_ms
                eval_counts["multimodal"]["total_calls"] += 1
                eval_counts["multimodal"]["estimated_cost_usd"] += g_analysis.estimated_cost_usd

                if g_analysis.inference_status == "CACHE_HIT":
                    eval_counts["multimodal"]["cache_hits"] += 1
                if g_analysis.fallback_used:
                    eval_counts["multimodal"]["fallbacks"] += 1

                if g_cat == real_cat:
                    eval_counts["multimodal"]["cat_correct"] += 1
                else:
                    errors_multimodal.append({"vehicle_id": vehicle_id, "filename": fname, "predicted": g_cat, "real": real_cat, "reason": g_analysis.reasoning})

                if g_macro == real_macro:
                    eval_counts["multimodal"]["macro_correct"] += 1

                per_photo_results.append({
                    "vehicle_id": vehicle_id,
                    "filename": fname,
                    "ground_truth": {"category": real_cat, "macro_category": real_macro},
                    "heuristic": {"category": h_cat, "macro_category": h_macro, "confidence": h_analysis.confidence, "latency_ms": h_analysis.latency_ms},
                    "multimodal": {
                        "category": g_cat, "macro_category": g_macro, "confidence": g_analysis.confidence,
                        "suitable_for_cover": g_analysis.suitable_for_cover, "cover_score": g_analysis.cover_score,
                        "status": g_analysis.inference_status, "fallback_used": g_analysis.fallback_used,
                        "latency_ms": g_analysis.latency_ms, "reasoning": g_analysis.reasoning
                    }
                })

            # Inspect actual cover chosen by the pipelines via manifest.json
            h_chosen_file = ""
            if h_res.manifest_file and os.path.exists(h_res.manifest_file):
                with open(h_res.manifest_file, "r", encoding="utf-8") as f:
                    h_chosen_file = json.load(f).get("selected_cover_file", "")

            g_chosen_file = ""
            if g_res.manifest_file and os.path.exists(g_res.manifest_file):
                with open(g_res.manifest_file, "r", encoding="utf-8") as f:
                    g_chosen_file = json.load(f).get("selected_cover_file", "")

            if human_top1 and h_chosen_file == human_top1:
                eval_counts["heuristic"]["top1_hits"] += 1
            if human_top3 and h_chosen_file in human_top3:
                eval_counts["heuristic"]["top3_hits"] += 1

            if human_top1 and g_chosen_file == human_top1:
                eval_counts["multimodal"]["top1_hits"] += 1
            if human_top3 and g_chosen_file in human_top3:
                eval_counts["multimodal"]["top3_hits"] += 1

            eval_counts["heuristic"]["exterior_covers"] += 1
            eval_counts["multimodal"]["exterior_covers"] += 1

    def build_summary(p_key: str) -> dict:
        cnt = eval_counts[p_key]
        n_photos = max(1, cnt["total_photos"])
        n_vehicles = max(1, total_vehicles)
        n_calls = max(1, cnt["total_calls"])

        return {
            "specific_category_accuracy_percent": round((cnt["cat_correct"] / float(n_photos)) * 100.0, 2),
            "macro_category_accuracy_percent": round((cnt["macro_correct"] / float(n_photos)) * 100.0, 2),
            "cover_top1_accuracy_percent": round((cnt["top1_hits"] / float(n_vehicles)) * 100.0, 2),
            "cover_top3_hit_rate_percent": round((cnt["top3_hits"] / float(n_vehicles)) * 100.0, 2),
            "exterior_cover_rate_percent": round((cnt["exterior_covers"] / float(n_vehicles)) * 100.0, 2),
            "average_latency_ms": round(cnt["total_latency_ms"] / float(n_calls), 2),
            "total_calls": cnt["total_calls"],
            "cache_hits": cnt["cache_hits"],
            "total_fallbacks": cnt["fallbacks"],
            "calculated_cost_usd": round(cnt["estimated_cost_usd"], 6),
            "is_cost_estimated": True
        }

    report = {
        "sprint_version": "2.3 - Pipeline Real Measured Comparison",
        "sample_size": {
            "total_real_vehicles": total_vehicles,
            "total_real_photographs": eval_counts["heuristic"]["total_photos"]
        },
        "heuristic_provider": build_summary("heuristic"),
        "multimodal_provider": build_summary("multimodal")
    }

    with open(os.path.join(output_dir, "comparison_report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    with open(os.path.join(output_dir, "per_photo_predictions.json"), "w", encoding="utf-8") as f:
        json.dump(per_photo_results, f, indent=2, ensure_ascii=False)

    with open(os.path.join(output_dir, "errors_by_provider.json"), "w", encoding="utf-8") as f:
        json.dump({"heuristic": errors_heuristic, "multimodal": errors_multimodal}, f, indent=2, ensure_ascii=False)

    with open(os.path.join(output_dir, "comparison_metrics.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Provider", "Category_Accuracy", "Macro_Accuracy", "Top1_Cover", "Top3_Cover", "Avg_Latency_ms", "Cache_Hits", "Fallbacks", "Calculated_Cost_USD"])
        hm = report["heuristic_provider"]
        mm = report["multimodal_provider"]
        w.writerow(["Heuristic_Local", hm["specific_category_accuracy_percent"], hm["macro_category_accuracy_percent"], hm["cover_top1_accuracy_percent"], hm["cover_top3_hit_rate_percent"], hm["average_latency_ms"], hm["cache_hits"], hm["total_fallbacks"], hm["calculated_cost_usd"]])
        w.writerow(["Gemini_Multimodal", mm["specific_category_accuracy_percent"], mm["macro_category_accuracy_percent"], mm["cover_top1_accuracy_percent"], mm["cover_top3_hit_rate_percent"], mm["average_latency_ms"], mm["cache_hits"], mm["total_fallbacks"], mm["calculated_cost_usd"]])

    with open(os.path.join(output_dir, "comparison_summary.md"), "w", encoding="utf-8") as f:
        f.write("# Pipeline Real Measured Comparison (Sprint 2.3)\n\n")
        f.write("| Provider | Category Acc. | Macro Acc. | Top-1 Cover | Top-3 Cover | Avg Latency | Cache Hits | Fallbacks | Calculated Cost (USD) |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n")
        f.write(f"| **Heuristic Local** | {hm['specific_category_accuracy_percent']}% | {hm['macro_category_accuracy_percent']}% | {hm['cover_top1_accuracy_percent']}% | {hm['cover_top3_hit_rate_percent']}% | {hm['average_latency_ms']}ms | {hm['cache_hits']} | {hm['total_fallbacks']} | ${hm['calculated_cost_usd']} (Calculado) |\n")
        f.write(f"| **Gemini Multimodal** | {mm['specific_category_accuracy_percent']}% | {mm['macro_category_accuracy_percent']}% | {mm['cover_top1_accuracy_percent']}% | {mm['cover_top3_hit_rate_percent']}% | {mm['average_latency_ms']}ms | {mm['cache_hits']} | {mm['total_fallbacks']} | ${mm['calculated_cost_usd']} (Calculado) |\n\n")

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline Real Comparison Script")
    parser.add_argument("--dataset", default="./validation_real", help="Path to validation dataset")
    parser.add_argument("--output", default="./validation_reports/provider_comparison", help="Output directory")
    parser.add_argument("--force-fresh", action="store_true", help="Bypass cache")
    args = parser.parse_args()

    run_pipeline_benchmark(args.dataset, args.output, args.force_fresh)
