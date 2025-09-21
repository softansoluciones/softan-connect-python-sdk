import base64
import json
import hashlib
import hmac
import time
from sdk import SDK_META


def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip('=')


def base64url_decode(data: str) -> bytes:
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)

# 🧾 Generar hash firmado para X-Connect-SDK
def generate_sdk_header(api_key: str, app_identifier: str):
    payload = json.dumps({
        "sdk_version": SDK_META["sdk_version"],
        "sdk_type": SDK_META["sdk_type"],
        "app_identifier": app_identifier,
        "timestamp": int(time.time())
    })
    payload_b64 = base64url_encode(payload.encode())
    sig = hmac.new(api_key.encode(), payload_b64.encode(), hashlib.sha256).digest()
    sig_b64 = base64url_encode(sig)
    return f"{payload_b64}.{sig_b64}"
