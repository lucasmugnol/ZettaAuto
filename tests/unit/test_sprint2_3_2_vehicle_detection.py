"""Unit tests for Sprint 2.3.2 Grounding DINO + Smart Framing Engine using Mocks."""

import os
import tempfile
import pytest
from unittest.mock import MagicMock, patch

from automedia.core.models import (
    ImageAsset, VehicleBoundingBox, VehicleDetectionResult, PhotoCategory
)
from automedia.core.errors import ProcessingError
from automedia.providers.noop_vehicle_detector import NoOpVehicleDetector
from automedia.providers.grounding_dino_detector import GroundingDinoVehicleDetector
from automedia.providers.vehicle_detector_factory import VehicleDetectorFactory
from automedia.modules.smart_framing import SmartFramingEngine, FramingPlan


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
    # Ensure vehicle box (400..1400, 300..800) is completely inside crop_box
    c_x1, c_y1, c_x2, c_y2 = plan.crop_box
    assert c_x1 <= 400.0
    assert c_y1 <= 300.0
    assert c_x2 >= 1400.0
    assert c_y2 >= 800.0


@patch("PIL.Image.open")
@patch("transformers.AutoModelForZeroShotObjectDetection.from_pretrained")
@patch("transformers.AutoProcessor.from_pretrained")
def test_grounding_dino_detector_mocked_inference(mock_proc_cls, mock_model_cls, mock_img_open):
    # Setup mock image
    mock_img = MagicMock()
    mock_img.size = (1000, 800)
    mock_img_open.return_value.convert.return_value = mock_img

    # Setup mock processor & model
    mock_proc = MagicMock()
    mock_proc_cls.return_value = mock_proc

    mock_model = MagicMock()
    mock_model_cls.return_value = mock_model

    # Mock tensor boxes
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
