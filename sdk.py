import json
import os
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent

# Static metadata packaged with the SDK
SDK_META_PATH = PACKAGE_ROOT / "sdk_meta.json"

# Default location for mutable config inside the consuming project
DEFAULT_CONFIG_DIR = Path.cwd() / "config" / "softan_connect"
DEFAULT_CONFIG_PATH = DEFAULT_CONFIG_DIR / "sdk_config.json"

# Allow overriding the config file location via env var
_config_override = os.getenv("SOFTAN_CONNECT_CONFIG_PATH")
if _config_override:
    SDK_CONFIG_PATH = Path(_config_override).expanduser()
else:
    SDK_CONFIG_PATH = DEFAULT_CONFIG_PATH


def load_json(path: Path):
    """Load JSON file, return {} if missing or invalid."""
    path = Path(path)
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError:
        return {}


# Static metadata (SDK-owned)
SDK_META = load_json(SDK_META_PATH)

# Defaults and install base URL
DEFAULT_ENV = SDK_META.get("default_environment", "stg")
BASE_URL_FOR_INSTALL = SDK_META.get("base_urls", {}).get(DEFAULT_ENV)

# User configuration (post-install)
SDK_CONFIG = load_json(SDK_CONFIG_PATH)

# Ensure active environment defaults to DEFAULT_ENV (stg) if missing
if "active_environment" not in SDK_CONFIG:
    SDK_CONFIG["active_environment"] = DEFAULT_ENV

ACTIVE_ENV = SDK_CONFIG.get("active_environment", DEFAULT_ENV)
ENVIRONMENTS = SDK_CONFIG.get("environments", {})
CURRENT_ENV_CONFIG = ENVIRONMENTS.get(ACTIVE_ENV, {})


def get_runtime_base_url():
    """Return base URL for the active environment (includes /public)."""
    env = SDK_CONFIG.get("active_environment", DEFAULT_ENV)
    return (SDK_META.get("base_urls", {}) or {}).get(env)

