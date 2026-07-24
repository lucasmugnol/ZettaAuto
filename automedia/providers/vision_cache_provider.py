"""Local atomic JSON vision cache implementation."""

import os
import json
import hashlib
from typing import Dict, Any, Optional


class VisionCacheProvider:
    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = cache_dir
        self.cache_file = os.path.join(self.cache_dir, "vision_cache.json")
        os.makedirs(self.cache_dir, exist_ok=True)

    def _generate_key(
        self, image_path: str, provider: str, model: str, prompt_version: str
    ) -> str:
        try:
            with open(image_path, "rb") as f:
                img_bytes = f.read()
            img_hash = hashlib.sha256(img_bytes).hexdigest()
        except Exception:
            img_hash = hashlib.sha256(image_path.encode("utf-8")).hexdigest()

        composite_str = f"{img_hash}:{provider}:{model}:{prompt_version}"
        return hashlib.sha256(composite_str.encode("utf-8")).hexdigest()

    def get(
        self, image_path: str, provider: str, model: str, prompt_version: str
    ) -> Optional[Dict[str, Any]]:
        if not os.path.exists(self.cache_file):
            return None

        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            key = self._generate_key(image_path, provider, model, prompt_version)
            return data.get(key)
        except Exception:
            return None

    def set(
        self,
        image_path: str,
        provider: str,
        model: str,
        prompt_version: str,
        result_dict: Dict[str, Any]
    ) -> bool:
        try:
            current_data = {}
            if os.path.exists(self.cache_file):
                try:
                    with open(self.cache_file, "r", encoding="utf-8") as f:
                        current_data = json.load(f)
                except Exception:
                    current_data = {}

            key = self._generate_key(image_path, provider, model, prompt_version)
            current_data[key] = result_dict

            # Atomic write (.tmp + os.replace)
            tmp_file = f"{self.cache_file}.tmp"
            with open(tmp_file, "w", encoding="utf-8") as f:
                json.dump(current_data, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())

            os.replace(tmp_file, self.cache_file)
            return True
        except Exception:
            return False
