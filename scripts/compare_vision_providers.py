"""Vision Provider Comparative Evaluation Script (Sprint 2.3 Hardening Step 5 & 7).

Compares Heuristic Local Classifier vs. Gemini Multimodal Vision Provider
against human ground truth annotations on real vehicle photographs.
"""

import os
import sys
import json
import csv
import time
import argparse

from PIL import Image

from automedia.config_loader import load_dotenv, get_vision_provider_startup_status
from automedia.core.models import (
    MacroCategory, PhotoCategory, ImageAsset, PhotoQualityScore,
    PhotoClassificationResult, VehicleData
)
from automedia.modules.cover_selector import CoverSelector
from automedia.providers.vision_provider_factory import VisionProviderFactory
from automedia.providers.local_photo_classifier import LocalPhotoClassifier
from automedia.providers.local_photo_analyzer import LocalPhotoAnalyzer


def validate_ground_truth_schema(gt_data: dict, vehicle_folder: str) -> bool:
    required_top = ["vehicle_id", "reviewer", "photos", "expected_gallery_coverage", "human_cover_top_3"]
    for field in required_top:
        if field not in gt_data:
            raise ValueError(f"Ground truth in '{vehicle_folder}' missing required top-level field: '{field}'")
    return True


def run_vision_comparison(dataset_dir: str, output_dir: str, force_fresh: bool = False) -> dict:
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

    # Instantiate providers via Factory & Direct Ports
    gemini_provider = VisionProviderFactory.create_provider({**multimodal_config, "provider": "gemini"})
    heuristic_classifier = LocalPhotoClassifier()
    analyzer = LocalPhotoAnalyzer()
    cover_selector = CoverSelector()

    per_photo_results = []
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

        h_assets, h_quality_map, h_class_map = [], {}, {}
        m_assets, m_quality_map, m_class_map = [], {}, {}

        for fname, gt_info in gt_photos.items():
            img_path = os.path.join(images_dir, fname)
            if not os.path.exists(img_path):
                continue

            with Image.open(img_path) as img:
                w, h = img.size

            asset = ImageAsset(path=img_path, filename=fname, width=w, height=h, is_valid=True)
            real_cat = gt_info["category"]
            real_macro = gt_info["macro_category"]

            # 1. Heuristic Classification
            t0 = time.time()
            detailed_q = analyzer.analyze_quality(img_path, asset)
            h_res = heuristic_classifier.classify_photo(img_path, asset, detailed_q)
            h_lat = (time.time() - t0) * 1000.0

            h_cat = h_res.category
            h_macro = h_res.macro_category or MacroCategory.get_macro(h_cat)

            h_assets.append(asset)
            h_quality_map[fname] = detailed_q
            h_class_map[fname] = h_res

            eval_counts["heuristic"]["total_photos"] += 1
            eval_counts["heuristic"]["total_latency_ms"] += h_lat
            eval_counts["heuristic"]["total_calls"] += 1

            if h_cat == real_cat:
                eval_counts["heuristic"]["cat_correct"] += 1
            else:
                errors_heuristic.append({"vehicle_id": vehicle_id, "filename": fname, "predicted": h_cat, "real": real_cat})

            if h_macro == real_macro:
                eval_counts["heuristic"]["macro_correct"] += 1

            # 2. Multimodal Gemini Classification
            t0 = time.time()
            m_res = gemini_provider.analyze_image(img_path, asset)
            m_lat = m_res.latency_ms

            m_cat = m_res.category
            m_macro = m_res.macro_category or MacroCategory.get_macro(m_cat)

            m_assets.append(asset)
            m_quality_map[fname] = PhotoQualityScore(overall_score=m_res.composition_score, status=m_res.quality_status)
            m_class_map[fname] = PhotoClassificationResult(category=m_cat, macro_category=m_macro, confidence=m_res.confidence)

            eval_counts["multimodal"]["total_photos"] += 1
            eval_counts["multimodal"]["total_latency_ms"] += m_lat
            eval_counts["multimodal"]["total_calls"] += 1
            eval_counts["multimodal"]["estimated_cost_usd"] += m_res.estimated_cost_usd

            if m_res.inference_status == "CACHE_HIT":
                eval_counts["multimodal"]["cache_hits"] += 1
            if m_res.fallback_used:
                eval_counts["multimodal"]["fallbacks"] += 1

            if m_cat == real_cat:
                eval_counts["multimodal"]["cat_correct"] += 1
            else:
                errors_multimodal.append({"vehicle_id": vehicle_id, "filename": fname, "predicted": m_cat, "real": real_cat, "reason": m_res.reasoning_summary})

            if m_macro == real_macro:
                eval_counts["multimodal"]["macro_correct"] += 1

            per_photo_results.append({
                "vehicle_id": vehicle_id,
                "filename": fname,
                "ground_truth": {"category": real_cat, "macro_category": real_macro},
                "heuristic": {"category": h_cat, "macro_category": h_macro, "confidence": h_res.confidence, "latency_ms": round(h_lat, 2)},
                "multimodal": {
                    "category": m_cat, "macro_category": m_macro, "confidence": m_res.confidence,
                    "suitable_for_cover": m_res.suitable_for_cover, "cover_score": m_res.cover_score,
                    "status": m_res.inference_status, "fallback_used": m_res.fallback_used,
                    "latency_ms": round(m_lat, 2), "reasoning": m_res.reasoning_summary
                }
            })

        # Cover selection comparison for this vehicle
        vdata = VehicleData(manufacturer="Fiat", model="Mobi", year=2023, price="60.000")

        h_cover = cover_selector.select_cover(h_assets, h_quality_map, h_class_map, [], vdata)
        if human_top1 and h_cover.selected_file == human_top1:
            eval_counts["heuristic"]["top1_hits"] += 1
        if human_top3 and h_cover.selected_file in human_top3:
            eval_counts["heuristic"]["top3_hits"] += 1
        if h_class_map.get(h_cover.selected_file, PhotoClassificationResult()).macro_category == MacroCategory.EXTERIOR:
            eval_counts["heuristic"]["exterior_covers"] += 1

        m_cover = cover_selector.select_cover(m_assets, m_quality_map, m_class_map, [], vdata)
        if human_top1 and m_cover.selected_file == human_top1:
            eval_counts["multimodal"]["top1_hits"] += 1
        if human_top3 and m_cover.selected_file in human_top3:
            eval_counts["multimodal"]["top3_hits"] += 1
        if m_class_map.get(m_cover.selected_file, PhotoClassificationResult()).macro_category == MacroCategory.EXTERIOR:
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
            "estimated_cost_usd": round(cnt["estimated_cost_usd"], 6)
        }

    report = {
        "sprint_version": "2.3 - Measured Vision Provider Comparison",
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
        w.writerow(["Provider", "Category_Accuracy", "Macro_Accuracy", "Top1_Cover", "Top3_Cover", "Avg_Latency_ms", "Cache_Hits", "Fallbacks", "Est_Cost_USD"])
        hm = report["heuristic_provider"]
        mm = report["multimodal_provider"]
        w.writerow(["Heuristic_Local", hm["specific_category_accuracy_percent"], hm["macro_category_accuracy_percent"], hm["cover_top1_accuracy_percent"], hm["cover_top3_hit_rate_percent"], hm["average_latency_ms"], hm["cache_hits"], hm["total_fallbacks"], hm["estimated_cost_usd"]])
        w.writerow(["Gemini_Multimodal", mm["specific_category_accuracy_percent"], mm["macro_category_accuracy_percent"], mm["cover_top1_accuracy_percent"], mm["cover_top3_hit_rate_percent"], mm["average_latency_ms"], mm["cache_hits"], mm["total_fallbacks"], mm["estimated_cost_usd"]])

    with open(os.path.join(output_dir, "comparison_summary.md"), "w", encoding="utf-8") as f:
        f.write("# Measured Vision Provider Comparison (Sprint 2.3)\n\n")
        f.write("| Provider | Category Acc. | Macro Acc. | Top-1 Cover | Top-3 Cover | Avg Latency | Cache Hits | Fallbacks | Cost |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n")
        f.write(f"| **Heuristic Local** | {hm['specific_category_accuracy_percent']}% | {hm['macro_category_accuracy_percent']}% | {hm['cover_top1_accuracy_percent']}% | {hm['cover_top3_hit_rate_percent']}% | {hm['average_latency_ms']}ms | {hm['cache_hits']} | {hm['total_fallbacks']} | ${hm['estimated_cost_usd']} |\n")
        f.write(f"| **Gemini Multimodal** | {mm['specific_category_accuracy_percent']}% | {mm['macro_category_accuracy_percent']}% | {mm['cover_top1_accuracy_percent']}% | {mm['cover_top3_hit_rate_percent']}% | {mm['average_latency_ms']}ms | {mm['cache_hits']} | {mm['total_fallbacks']} | ${mm['estimated_cost_usd']} |\n\n")

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vision Provider Comparison Script")
    parser.add_argument("--dataset", default="./validation_real", help="Path to validation dataset")
    parser.add_argument("--output", default="./validation_reports/provider_comparison", help="Output directory")
    parser.add_argument("--force-fresh", action="store_true", help="Bypass cache")
    args = parser.parse_args()

    run_vision_comparison(args.dataset, args.output, args.force_fresh)
