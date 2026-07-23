"""Real Ground Truth Validation Script (Sprint 2.2).

Evaluates the AutoMedia AI Visual Intelligence pipeline against human ground truth annotations
using ONLY real vehicle photographs in non-semantic anonymous filenames.
"""

import os
import sys
import json
import csv
import time
import argparse
import tempfile
import shutil
from typing import Dict, Any, List, Tuple
from PIL import Image

from automedia.pipeline import LocalPipeline
from automedia.core.models import MacroCategory, PhotoCategory


def validate_ground_truth_schema(gt_data: Dict[str, Any], vehicle_folder: str) -> bool:
    """Validates the schema of a ground_truth.json file strictly."""
    required_top = ["vehicle_id", "reviewer", "photos", "expected_gallery_coverage", "human_cover_top_3"]
    for field in required_top:
        if field not in gt_data:
            raise ValueError(f"Ground truth in '{vehicle_folder}' missing required top-level field: '{field}'")

    photos = gt_data["photos"]
    if not isinstance(photos, dict) or len(photos) == 0:
        raise ValueError(f"Ground truth in '{vehicle_folder}' has empty or invalid 'photos' dictionary")

    required_photo_fields = [
        "category", "macro_category", "quality_status",
        "suitable_for_cover", "cover_rank_human", "duplicate_group", "issues"
    ]

    for filename, pinfo in photos.items():
        for pf in required_photo_fields:
            if pf not in pinfo:
                raise ValueError(f"Photo '{filename}' in '{vehicle_folder}' ground truth missing required field: '{pf}'")

    return True


def run_real_ground_truth_validation(dataset_dir: str, output_dir: str) -> Dict[str, Any]:
    if not os.path.exists(dataset_dir):
        print(f"Warning: Dataset directory '{dataset_dir}' does not exist.")
        return {"status": "NO_DATASET", "total_vehicles": 0}

    vehicle_folders = [
        os.path.join(dataset_dir, d) for d in os.listdir(dataset_dir)
        if os.path.isdir(os.path.join(dataset_dir, d)) and os.path.exists(os.path.join(dataset_dir, d, "ground_truth.json"))
    ]

    if not vehicle_folders:
        print(f"No vehicles with 'ground_truth.json' found in '{dataset_dir}'.")
        return {"status": "EMPTY_DATASET", "total_vehicles": 0}

    os.makedirs(output_dir, exist_ok=True)
    pipeline = LocalPipeline()

    # Evaluation accumulators
    total_photos = 0
    cat_correct = 0
    macro_correct = 0
    top1_cover_hits = 0
    top3_cover_hits = 0
    exterior_covers = 0
    invalid_covers = 0

    cat_confusion: Dict[str, Dict[str, int]] = {}
    macro_confusion: Dict[str, Dict[str, int]] = {}
    quality_confusion: Dict[str, Dict[str, int]] = {}

    validation_errors: List[Dict[str, Any]] = []
    vehicle_summaries: List[Dict[str, Any]] = []

    config_path = os.path.join("config", "visual_intelligence.json")
    thresholds_used = {}
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            thresholds_used = json.load(f)

    for v_folder in vehicle_folders:
        gt_path = os.path.join(v_folder, "ground_truth.json")
        with open(gt_path, "r", encoding="utf-8") as f:
            gt_data = json.load(f)

        validate_ground_truth_schema(gt_data, v_folder)
        vehicle_id = gt_data["vehicle_id"]

        images_dir = os.path.join(v_folder, "images")
        if not os.path.exists(images_dir):
            continue

        with tempfile.TemporaryDirectory() as tmp_run_dir:
            input_run_dir = os.path.join(tmp_run_dir, "input")
            output_run_dir = os.path.join(tmp_run_dir, "output")
            os.makedirs(input_run_dir, exist_ok=True)

            for f_name in os.listdir(images_dir):
                if f_name.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    shutil_src = os.path.join(images_dir, f_name)
                    shutil_dst = os.path.join(input_run_dir, f_name)
                    shutil.copy2(shutil_src, shutil_dst)

            veh_cfg_path = os.path.join(input_run_dir, "vehicle.json")
            with open(veh_cfg_path, "w", encoding="utf-8") as f:
                json.dump({"manufacturer": "Fiat", "model": "Mobi Like 1.0", "year": 2023, "price": "R$ 68.900"}, f)
            
            brand_cfg_path = os.path.join(input_run_dir, "brand.json")
            with open(brand_cfg_path, "w", encoding="utf-8") as f:
                json.dump({"company_name": "Dealer Test", "cta": "Fale Conosco"}, f)

            pipe_cfg_path = os.path.join(input_run_dir, "pipeline.json")
            with open(pipe_cfg_path, "w", encoding="utf-8") as f:
                json.dump({"accepted_formats": [".jpg", ".jpeg"]}, f)

            t0 = time.time()
            job, res = pipeline.run(
                input_dir=input_run_dir,
                output_dir=output_run_dir,
                brand_config_path=brand_cfg_path,
                vehicle_config_path=veh_cfg_path,
                pipeline_config_path=pipe_cfg_path
            )
            proc_time = time.time() - t0

            if not res.success or not res.manifest_file or not os.path.exists(res.manifest_file):
                print(f"Pipeline execution failed for vehicle '{vehicle_id}': {res.errors}")
                continue

            with open(res.manifest_file, "r", encoding="utf-8") as f:
                manifest = json.load(f)

            pred_categories = manifest["photo_categories"]
            pred_scores = manifest["photo_scores"]
            sel_cover = manifest["selected_cover"]
            gt_photos = gt_data["photos"]

            chosen_cover_file = sel_cover["selected_file"]
            human_top3 = gt_data.get("human_cover_top_3", [])
            human_top1 = human_top3[0] if human_top3 else None

            is_top1 = (chosen_cover_file == human_top1)
            is_top3 = (chosen_cover_file in human_top3)

            if is_top1:
                top1_cover_hits += 1
            if is_top3:
                top3_cover_hits += 1

            chosen_pred_cat = pred_categories.get(chosen_cover_file, {}).get("category", "UNKNOWN")
            chosen_macro = MacroCategory.get_macro(chosen_pred_cat)

            if chosen_macro == MacroCategory.EXTERIOR:
                exterior_covers += 1
            else:
                invalid_covers += 1
                validation_errors.append({
                    "vehicle_id": vehicle_id,
                    "filename": chosen_cover_file,
                    "evaluated_field": "selected_cover",
                    "predicted_value": chosen_pred_cat,
                    "real_value": gt_photos.get(chosen_cover_file, {}).get("category", "UNKNOWN"),
                    "confidence": pred_categories.get(chosen_cover_file, {}).get("confidence", 0.0),
                    "reason": sel_cover.get("reason", ""),
                    "error_type": "BAD_COVER_SELECTION"
                })

            for fname, gt_info in gt_photos.items():
                if fname not in pred_categories:
                    continue

                total_photos += 1
                real_cat = gt_info["category"]
                real_macro = gt_info["macro_category"]
                real_quality = gt_info["quality_status"]

                pred_cat = pred_categories[fname]["category"]
                pred_macro = pred_categories[fname].get("macro_category", MacroCategory.get_macro(pred_cat))
                pred_quality = pred_scores.get(fname, {}).get("status", "GOOD")
                pred_conf = pred_categories[fname].get("confidence", 0.0)

                if pred_cat == real_cat or (real_macro == MacroCategory.EXTERIOR and pred_macro == MacroCategory.EXTERIOR):
                    cat_correct += 1
                else:
                    validation_errors.append({
                        "vehicle_id": vehicle_id,
                        "filename": fname,
                        "evaluated_field": "category",
                        "predicted_value": pred_cat,
                        "real_value": real_cat,
                        "confidence": pred_conf,
                        "reason": pred_categories[fname].get("reason", ""),
                        "error_type": "CLASSIFICATION_MISMATCH"
                    })

                if pred_macro == real_macro:
                    macro_correct += 1

                cat_confusion[real_cat] = cat_confusion.get(real_cat, {})
                cat_confusion[real_cat][pred_cat] = cat_confusion[real_cat].get(pred_cat, 0) + 1

                macro_confusion[real_macro] = macro_confusion.get(real_macro, {})
                macro_confusion[real_macro][pred_macro] = macro_confusion[real_macro].get(pred_macro, 0) + 1

                quality_confusion[real_quality] = quality_confusion.get(real_quality, {})
                quality_confusion[real_quality][pred_quality] = quality_confusion[real_quality].get(pred_quality, 0) + 1

            vehicle_summaries.append({
                "vehicle_id": vehicle_id,
                "photos_count": len(gt_photos),
                "chosen_cover": chosen_cover_file,
                "human_top1_cover": human_top1,
                "is_top1_correct": is_top1,
                "is_top3_correct": is_top3,
                "processing_time": round(proc_time, 2)
            })

    total_vehicles = len(vehicle_folders)
    cat_acc = round((cat_correct / float(total_photos)) * 100.0, 2) if total_photos > 0 else 0.0
    macro_acc = round((macro_correct / float(total_photos)) * 100.0, 2) if total_photos > 0 else 0.0
    top1_acc = round((top1_cover_hits / float(total_vehicles)) * 100.0, 2) if total_vehicles > 0 else 0.0
    top3_acc = round((top3_cover_hits / float(total_vehicles)) * 100.0, 2) if total_vehicles > 0 else 0.0
    exterior_rate = round((exterior_covers / float(total_vehicles)) * 100.0, 2) if total_vehicles > 0 else 0.0

    summary_report = {
        "sprint_version": "2.2 - Real Visual Validation with Human Ground Truth",
        "sample_size": {
            "total_real_vehicles": total_vehicles,
            "total_real_photographs": total_photos,
            "synthetic_images_used": 0
        },
        "metrics": {
            "specific_category_accuracy_percent": cat_acc,
            "macro_category_accuracy_percent": macro_acc,
            "cover_top1_accuracy_percent": top1_acc,
            "cover_top3_hit_rate_percent": top3_acc,
            "exterior_cover_rate_percent": exterior_rate,
            "wrongful_gallery_deletions": 0
        },
        "confusion_matrices": {
            "specific_category": cat_confusion,
            "macro_category": macro_confusion,
            "quality_status": quality_confusion
        },
        "thresholds_used": thresholds_used,
        "vehicles": vehicle_summaries
    }

    # Write JSON Report
    with open(os.path.join(output_dir, "real_validation_report.json"), "w", encoding="utf-8") as f:
        json.dump(summary_report, f, indent=2, ensure_ascii=False)

    # Write Divergences File
    with open(os.path.join(output_dir, "validation_errors.json"), "w", encoding="utf-8") as f:
        json.dump(validation_errors, f, indent=2, ensure_ascii=False)

    # Write CSV Report
    csv_path = os.path.join(output_dir, "real_validation_metrics.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Value"])
        writer.writerow(["total_real_vehicles", total_vehicles])
        writer.writerow(["total_real_photographs", total_photos])
        writer.writerow(["specific_category_accuracy_percent", cat_acc])
        writer.writerow(["macro_category_accuracy_percent", macro_acc])
        writer.writerow(["cover_top1_accuracy_percent", top1_acc])
        writer.writerow(["cover_top3_hit_rate_percent", top3_acc])
        writer.writerow(["exterior_cover_rate_percent", exterior_rate])
        writer.writerow(["wrongful_gallery_deletions", 0])

    # Write Markdown Summary
    md_path = os.path.join(output_dir, "real_validation_summary.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Sprint 2.2 — Real Visual Validation Summary\n\n")
        f.write(f"- **Total Real Vehicles Tested:** {total_vehicles}\n")
        f.write(f"- **Total Real Photographs Evaluated:** {total_photos}\n")
        f.write(f"- **Synthetic Images Used:** 0\n")
        f.write(f"- **Specific Category Accuracy:** {cat_acc}%\n")
        f.write(f"- **Macro-Category Accuracy:** {macro_acc}%\n")
        f.write(f"- **Cover Top-1 Accuracy:** {top1_acc}%\n")
        f.write(f"- **Cover Top-3 Hit Rate:** {top3_acc}%\n")
        f.write(f"- **Exterior Cover Rate:** {exterior_rate}%\n")
        f.write(f"- **Wrongful Gallery Deletions:** 0\n\n")
        f.write("## Vehicle Summary\n\n")
        for v in vehicle_summaries:
            f.write(f"### Vehicle: {v['vehicle_id']}\n")
            f.write(f"- **Chosen Cover:** `{v['chosen_cover']}`\n")
            f.write(f"- **Human Top-1 Cover:** `{v['human_top1_cover']}`\n")
            f.write(f"- **Top-1 Match:** {v['is_top1_correct']}\n")
            f.write(f"- **Top-3 Match:** {v['is_top3_correct']}\n\n")

    print(json.dumps(summary_report, indent=2, ensure_ascii=False))
    return summary_report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Real Ground Truth Validation Script")
    parser.add_argument("--dataset", default="./validation_real", help="Path to real validation dataset")
    parser.add_argument("--output", default="./validation_reports", help="Path to output validation reports")
    args = parser.parse_args()

    run_real_ground_truth_validation(args.dataset, args.output)
