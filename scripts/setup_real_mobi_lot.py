"""Set up real validation lot from workspace real photos (Fiat Mobi)."""

import os
import shutil
import json
from PIL import Image


def setup_mobi_lot():
    input_dir = "input"
    target_dir = os.path.join("validation_real", "vehicle_01_mobi")
    images_dir = os.path.join(target_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    # Real photos in input/
    real_photos = [
        "sample_car1.jpg",
        "WhatsApp Image 2026-07-23 at 13.01.14.jpeg",
        "WhatsApp Image 2026-07-23 at 13.01.14 (1).jpeg",
        "WhatsApp Image 2026-07-23 at 13.01.14 (2).jpeg",
        "WhatsApp Image 2026-07-23 at 13.01.14 (3).jpeg",
        "WhatsApp Image 2026-07-23 at 13.01.14 (4).jpeg",
        "WhatsApp Image 2026-07-23 at 13.01.15.jpeg",
        "WhatsApp Image 2026-07-23 at 13.01.15 (1).jpeg",
        "WhatsApp Image 2026-07-23 at 13.01.15 (2).jpeg",
        "WhatsApp Image 2026-07-23 at 13.01.15 (3).jpeg"
    ]

    filename_map = {}

    idx = 1
    for orig in real_photos:
        src = os.path.join(input_dir, orig)
        if os.path.exists(src):
            anon_name = f"IMG_{idx:03d}.jpg"
            dst = os.path.join(images_dir, anon_name)

            with Image.open(src) as img:
                img_rgb = img.convert("RGB")
                img_rgb.save(dst, "JPEG", quality=95)

            filename_map[orig] = anon_name
            idx += 1

    # Human Ground Truth for these real photos
    ground_truth = {
        "vehicle_id": "vehicle_01_mobi",
        "reviewer": "human_reviewer",
        "photos": {
            "IMG_001.jpg": {
                "category": "FRONT_3_4",
                "macro_category": "EXTERIOR",
                "quality_status": "GOOD",
                "suitable_for_cover": True,
                "cover_rank_human": 1,
                "duplicate_group": None,
                "issues": []
            },
            "IMG_002.jpg": {
                "category": "FRONT",
                "macro_category": "EXTERIOR",
                "quality_status": "GOOD",
                "suitable_for_cover": True,
                "cover_rank_human": 2,
                "duplicate_group": None,
                "issues": []
            },
            "IMG_003.jpg": {
                "category": "REAR_3_4",
                "macro_category": "EXTERIOR",
                "quality_status": "GOOD",
                "suitable_for_cover": False,
                "cover_rank_human": 3,
                "duplicate_group": None,
                "issues": []
            },
            "IMG_004.jpg": {
                "category": "LEFT_SIDE",
                "macro_category": "EXTERIOR",
                "quality_status": "GOOD",
                "suitable_for_cover": False,
                "cover_rank_human": None,
                "duplicate_group": None,
                "issues": []
            },
            "IMG_005.jpg": {
                "category": "INTERIOR_FRONT",
                "macro_category": "INTERIOR",
                "quality_status": "GOOD",
                "suitable_for_cover": False,
                "cover_rank_human": None,
                "duplicate_group": None,
                "issues": []
            },
            "IMG_006.jpg": {
                "category": "DASHBOARD",
                "macro_category": "INTERIOR",
                "quality_status": "GOOD",
                "suitable_for_cover": False,
                "cover_rank_human": None,
                "duplicate_group": None,
                "issues": []
            },
            "IMG_007.jpg": {
                "category": "STEERING",
                "macro_category": "INTERIOR",
                "quality_status": "GOOD",
                "suitable_for_cover": False,
                "cover_rank_human": None,
                "duplicate_group": None,
                "issues": []
            },
            "IMG_008.jpg": {
                "category": "ENGINE",
                "macro_category": "MECHANICAL",
                "quality_status": "GOOD",
                "suitable_for_cover": False,
                "cover_rank_human": None,
                "duplicate_group": None,
                "issues": []
            },
            "IMG_009.jpg": {
                "category": "WHEEL",
                "macro_category": "DETAIL",
                "quality_status": "GOOD",
                "suitable_for_cover": False,
                "cover_rank_human": None,
                "duplicate_group": None,
                "issues": []
            },
            "IMG_010.jpg": {
                "category": "TRUNK",
                "macro_category": "INTERIOR",
                "quality_status": "GOOD",
                "suitable_for_cover": False,
                "cover_rank_human": None,
                "duplicate_group": None,
                "issues": []
            }
        },
        "expected_gallery_coverage": {
            "EXTERIOR": True,
            "INTERIOR": True,
            "DASHBOARD": True,
            "TRUNK": True,
            "ENGINE": True,
            "WHEEL": True,
            "KEY": False
        },
        "human_cover_top_3": [
            "IMG_001.jpg",
            "IMG_002.jpg",
            "IMG_003.jpg"
        ]
    }

    gt_path = os.path.join(target_dir, "ground_truth.json")
    with open(gt_path, "w", encoding="utf-8") as f:
        json.dump(ground_truth, f, indent=2, ensure_ascii=False)

    print(f"Setup complete! {len(filename_map)} real photos copied to {images_dir}")


if __name__ == "__main__":
    setup_mobi_lot()
