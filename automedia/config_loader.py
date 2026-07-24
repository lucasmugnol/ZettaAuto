"""Environment configuration loader for AutoMedia AI."""

import os


def load_dotenv(dotenv_path: str = ".env") -> bool:
    """Loads environment variables from a .env file into os.environ if present."""
    if not os.path.exists(dotenv_path):
        return False

    try:
        with open(dotenv_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = val
        return True
    except Exception:
        return False


def get_vision_provider_startup_status() -> str:
    """Returns safe startup status summary for the configured vision provider."""
    load_dotenv()
    provider_name = os.environ.get("VISION_PROVIDER", "gemini").lower()
    has_key = bool(os.environ.get("GEMINI_API_KEY", "").strip())
    status_key = "configured" if has_key else "missing"
    return f"Vision provider: {provider_name}\nGemini API key: {status_key}"
