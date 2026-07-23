"""Local storage provider implementation."""

import os
import shutil
import zipfile
from automedia.core.interfaces import IStorageProvider
from automedia.core.errors import ExportError


class LocalStorageProvider(IStorageProvider):
    def create_job_directory(self, base_output_path: str, job_id: str) -> str:
        job_dir = os.path.join(base_output_path, job_id)
        photos_dir = os.path.join(job_dir, "photos")
        os.makedirs(photos_dir, exist_ok=True)
        return job_dir

    def save_file(self, destination_path: str, content: bytes) -> str:
        try:
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            with open(destination_path, "wb") as f:
                f.write(content)
            return destination_path
        except Exception as e:
            raise ExportError(f"Failed to save file '{destination_path}': {str(e)}")

    def create_zip_archive(self, folder_path: str, zip_output_path: str) -> str:
        try:
            os.makedirs(os.path.dirname(zip_output_path), exist_ok=True)
            with zipfile.ZipFile(zip_output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        # Do not include the zip itself inside the zip if created in the same folder
                        if full_path == zip_output_path:
                            continue
                        arcname = os.path.relpath(full_path, folder_path)
                        zipf.write(full_path, arcname)
            return zip_output_path
        except Exception as e:
            raise ExportError(f"Failed to create ZIP archive '{zip_output_path}': {str(e)}")
