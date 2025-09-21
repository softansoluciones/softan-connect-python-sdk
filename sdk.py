import json
import os

# Paths (relative to project root)
SDK_META_PATH = "sdk_meta.json"
SDK_CONFIG_PATH = "sdk_config.json"


def load_json(path: str):
    """Load JSON file, return {} if missing."""
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


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

