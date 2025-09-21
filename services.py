from typing import Optional, Dict, Any
try:
    from .client import make_request
    from .headers import build_runtime_headers
    from .sdk import SDK_META
except ImportError:
    from client import make_request
    from headers import build_runtime_headers
    from sdk import SDK_META


def _get_endpoint(*keys: str) -> str:
    ep = SDK_META.get("endpoints", {})
    for k in keys:
        if not isinstance(ep, dict) or k not in ep:
            path = "/".join(keys)
            raise ValueError(f"Endpoint path not configured in sdk_meta.json for '{path}'")
        ep = ep[k]
    if not isinstance(ep, str):
        path = "/".join(keys)
        raise ValueError(f"Endpoint leaf for '{path}' is not a string")
    return ep


def _require(data: Dict[str, Any], field: str, typ):
    if field not in data:
        raise ValueError(f"Missing required field: {field}")
    if typ is int and not isinstance(data[field], int):
        raise ValueError(f"Field '{field}' must be int")
    if typ is str and not isinstance(data[field], str):
        raise ValueError(f"Field '{field}' must be str")


def request_token(data: Dict[str, Any], headers: Optional[Dict[str, str]] = None, verify: bool = True):
    """POST /public/tokens (crear token)"""
    _require(data, "user_id", int)
    endpoint = _get_endpoint("tokens", "create")
    headers = headers or build_runtime_headers()
    return make_request(endpoint=endpoint, method="POST", headers=headers, data=data, verify=verify)


def token_status(data: Dict[str, Any], headers: Optional[Dict[str, str]] = None, verify: bool = True):
    """POST /public/tokens/status (estado del token)"""
    _require(data, "token", str)
    _require(data, "user_id", int)
    endpoint = _get_endpoint("tokens", "status")
    headers = headers or build_runtime_headers()
    return make_request(endpoint=endpoint, method="POST", headers=headers, data=data, verify=verify)


def request_otp(data: Dict[str, Any], headers: Optional[Dict[str, str]] = None, verify: bool = True):
    """POST /public/otp (generar/enviar OTP)"""
    _require(data, "user_id", int)
    endpoint = _get_endpoint("otp", "create")
    headers = headers or build_runtime_headers()
    return make_request(endpoint=endpoint, method="POST", headers=headers, data=data, verify=verify)


def validate_otp(data: Dict[str, Any], headers: Optional[Dict[str, str]] = None, verify: bool = True):
    """POST /public/otp/validate (validar OTP)"""
    _require(data, "otp_code", int)
    _require(data, "user_id", int)
    endpoint = _get_endpoint("otp", "validate")
    headers = headers or build_runtime_headers()
    return make_request(endpoint=endpoint, method="POST", headers=headers, data=data, verify=verify)
