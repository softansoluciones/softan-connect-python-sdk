import requests
try:
    from .sdk import get_runtime_base_url
    from .headers import *
except ImportError:
    from sdk import get_runtime_base_url
    from headers import *


def post(endpoint, headers, body=None):
    url = f"{get_runtime_base_url().rstrip('/')}/{endpoint.lstrip('/')}"
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"? Error en POST {url}: {str(e)}")
        return None


def make_request(
    endpoint: str,
    headers: dict,
    method: str = "GET",
    data: dict = None,
    verbose: bool = True,
    base_url_override: str = None,
    verify: bool = True,
):
    """
    Cliente HTTP generico. Permite override de base_url (instalacion/alta entornos)
    y parametriza `verify` para controlar la verificacion TLS (True por defecto).
    """

    base_url = base_url_override or get_runtime_base_url()
    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    if verbose:
        print(f"\n?? URL: {url}")
        print("?? Headers:")
        for k, v in headers.items():
            print(f"   {k}: {v}")
        if data:
            print(f"?? Body:\n{data}\n")

    try:
        response = requests.request(
            method=method.upper(),
            url=url,
            headers=headers,
            json=data,
            verify=verify,
        )

        try:
            return response.json()
        except ValueError:
            return {"status_code": response.status_code, "raw": response.text}

    except requests.RequestException as e:
        return {"error": str(e)}
