"""Batch validation script for Sprint 2 - Real Lot Evaluation (5 vehicles x 15+ photos)."""

import os
import json
import time
import shutil
import tempfile
from PIL import Image, ImageDraw, ImageFilter
from automedia.pipeline import LocalPipeline
from automedia.core.models import VehicleData, BrandConfig, PipelineConfig


def generate_mock_vehicle_lot(base_dir: str):
    """Generates 5 synthetic vehicle folders each with 15 distinct photos."""
    vehicles_data = [
        {"id": "v1_corolla", "brand": "Toyota", "model": "Corolla XEi 2.0", "year": 2023, "price": "R$ 145.000"},
        {"id": "v2_civic", "brand": "Honda", "model": "Civic Touring 1.5 Turbo", "year": 2022, "price": "R$ 160.000"},
        {"id": "v3_compass", "brand": "Jeep", "model": "Compass Longitude 1.3T", "year": 2024, "price": "R$ 180.000"},
        {"id": "v4_onix", "brand": "Chevrolet", "model": "Onix Premier 1.0 Turbo", "year": 2023, "price": "R$ 89.900"},
        {"id": "v5_bmw320i", "brand": "BMW", "model": "320i M Sport 2.0", "year": 2024, "price": "R$ 310.000"}
    ]

    categories_templates = [
        ("front_3_4_main.jpg", (1200, 800), (40, 80, 160), "Exterior front 3/4"),
        ("front_direct.jpg", (1200, 800), (50, 90, 170), "Exterior front"),
        ("rear_3_4.jpg", (1200, 800), (45, 85, 165), "Exterior rear 3/4"),
        ("rear_direct.jpg", (1200, 800), (42, 82, 162), "Exterior rear"),
        ("left_side.jpg", (1200, 800), (48, 88, 168), "Exterior left side"),
        ("right_side.jpg", (1200, 800), (48, 88, 168), "Exterior right side"),
        ("interior_front.jpg", (1200, 800), (30, 30, 30), "Interior cabin"),
        ("interior_rear.jpg", (1200, 800), (25, 25, 25), "Rear seats"),
        ("dashboard.jpg", (1200, 800), (20, 20, 30), "Dashboard gauges"),
        ("steering_wheel.jpg", (1000, 1000), (15, 15, 15), "Steering wheel"),
        ("engine_bay.jpg", (1200, 800), (60, 60, 60), "Engine compartment"),
        ("trunk.jpg", (1200, 800), (35, 35, 35), "Trunk space"),
        ("wheel_detail.jpg", (800, 800), (50, 50, 55), "Alloy wheel close-up"),
        ("key_fob.jpg", (600, 600), (10, 10, 10), "Vehicle key"),
        ("duplicate_front_3_4.jpg", (1200, 800), (40, 80, 160), "Near duplicate of front 3/4"),
        ("dark_interior.jpg", (1200, 800), (5, 5, 5), "Too dark photo")
    ]

    lot_manifest = []

    for v in vehicles_data:
        v_dir = os.path.join(base_dir, "input_lots", v["id"])
        out_base = os.path.join(base_dir, "output_lots", v["id"])
        os.makedirs(v_dir, exist_ok=True)
        os.makedirs(out_base, exist_ok=True)

        for name, (w, h), color, desc in categories_templates:
            img_p = os.path.join(v_dir, name)
            img = Image.new("RGB", (w, h), color=color)
            draw = ImageDraw.Draw(img)
            # Add synthetic vehicle edges
            draw.rectangle([int(w*0.2), int(h*0.2), int(w*0.8), int(h*0.8)], outline=(255, 255, 255), width=4)
            draw.text((int(w*0.25), int(h*0.4)), f"{v['brand']} {v['model']} - {name}", fill=(255, 255, 255))
            img.save(img_p)

        # Write config files for this vehicle
        brand_p = os.path.join(v_dir, "brand.json")
        with open(brand_p, "w", encoding="utf-8") as f:
            json.dump({"company_name": f"{v['brand']} Dealer", "cta": "Fale conosco!"}, f)

        veh_p = os.path.join(v_dir, "vehicle.json")
        with open(veh_p, "w", encoding="utf-8") as f:
            json.dump({"manufacturer": v["brand"], "model": v["model"], "year": v["year"], "price": v["price"]}, f)

        pipe_p = os.path.join(v_dir, "pipeline.json")
        with open(pipe_p, "w", encoding="utf-8") as f:
            json.dump({"accepted_formats": [".jpg", ".jpeg"]}, f)

        lot_manifest.append({
            "id": v["id"],
            "input_dir": v_dir,
            "output_dir": out_base,
            "brand_path": brand_p,
            "vehicle_path": veh_p,
            "pipeline_path": pipe_p
        })

    return lot_manifest


def run_batch_validation():
    with tempfile.TemporaryDirectory() as tmpdir:
        lot_manifest = generate_mock_vehicle_lot(tmpdir)
        pipeline = LocalPipeline()

        report_summary = []

        for item in lot_manifest:
            t0 = time.time()
            job, res = pipeline.run(
                input_dir=item["input_dir"],
                output_dir=item["output_dir"],
                brand_config_path=item["brand_path"],
                vehicle_config_path=item["vehicle_path"],
                pipeline_config_path=item["pipeline_path"]
            )
            proc_time = time.time() - t0

            # Read manifest
            with open(res.manifest_file, "r", encoding="utf-8") as f:
                m_data = json.load(f)

            sel_cover = m_data["selected_cover"]
            sel_file = sel_cover["selected_file"]
            q_info = m_data["photo_scores"].get(sel_file, {})
            cat_info = m_data["photo_categories"].get(sel_file, {})

            report_summary.append({
                "vehicle_id": item["id"],
                "total_photos_processed": job.total_images,
                "job_status": job.status,
                "selected_cover_file": sel_file,
                "selected_cover_score": sel_cover["score"],
                "selected_cover_rank": sel_cover["rank"],
                "selected_cover_reason": sel_cover["reason"],
                "category": cat_info.get("category", "UNKNOWN"),
                "overall_quality_score": q_info.get("overall_score", 0.0),
                "processing_time_seconds": round(proc_time, 4),
                "duplicates_removed_count": len(m_data["duplicates"]["duplicate_removed"]),
                "gallery_coverage_score": m_data["gallery_coverage"]["coverage_score"]
            })

        print(json.dumps(report_summary, indent=2, ensure_ascii=False))
        return report_summary


if __name__ == "__main__":
    run_batch_validation()
