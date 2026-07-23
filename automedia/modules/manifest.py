"""Manifest module for writing job metadata json."""

import os
import json
from typing import Dict, Any
from automedia.core.models import Job


class ManifestWriter:
    def write_manifest(self, job_dir: str, manifest_data: Dict[str, Any]) -> str:
        manifest_path = os.path.join(job_dir, "manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=2, ensure_ascii=False)
        return manifest_path
