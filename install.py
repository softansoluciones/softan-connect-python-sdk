import json
import os
try:
    from .crypto import generate_sdk_header
    from .client import make_request
    from .sdk import *
    from .headers import build_validation_headers
except ImportError:
    from crypto import generate_sdk_header
    from client import make_request
    from sdk import *
    from headers import build_validation_headers


def install_sdk():
    print("\n🔧 Instalación Softan Connect SDK")

    # Paso 0: Definir entorno fijo (stg)
    env = "stg"
    print(f"🌐 Instalación inicial apuntará al entorno: {env}")

    # Paso 1: Obtener datos del usuario
    api_key = input("🔑 Ingresa tu API KEY: ").strip()
    connect_info = input("📦 Ingresa tu X-Connect-Info: ").strip()
    app_identifier = input("🔗 Ingresa tu App Identifier: ").strip()
    email = input("📧 Ingresa tu correo: ").strip()

    # Paso 2: Generar SDK Hash
    sdk_hash = generate_sdk_header(api_key, app_identifier)

    # Paso 3: Validar en el endpoint
    headers = build_validation_headers(api_key, connect_info, sdk_hash)
    validation_url = f"{BASE_URL_FOR_INSTALL.rstrip('/')}/developers/validate"

    print(f"🔍 Validando credenciales en: {validation_url}")
    # Forzar el uso de la base_url de instalación (stg) para evitar autodetección
    response = make_request(
        endpoint="developers/validate",
        method="POST",
        headers=headers,
        data=None,
        verbose=True,
        base_url_override=BASE_URL_FOR_INSTALL,
    )

    if not response or not isinstance(response.get("Response"), dict):
        print("❌ Error en la respuesta de validación:", response)
        return

    validation = response["Response"]
    if all(validation.get(k) for k in ["api-key", "connect-info", "sdk-key"]):
        print("✅ Validación exitosa. Guardando configuración...")

        # Preparar estructura del config
        config = {
            "developer_email": email,
            "app_identifier": app_identifier,
            "active_environment": env,
            "environments": {
                env: {
                    "api_key": api_key,
                    "connect_info": connect_info,
                    "connect_sdk": sdk_hash
                }
            }
        }

        with open(SDK_CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)

        print(f"🎉 SDK configurado correctamente para entorno '{env}'.")

    else:
        print("❌ Validación fallida. Resultado:")
        print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    install_sdk()
