"""Exporter module for organizing final artifacts in output directory."""

import os
from typing import List, Tuple, Dict, Any, Optional
from automedia.core.interfaces import IStorageProvider
from automedia.core.errors import ExportError, CoverFailureError


class Exporter:
    def __init__(self, storage_provider: IStorageProvider):
        self.storage = storage_provider

    def prepare_job_output(self, base_output_path: str, job_id: str) -> str:
        return self.storage.create_job_directory(base_output_path, job_id)

    def export_text_artifacts(self, job_dir: str, title: str, description: str) -> Tuple[str, str]:
        title_path = os.path.join(job_dir, "title.txt")
        desc_path = os.path.join(job_dir, "description.txt")

        self.storage.save_file(title_path, title.encode("utf-8"))
        self.storage.save_file(desc_path, description.encode("utf-8"))

        return title_path, desc_path

    def package_final_output(self, job_dir: str) -> str:
        cover_path = os.path.join(job_dir, "cover.jpg")
        if not os.path.exists(cover_path):
            raise CoverFailureError("Cannot create final ZIP: cover.jpg is missing or failed.")

        zip_path = os.path.join(job_dir, "vehicle_media_package.zip")
        return self.storage.create_zip_archive(job_dir, zip_path)
