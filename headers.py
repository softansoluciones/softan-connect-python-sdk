try:
    from .sdk import SDK_CONFIG
except ImportError:
    from sdk import SDK_CONFIG


def build_validation_headers(api_key: str, connect_info: str, sdk_hash: str):
    return {
        "X-API-KEY": api_key,
        "X-Connect-Info": connect_info,
        "X-Connect-SDK": sdk_hash,
        "Content-Type": "application/json"
    }


def build_runtime_headers():
    env = SDK_CONFIG.get("active_environment")
    env_config = SDK_CONFIG.get("environments", {}).get(env, {})

    return {
        "X-API-KEY": env_config.get("api_key", ""),
        "X-Connect-Info": env_config.get("connect_info", ""),
        "X-Connect-SDK": env_config.get("connect_sdk", ""),
        "Content-Type": "application/json"
    }
