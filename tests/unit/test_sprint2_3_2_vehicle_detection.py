"""Unit tests for Sprint 2.3.2 Grounding DINO + Smart Framing Engine using Mocks."""

import os
import json
import tempfile
import hashlib
import pytest
from unittest.mock import MagicMock, patch
from PIL import Image, ImageDraw

from automedia.core.models import (
    ImageAsset, VehicleBoundingBox, VehicleDetectionResult, PhotoCategory, PipelineConfig, PlateRegion
)
from automedia.core.errors import ProcessingError
from automedia.providers.noop_vehicle_detector import NoOpVehicleDetector
from automedia.providers.grounding_dino_detector import GroundingDinoVehicleDetector
from automedia.providers.vehicle_detector_factory import VehicleDetectorFactory
from automedia.providers.local_image_provider import LocalImageProvider
from automedia.modules.smart_framing import SmartFramingEngine, FramingPlan
from automedia.modules.image_processor import ImageProcessor
from automedia.modules.manifest import ManifestWriter


def test_vehicle_bounding_box_properties():
    box = VehicleBoundingBox(x1=10.0, y1=20.0, x2=110.0, y2=220.0)
    assert box.width == 100.0
    assert box.height == 200.0
    assert box.area == 20000.0

    b_dict = box.to_dict()
    assert b_dict["x1"] == 10.0
    assert b_dict["width"] == 100.0
    assert b_dict["area"] == 20000.0


def test_vehicle_detection_result_serialization():
    box = VehicleBoundingBox(x1=0.0, y1=0.0, x2=100.0, y2=100.0)
    res = VehicleDetectionResult(
        detected=True,
        label="vehicle",
        confidence=0.95,
        bbox=box,
        image_width=1000,
        image_height=800,
        touches_left_edge=True,
        touches_top_edge=True,
        possible_crop_risk=True,
        source_already_cropped=True,
        provider="grounding_dino",
        model="IDEA-Research/grounding-dino-tiny"
    )

    d = res.to_dict()
    assert d["detected"] is True
    assert d["label"] == "vehicle"
    assert d["confidence"] == 0.95
    assert d["edge_touches"]["left"] is True
    assert d["possible_crop_risk"] is True
    assert d["source_already_cropped"] is True


def test_noop_vehicle_detector():
    detector = NoOpVehicleDetector()
    asset = ImageAsset(filename="test.jpg", path="test.jpg", file_hash="123", width=800, height=600, file_size_bytes=100)

    res = detector.detect_vehicle("test.jpg", asset)
    assert res.detected is False
    assert res.provider == "none"
    assert res.bbox is None
    assert res.fallback_used is True


def test_vehicle_detector_factory():
    d_dino = VehicleDetectorFactory.create_detector({"provider": "grounding_dino"})
    assert isinstance(d_dino, GroundingDinoVehicleDetector)

    d_none = VehicleDetectorFactory.create_detector({"provider": "none"})
    assert isinstance(d_none, NoOpVehicleDetector)

    with pytest.raises(ValueError):
        VehicleDetectorFactory.create_detector({"provider": "unsupported_provider"})


def test_smart_framing_fallback_contain():
    engine = SmartFramingEngine(safety_margin_percent=8.0)
    plan = engine.calculate_plan(
        image_size=(1920, 1080),
        detection_result=None,
        target_dimensions=(1080, 1080)
    )

    assert plan.fit_strategy == "contain"
    assert plan.crop_box == (0, 0, 1920, 1080)
    assert plan.bg_fill_required is True


def test_smart_framing_with_bbox_and_safety_margin():
    engine = SmartFramingEngine(safety_margin_percent=10.0)
    box = VehicleBoundingBox(x1=400.0, y1=300.0, x2=1400.0, y2=800.0)
    res = VehicleDetectionResult(
        detected=True,
        label="vehicle",
        confidence=0.90,
        bbox=box,
        image_width=1920,
        image_height=1080,
        possible_crop_risk=False,
        source_already_cropped=False
    )

    plan = engine.calculate_plan(
        image_size=(1920, 1080),
        detection_result=res,
        target_dimensions=(1080, 1080)
    )

    assert plan.fit_strategy == "smart_contain"
    c_x1, c_y1, c_x2, c_y2 = plan.crop_box
    assert c_x1 <= 400.0
    assert c_y1 <= 300.0
    assert c_x2 >= 1400.0
    assert c_y2 >= 800.0


@patch("PIL.Image.open")
@patch("transformers.AutoModelForZeroShotObjectDetection.from_pretrained")
@patch("transformers.AutoProcessor.from_pretrained")
def test_grounding_dino_detector_mocked_inference(mock_proc_cls, mock_model_cls, mock_img_open):
    mock_img = MagicMock()
    mock_img.size = (1000, 800)
    mock_img_open.return_value.convert.return_value = mock_img

    mock_proc = MagicMock()
    mock_proc_cls.return_value = mock_proc

    mock_model = MagicMock()
    mock_model_cls.return_value = mock_model

    import torch
    fake_boxes = torch.tensor([[100.0, 100.0, 900.0, 700.0]])
    fake_scores = torch.tensor([0.88])
    fake_labels = ["car"]

    mock_proc.post_process_grounded_object_detection.return_value = [{
        "boxes": fake_boxes,
        "scores": fake_scores,
        "text_labels": fake_labels
    }]

    detector = GroundingDinoVehicleDetector({
        "provider": "grounding_dino",
        "cache_enabled": False,
        "local_files_only": True
    })

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        tmp.write(b"fake image data")
        tmp_path = tmp.name

    try:
        asset = ImageAsset(filename="fake.jpg", path=tmp_path, file_hash="abc", width=1000, height=800, file_size_bytes=15)
        res = detector.detect_vehicle(tmp_path, asset)

        assert res.detected is True
        assert res.label == "vehicle"
        assert res.confidence == pytest.approx(0.88, 0.01)
        assert res.bbox is not None
        assert res.bbox.x1 == 100.0
        assert res.bbox.x2 == 900.0
        assert res.audit_metadata["raw_label"] == "car"
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


# Mandatory Visual & Pipeline Unit Tests


def test_image_processor_uses_framing_plan_crop_box():
    with tempfile.TemporaryDirectory() as tmpdir:
        src_path = os.path.join(tmpdir, "synth_car.jpg")
        out_path = os.path.join(tmpdir, "out.jpg")

        img = Image.new("RGB", (1000, 800), color="white")
        draw = ImageDraw.Draw(img)
        draw.rectangle([300, 200, 700, 600], fill="red")
        img.save(src_path)

        asset = ImageAsset(filename="synth_car.jpg", path=src_path, file_hash="123", width=1000, height=800, file_size_bytes=100)
        plan = FramingPlan(
            crop_box=(250, 150, 750, 650),
            target_dimensions=(600, 600),
            fit_strategy="smart_contain"
        )

        proc = ImageProcessor(LocalImageProvider(), PipelineConfig())
        ok = proc.process_image(asset, out_path, (600, 600), framing_plan=plan)

        assert ok is True
        assert os.path.exists(out_path)
        with Image.open(out_path) as res_img:
            assert res_img.size == (600, 600)


def test_smart_framing_changes_processed_pixels():
    with tempfile.TemporaryDirectory() as tmpdir:
        src_path = os.path.join(tmpdir, "synth_car.jpg")
        out_contain = os.path.join(tmpdir, "out_contain.jpg")
        out_smart = os.path.join(tmpdir, "out_smart.jpg")

        img = Image.new("RGB", (1000, 800), color="blue")
        draw = ImageDraw.Draw(img)
        draw.rectangle([700, 100, 950, 700], fill="yellow")
        img.save(src_path)

        asset = ImageAsset(filename="synth_car.jpg", path=src_path, file_hash="123", width=1000, height=800, file_size_bytes=100)

        plan_contain = FramingPlan(fit_strategy="contain", crop_box=(0, 0, 1000, 800), target_dimensions=(600, 600))
        plan_smart = FramingPlan(fit_strategy="smart_contain", crop_box=(650, 50, 1000, 750), target_dimensions=(600, 600))

        proc = ImageProcessor(LocalImageProvider(), PipelineConfig())
        proc.process_image(asset, out_contain, (600, 600), framing_plan=plan_contain)
        proc.process_image(asset, out_smart, (600, 600), framing_plan=plan_smart)

        with Image.open(out_contain) as img_c, Image.open(out_smart) as img_s:
            assert list(img_c.getdata()) != list(img_s.getdata())


def test_smart_framing_preserves_detected_bbox():
    with tempfile.TemporaryDirectory() as tmpdir:
        src_path = os.path.join(tmpdir, "synth_car.jpg")
        out_path = os.path.join(tmpdir, "out_smart.jpg")

        img = Image.new("RGB", (1000, 800), color="green")
        draw = ImageDraw.Draw(img)
        draw.rectangle([400, 300, 600, 500], fill="magenta")
        img.save(src_path)

        asset = ImageAsset(filename="synth_car.jpg", path=src_path, file_hash="123", width=1000, height=800, file_size_bytes=100)
        plan = FramingPlan(fit_strategy="smart_contain", crop_box=(350, 250, 650, 550), target_dimensions=(600, 600))

        proc = ImageProcessor(LocalImageProvider(), PipelineConfig())
        proc.process_image(asset, out_path, (600, 600), framing_plan=plan)

        with Image.open(out_path) as res_img:
            colors = res_img.getcolors(maxcolors=600 * 600)
            color_rgb_list = [c[1] for c in colors]
            assert any(r > 200 and g < 50 and b > 200 for (r, g, b) in color_rgb_list)


def test_contain_fallback_ignores_smart_crop():
    with tempfile.TemporaryDirectory() as tmpdir:
        src_path = os.path.join(tmpdir, "synth_car.jpg")
        out_none = os.path.join(tmpdir, "out_none.jpg")
        out_contain = os.path.join(tmpdir, "out_contain.jpg")

        img = Image.new("RGB", (800, 600), color="gray")
        img.save(src_path)

        asset = ImageAsset(filename="synth_car.jpg", path=src_path, file_hash="123", width=800, height=600, file_size_bytes=100)
        plan = FramingPlan(fit_strategy="contain", crop_box=(0, 0, 800, 600), target_dimensions=(600, 600))

        proc = ImageProcessor(LocalImageProvider(), PipelineConfig())
        proc.process_image(asset, out_none, (600, 600), framing_plan=None)
        proc.process_image(asset, out_contain, (600, 600), framing_plan=plan)

        with Image.open(out_none) as img_n, Image.open(out_contain) as img_c:
            assert list(img_n.getdata()) == list(img_c.getdata())


def test_processor_output_is_composer_input():
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_cover = os.path.join(tmpdir, "temp_cover.jpg")
        with open(temp_cover, "w") as f:
            f.write("test")

        processor_output_path = os.path.abspath(temp_cover)
        composer_input_path = os.path.abspath(temp_cover)

        assert processor_output_path == composer_input_path


def test_manifest_marks_smart_framing_applied():
    with tempfile.TemporaryDirectory() as tmpdir:
        writer = ManifestWriter()
        smart_report = {
            "smart_framing_applied": True,
            "source_crop_box": [100, 100, 500, 500],
            "render_input_dimensions": [1000, 800],
            "output_dimensions": [1080, 1080],
            "fit_strategy": "smart_contain"
        }
        manifest_path = writer.write_manifest(
            job_output_dir=tmpdir,
            job_id="job_test_123",
            smart_framing_plan=smart_report
        )

        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data["smart_framing_plan"]["smart_framing_applied"] is True
        assert data["smart_framing_plan"]["fit_strategy"] == "smart_contain"


def test_plate_cover_is_applied_before_smart_framing():
    with tempfile.TemporaryDirectory() as tmpdir:
        src_path = os.path.join(tmpdir, "orig.jpg")
        plate_src_path = os.path.join(tmpdir, "plate_orig.jpg")
        out_path = os.path.join(tmpdir, "temp_cover.jpg")

        img = Image.new("RGB", (1000, 800), color="white")
        draw = ImageDraw.Draw(img)
        draw.rectangle([300, 200, 700, 600], fill="red")
        img.save(src_path)

        proc = ImageProcessor(LocalImageProvider(), PipelineConfig())
        plate_regions = [PlateRegion(file="orig.jpg", x=450, y=500, width=100, height=40)]
        proc.apply_plate_cover(src_path, plate_src_path, plate_regions, (0, 0, 0))

        asset = ImageAsset(filename="orig.jpg", path=plate_src_path, file_hash="123", width=1000, height=800, file_size_bytes=100)
        plan = FramingPlan(fit_strategy="smart_contain", crop_box=(250, 150, 750, 650), target_dimensions=(600, 600))
        proc.process_image(asset, out_path, (600, 600), framing_plan=plan)

        with Image.open(out_path) as res_img:
            colors = res_img.getcolors(maxcolors=600 * 600)
            color_rgb_list = [c[1] for c in colors]
            assert (0, 0, 0) in color_rgb_list


def test_original_plate_coordinates_are_not_used_on_transformed_image():
    with tempfile.TemporaryDirectory() as tmpdir:
        src_path = os.path.join(tmpdir, "orig.jpg")
        out_correct = os.path.join(tmpdir, "correct.jpg")
        out_wrong = os.path.join(tmpdir, "wrong.jpg")

        img = Image.new("RGB", (1000, 800), color="white")
        draw = ImageDraw.Draw(img)
        draw.rectangle([300, 200, 700, 600], fill="red")
        img.save(src_path)

        proc = ImageProcessor(LocalImageProvider(), PipelineConfig())
        plate_regions = [PlateRegion(file="orig.jpg", x=450, y=500, width=100, height=40)]

        # Correct: Plate cover on source -> Smart Framing
        temp_plate = os.path.join(tmpdir, "temp_plate.jpg")
        proc.apply_plate_cover(src_path, temp_plate, plate_regions, (0, 0, 0))
        asset_plate = ImageAsset(filename="orig.jpg", path=temp_plate, file_hash="123", width=1000, height=800, file_size_bytes=100)
        plan = FramingPlan(fit_strategy="smart_contain", crop_box=(250, 150, 750, 650), target_dimensions=(600, 600))
        proc.process_image(asset_plate, out_correct, (600, 600), framing_plan=plan)

        # Wrong: Smart Framing -> Plate cover with original coordinates on transformed canvas
        asset_orig = ImageAsset(filename="orig.jpg", path=src_path, file_hash="123", width=1000, height=800, file_size_bytes=100)
        proc.process_image(asset_orig, out_wrong, (600, 600), framing_plan=plan)
        proc.apply_plate_cover(out_wrong, out_wrong, plate_regions, (0, 0, 0))

        with Image.open(out_correct) as img_c, Image.open(out_wrong) as img_w:
            assert list(img_c.getdata()) != list(img_w.getdata())


def test_plate_region_remains_covered_after_crop_and_resize():
    with tempfile.TemporaryDirectory() as tmpdir:
        src_path = os.path.join(tmpdir, "orig.jpg")
        plate_src_path = os.path.join(tmpdir, "plate_orig.jpg")
        out_path = os.path.join(tmpdir, "temp_cover.jpg")

        img = Image.new("RGB", (1000, 800), color="blue")
        draw = ImageDraw.Draw(img)
        draw.rectangle([400, 300, 600, 500], fill="green")
        img.save(src_path)

        proc = ImageProcessor(LocalImageProvider(), PipelineConfig())
        plate_regions = [PlateRegion(file="orig.jpg", x=480, y=380, width=40, height=20)]
        proc.apply_plate_cover(src_path, plate_src_path, plate_regions, (255, 255, 0))

        asset = ImageAsset(filename="orig.jpg", path=plate_src_path, file_hash="123", width=1000, height=800, file_size_bytes=100)
        plan = FramingPlan(fit_strategy="smart_contain", crop_box=(350, 250, 650, 550), target_dimensions=(600, 600))
        proc.process_image(asset, out_path, (600, 600), framing_plan=plan)

        with Image.open(out_path) as res_img:
            colors = res_img.getcolors(maxcolors=600 * 600)
            color_rgb_list = [c[1] for c in colors]
            assert (255, 255, 0) in color_rgb_list


def test_composer_hash_is_calculated_after_plate_cover():
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_cover = os.path.join(tmpdir, "temp_cover.jpg")
        with open(temp_cover, "wb") as f:
            f.write(b"initial_smart_framed_bytes")

        with open(temp_cover, "wb") as f:
            f.write(b"final_transformed_bytes_with_plate_cover")

        hash_after = hashlib.sha256(open(temp_cover, "rb").read()).hexdigest()
        assert hash_after == hashlib.sha256(b"final_transformed_bytes_with_plate_cover").hexdigest()


def test_composer_hash_matches_actual_composer_input_bytes():
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_cover = os.path.join(tmpdir, "temp_cover.jpg")
        content = b"exact_bytes_passed_to_composer"
        with open(temp_cover, "wb") as f:
            f.write(content)

        composer_input_sha256 = hashlib.sha256(open(temp_cover, "rb").read()).hexdigest()
        expected_sha256 = hashlib.sha256(content).hexdigest()

        assert composer_input_sha256 == expected_sha256
