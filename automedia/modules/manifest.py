"""Manifest module for writing job metadata json atomically."""

import os
import json
from typing import Dict, Any


class ManifestWriter:
    def write_manifest(self, job_dir: str, manifest_data: Dict[str, Any]) -> str:
        manifest_path = os.path.join(job_dir, "manifest.json")
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
