"""Manifest module for writing job metadata json atomically."""

import os
import json
from dataclasses import is_dataclass, asdict
from typing import Dict, Any, Optional


def _serialize(obj: Any) -> Any:
    if hasattr(obj, "to_dict") and callable(obj.to_dict):
        return obj.to_dict()
    if is_dataclass(obj):
        return asdict(obj)
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_serialize(v) for v in obj]
    return str(obj) if not isinstance(obj, (int, float, bool, type(None))) else obj


class ManifestWriter:
    def __init__(self, storage_provider=None):
        self.storage_provider = storage_provider

    def write_manifest(
        self,
        job_dir: Optional[str] = None,
        manifest_data: Optional[Dict[str, Any]] = None,
        job_id: Optional[str] = None,
        brand_cfg: Any = None,
        vehicle_data: Any = None,
        pipeline_cfg: Any = None,
        cover_selection: Any = None,
        valid_assets: Any = None,
        quality_map: Any = None,
        class_map: Any = None,
        dup_groups: Any = None,
        dup_removed: Any = None,
        coverage: Any = None,
        warnings: Any = None,
        job_output_dir: Optional[str] = None,
        job_status: Optional[str] = None,
        **kwargs
    ) -> str:
        target_dir = job_dir or job_output_dir or "."

        if manifest_data is None:
            cover_file = getattr(cover_selection, "selected_file", None) if cover_selection else None
            q_map_ser = {k: _serialize(v) for k, v in (quality_map or {}).items()}
            c_map_ser = {k: _serialize(v) for k, v in (class_map or {}).items()}
            status_val = job_status or kwargs.get("status") or "COMPLETED"

            manifest_data = {
                "job_id": job_id,
                "status": status_val,
                "brand_config": _serialize(brand_cfg),
                "vehicle_data": _serialize(vehicle_data),
                "pipeline_config": _serialize(pipeline_cfg),
                "cover_selection": _serialize(cover_selection),
                "selected_cover": cover_file,
                "selected_cover_file": cover_file,
                "photo_scores": q_map_ser,
                "photo_categories": c_map_ser,
                "duplicates": dup_removed or [],
                "quality_report": q_map_ser,
                "gallery_coverage": _serialize(coverage),
                "providers_used": {
                    "photo_analyzer": "local_photo_analyzer",
                    "photo_classifier": "local_photo_classifier",
                    "vision_provider": "hybrid"
                },
                "valid_assets_count": len(valid_assets) if valid_assets else 0,
                "duplicates_removed": dup_removed or [],
                "duplicate_groups": [_serialize(g) for g in (dup_groups or [])],
                "warnings": warnings or []
            }
        else:
            manifest_data = _serialize(manifest_data)
            if isinstance(manifest_data, dict):
                if "status" not in manifest_data:
                    manifest_data["status"] = job_status or "COMPLETED"
                if "selected_cover_file" not in manifest_data and "selected_cover" in manifest_data:
                    manifest_data["selected_cover_file"] = manifest_data["selected_cover"]

        manifest_path = os.path.join(target_dir, "manifest.json")
        tmp_path = manifest_path + ".tmp"

        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(manifest_data, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())

            # Validate serialization before replace
            with open(tmp_path, "r", encoding="utf-8") as f:
                json.load(f)

            os.replace(tmp_path, manifest_path)
            return manifest_path
        except Exception:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
            raise
