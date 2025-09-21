try:
    from .sdk import SDK_META, SDK_CONFIG, SDK_CONFIG_PATH
    from .headers import build_validation_headers
    from .crypto import generate_sdk_header
    from .client import make_request
except ImportError:
    from sdk import SDK_META, SDK_CONFIG, SDK_CONFIG_PATH
    from headers import build_validation_headers
    from crypto import generate_sdk_header
    from client import make_request
import json


def main():
    print("\n???  Añadir/actualizar entorno 'prod' en el SDK")

    # Solo permitir agregar/actualizar 'prod'
    selected_env = "prod"
    base_urls = SDK_META.get("base_urls", {})
    if selected_env not in base_urls:
        print("? El entorno 'prod' no está definido en sdk_meta.json > base_urls.")
        return

    # Datos globales del config existente
    app_identifier = SDK_CONFIG.get("app_identifier")
    email = SDK_CONFIG.get("developer_email")
    SDK_CONFIG.setdefault("environments", {})

    if not app_identifier or not email:
        print("? El archivo sdk_config.json no tiene información global válida.")
        return

    # Si ya existe, ofrecer actualización
    if selected_env in SDK_CONFIG["environments"]:
        opt = input("?? El entorno 'prod' ya existe. ¿Deseas actualizarlo? (s/n): ").strip().lower()
        if opt not in ("s", "si", "sí", "y", "yes"):
            print("? Operación cancelada. No se realizaron cambios.")
            return

    print(f"\n??  Configurando entorno: {selected_env}")
    api_key = input("?? API KEY (prod): ").strip()
    connect_info = input("?? X-Connect-Info (prod): ").strip()

    # Generar SDK hash y validar
    sdk_hash = generate_sdk_header(api_key, app_identifier)
    headers = build_validation_headers(api_key, connect_info, sdk_hash)
    base_url = base_urls[selected_env]

    print("?? Validando credenciales (prod)...")
    response = make_request(
        "developers/validate",
        method="POST",
        headers=headers,
        base_url_override=base_url,
    )

    if not response or not isinstance(response.get("Response"), dict):
        print("? Error en la respuesta de validación:", response)
        return

    validation = response["Response"]
    if all(validation.get(k) for k in ["api-key", "connect-info", "sdk-key"]):
        print("? Validación exitosa. Guardando configuración...")

        SDK_CONFIG["environments"][selected_env] = {
            "api_key": api_key,
            "connect_info": connect_info,
            "connect_sdk": sdk_hash,
        }

        with open(SDK_CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(SDK_CONFIG, f, indent=2)

        print(f"?? Entorno '{selected_env}' añadido/actualizado correctamente.")
        print("? Sugerencia: ejecuta 'python switch_env.py' para cambiar el entorno activo.")
    else:
        print("? Validación fallida. Resultado:")
        print(json.dumps(validation, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
