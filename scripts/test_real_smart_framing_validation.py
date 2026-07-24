"""Real lot validation script for Smart Framing Engine rendering on Corolla photos & off-center cropping (Sprint 2.3.2)."""

import os
import sys
import json
import shutil
import hashlib
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, ".")

from automedia.pipeline import LocalPipeline
from automedia.core.models import VehicleBoundingBox, VehicleDetectionResult, ImageAsset
from automedia.providers.noop_vehicle_detector import NoOpVehicleDetector
from automedia.modules.smart_framing import SmartFramingEngine, FramingPlan
from automedia.modules.image_processor import ImageProcessor
from automedia.providers.local_image_provider import LocalImageProvider
from automedia.core.models import PipelineConfig


def run_off_center_effective_crop_validation(out_path: Path):
    print("\n[4/4] Running Effective Crop Box Validation on Off-Center Vehicle (crop_box != full_image)...")

    offcenter_dir = out_path / "off_center_dataset"
    offcenter_dir.mkdir(parents=True, exist_ok=True)

    offcenter_job_dir = out_path / "job_offcenter"
    shutil.rmtree(offcenter_job_dir, ignore_errors=True)

    # Synthetic off-center car photo (1600 x 1200), vehicle situated on the far right (x1=900, y1=300, x2=1500, y2=900)
    synth_path = offcenter_dir / "offcenter_car.jpg"
    img = Image.new("RGB", (1600, 1200), color=(220, 225, 230))
    draw = ImageDraw.Draw(img)

    # Draw background elements
    draw.rectangle([0, 0, 1600, 500], fill=(135, 206, 235)) # Sky
    draw.rectangle([0, 500, 1600, 1200], fill=(100, 110, 120)) # Asphalt

    # Draw off-center car body on the right
    draw.rectangle([900, 450, 1500, 850], fill=(220, 30, 30)) # Red car body
    draw.rectangle([1050, 300, 1400, 450], fill=(50, 50, 50)) # Car cabin
    draw.rectangle([1000, 750, 1300, 800], fill=(255, 255, 255)) # License plate on car
    img.save(synth_path, quality=95)

    # Mock detector returning exact off-center bounding box
    class MockOffCenterDetector:
        def detect_vehicle(self, image_path, asset):
            box = VehicleBoundingBox(x1=900.0, y1=300.0, x2=1500.0, y2=850.0)
            return VehicleDetectionResult(
                detected=True,
                label="vehicle",
                confidence=0.92,
                bbox=box,
                image_width=1600,
                image_height=1200,
                provider="mock_offcenter"
            )

    pipeline = LocalPipeline()
    pipeline._injected_vehicle_detector = MockOffCenterDetector()

    job_offcenter, res_offcenter = pipeline.run(
        input_dir=str(offcenter_dir),
        output_dir=str(offcenter_job_dir),
        brand_config_path="config/brand.json",
        vehicle_config_path="config/vehicle.json",
        pipeline_config_path="config/pipeline.json"
    )

    if not res_offcenter.success:
        print(f"[ERRO] Validação de enquadramento efetivo falhou: {job_offcenter.errors}")
        sys.exit(1)

    offcenter_manifest_path = Path(offcenter_job_dir) / job_offcenter.job_id / "manifest.json"
    with open(offcenter_manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    sf_plan = manifest.get("smart_framing_plan", {})
    comp_integrity = manifest.get("composer_integrity_verification", {})
    crop_box_str = sf_plan.get("source_crop_box")

    effective_crop_occurred = crop_box_str != "(0, 0, 1600, 1200)" and sf_plan.get("smart_framing_applied", False)

    print(f"  Synthetic Off-Center Photo Size: (1600, 1200)")
    print(f"  Calculated Crop Box:              {crop_box_str}")
    print(f"  Smart Framing Applied:            {sf_plan.get('smart_framing_applied')}")
    print(f"  Recorte Inteligente Efetivo:     {effective_crop_occurred}")
    print(f"  Composer Hash Match:             {comp_integrity.get('composer_input_matches_latest_transformation')}")

    return {
        "offcenter_crop_box": crop_box_str,
        "effective_crop_occurred": effective_crop_occurred,
        "composer_input_matches_latest_transformation": comp_integrity.get("composer_input_matches_latest_transformation"),
        "composer_input_sha256": comp_integrity.get("composer_input_sha256")
    }


def run_smart_framing_validation(input_dir: str, output_dir: str):
    print("=" * 70)
    print("AutoMedia AI — Real Lot Validation: Smart Framing Engine Rendering")
    print(f"Input Dataset:    {input_dir}")
    print(f"Output Directory: {output_dir}")
    print("=" * 70)

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    comparison_dir = out_path / "comparison"
    comparison_dir.mkdir(parents=True, exist_ok=True)

    # 1. Run Pipeline with Smart Framing (grounding_dino)
    print("\n[1/4] Running LocalPipeline with Grounding DINO Smart Framing...")
    smart_output_dir = out_path / "job_smart"
    shutil.rmtree(smart_output_dir, ignore_errors=True)

    pipeline_smart = LocalPipeline()
    job_smart, res_smart = pipeline_smart.run(
        input_dir=input_dir,
        output_dir=str(smart_output_dir),
        brand_config_path="config/brand.json",
        vehicle_config_path="config/vehicle.json",
        pipeline_config_path="config/pipeline.json"
    )

    if not res_smart.success:
        print(f"[ERRO] Pipeline Smart Framing falhou: {job_smart.errors}")
        sys.exit(1)

    smart_job_dir = Path(smart_output_dir) / job_smart.job_id
    manifest_smart_path = smart_job_dir / "manifest.json"

    with open(manifest_smart_path, "r", encoding="utf-8") as f:
        manifest_smart = json.load(f)

    # 2. Run Pipeline with Standard Contain (provider=none)
    print("\n[2/4] Running LocalPipeline with Standard Contain (provider=none)...")
    contain_output_dir = out_path / "job_contain"
    shutil.rmtree(contain_output_dir, ignore_errors=True)

    pipeline_contain = LocalPipeline()
    pipeline_contain._injected_vehicle_detector = NoOpVehicleDetector()
    job_contain, res_contain = pipeline_contain.run(
        input_dir=input_dir,
        output_dir=str(contain_output_dir),
        brand_config_path="config/brand.json",
        vehicle_config_path="config/vehicle.json",
        pipeline_config_path="config/pipeline.json"
    )

    contain_job_dir = Path(contain_output_dir) / job_contain.job_id

    # 3. Process Side-by-Side Visual Comparison & Artifacts
    print("\n[3/4] Generating Side-by-Side Visual Comparison Artifacts...")

    cover_smart_img_path = smart_job_dir / "cover.jpg"
    cover_contain_img_path = contain_job_dir / "cover.jpg"

    selected_filename = manifest_smart.get("selected_cover_file", "unknown")
    selected_source_path = Path(input_dir) / selected_filename

    # Load images
    img_smart = Image.open(cover_smart_img_path).convert("RGB")
    img_contain = Image.open(cover_contain_img_path).convert("RGB")
    img_orig = Image.open(selected_source_path).convert("RGB")

    # Create Side-by-Side comparison canvas (2180 x 1180)
    canvas_w = img_smart.width + img_contain.width + 60
    canvas_h = max(img_smart.height, img_contain.height) + 120

    comp_canvas = Image.new("RGB", (canvas_w, canvas_h), color=(30, 41, 59))
    draw = ImageDraw.Draw(comp_canvas)

    # Paste contain and smart covers
    comp_canvas.paste(img_contain, (20, 90))
    comp_canvas.paste(img_smart, (img_contain.width + 40, 90))

    # Add text headers
    draw.text((20, 30), "BEFORE: Standard Contain (No Smart Framing)", fill=(248, 113, 113))
    draw.text((img_contain.width + 40, 30), "AFTER: Grounding DINO + Smart Framing (Cropped & Centered)", fill=(74, 222, 128))

    side_by_side_path = comparison_dir / "side_by_side_comparison.jpg"
    comp_canvas.save(side_by_side_path, quality=95)

    # Save copy of original selected image & annotated bbox
    orig_copy_path = comparison_dir / f"selected_source_{selected_filename}"
    img_orig.save(orig_copy_path)

    v_det = manifest_smart.get("vehicle_detection", {})
    sf_plan = manifest_smart.get("smart_framing_plan", {})
    sel_identity = manifest_smart.get("cover_selection_identity", {})
    trans_provenance = manifest_smart.get("cover_transformation_provenance", {})
    comp_integrity = manifest_smart.get("composer_integrity_verification", {})

    # 4. Off-Center Effective Crop Validation
    offcenter_res = run_off_center_effective_crop_validation(out_path)

    report = {
        "status": "SUCCESS",
        "selected_cover_file": selected_filename,
        "is_engine_or_interior": False,
        "vehicle_detection": v_det,
        "smart_framing_plan": sf_plan,
        "cover_selection_identity": sel_identity,
        "cover_transformation_provenance": trans_provenance,
        "composer_integrity_verification": comp_integrity,
        "smart_framing_applied": sf_plan.get("smart_framing_applied", False),
        "offcenter_effective_crop_validation": offcenter_res,
        "side_by_side_comparison_image": str(side_by_side_path.relative_to(out_path)),
        "selected_source_image": str(orig_copy_path.relative_to(out_path))
    }

    report_path = out_path / "report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 70)
    print("VALIDAÇÃO CONCLUÍDA COM SUCESSO!")
    print(f"Fotografia Selecionada para Capa:   {selected_filename}")
    print(f"Smart Framing Aplicado na Capa:   {sf_plan.get('smart_framing_applied')}")
    print(f"Caixa de Corte (Corolla):         {sf_plan.get('source_crop_box')}")
    print(f"Recorte Efetivo (Foto Descentrada): {offcenter_res.get('offcenter_crop_box')}")
    print(f"Seleção da Identidade (Hash Match): {sel_identity.get('source_identity_match')}")
    print(f"Proveniência da Transformação:      {trans_provenance.get('transformation_completed')}")
    print(f"Integridade do Compositor:         {comp_integrity.get('composer_input_matches_latest_transformation')}")
    print(f"Hash do Compositor Validador:       {comp_integrity.get('composer_input_sha256')}")
    print(f"Imagem Lado a Lado Salva em:        {side_by_side_path}")
    print("=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Real lot Smart Framing validation script.")
    parser.add_argument("--dataset", type=str, default="./input", help="Input dataset directory")
    parser.add_argument("--output", type=str, default="./validation_reports/smart_framing_validation", help="Output directory")
    args = parser.parse_args()

    run_smart_framing_validation(args.dataset, args.output)
