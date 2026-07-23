"""Unit tests for Temp File Cleanup and Clean ZIP packaging."""

import os
import zipfile
import tempfile
from automedia.providers.local_storage_provider import LocalStorageProvider


def test_zip_content_clean_without_temp_logs_repo_files():
    provider = LocalStorageProvider()

    with tempfile.TemporaryDirectory() as tmpdir:
        job_dir = os.path.join(tmpdir, "job_clean_test")
        os.makedirs(os.path.join(job_dir, "photos"), exist_ok=True)
        os.makedirs(os.path.join(job_dir, "temp"), exist_ok=True)
        os.makedirs(os.path.join(job_dir, "logs"), exist_ok=True)
        os.makedirs(os.path.join(job_dir, "__pycache__"), exist_ok=True)

        # Create valid job output files
        with open(os.path.join(job_dir, "cover.jpg"), "w") as f:
            f.write("cover")
        with open(os.path.join(job_dir, "photos", "photo_01.jpg"), "w") as f:
            f.write("photo_01")
        with open(os.path.join(job_dir, "title.txt"), "w") as f:
            f.write("title")
        with open(os.path.join(job_dir, "manifest.json"), "w") as f:
            f.write("{}")

        # Create unwanted files that MUST NOT end up in ZIP
        with open(os.path.join(job_dir, "temp", "temp_cover.jpg"), "w") as f:
            f.write("temp")
        with open(os.path.join(job_dir, "logs", "app.log"), "w") as f:
            f.write("log")
        with open(os.path.join(job_dir, "manifest.json.tmp"), "w") as f:
            f.write("tmp")
        with open(os.path.join(job_dir, "__pycache__", "cached.pyc"), "w") as f:
            f.write("pyc")

        zip_path = os.path.join(job_dir, "vehicle_media_package.zip")
        provider.create_zip_archive(job_dir, zip_path)

        assert os.path.exists(zip_path)

        # Inspect ZIP archive contents
        with zipfile.ZipFile(zip_path, "r") as zf:
            namelist = zf.namelist()

        assert "cover.jpg" in namelist
        assert "photos/photo_01.jpg" in namelist or "photos\\photo_01.jpg" in namelist
        assert "title.txt" in namelist
        assert "manifest.json" in namelist

        # Assert unwanted files are excluded
        forbidden = [".tmp", "temp_cover", "app.log", "cached.pyc", ".venv", "__pycache__", "vehicle_media_package.zip"]
        for item in namelist:
            for forb in forbidden:
                assert forb not in item
