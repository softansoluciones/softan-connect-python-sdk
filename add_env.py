import json
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



def main():
    print("\n???  Anadir/actualizar entorno 'prod' en el SDK")

    selected_env = "prod"
    base_urls = SDK_META.get("base_urls", {})
    if selected_env not in base_urls:
        print("? El entorno 'prod' no esta definido en sdk_meta.json > base_urls.")
        return

    app_identifier = SDK_CONFIG.get("app_identifier")
    email = SDK_CONFIG.get("developer_email")
    SDK_CONFIG.setdefault("environments", {})

    if not app_identifier or not email:
        print("? El archivo sdk_config.json no tiene informacion global valida.")
        return

    if selected_env in SDK_CONFIG["environments"]:
        opt = input("?? El entorno 'prod' ya existe. Deseas actualizarlo? (s/n): ").strip().lower()
        if opt not in ("s", "si", "y", "yes"):
            print("? Operacion cancelada. No se realizaron cambios.")
            return

    print(f"\n??  Configurando entorno: {selected_env}")
    api_key = input("?? API KEY (prod): ").strip()
    connect_info = input("?? X-Connect-Info (prod): ").strip()

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
        print("? Error en la respuesta de validacion:", response)
        return

    validation = response["Response"]
    if all(validation.get(k) for k in ["api-key", "connect-info", "sdk-key"]):
        print("? Validacion exitosa. Guardando configuracion...")

        SDK_CONFIG.setdefault("environments", {})
        SDK_CONFIG["environments"][selected_env] = {
            "api_key": api_key,
            "connect_info": connect_info,
            "connect_sdk": sdk_hash,
        }

        SDK_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with SDK_CONFIG_PATH.open("w", encoding="utf-8") as f:
            json.dump(SDK_CONFIG, f, indent=2)

        print(f"?? Entorno '{selected_env}' anadido/actualizado correctamente.")
        print("? Sugerencia: ejecuta 'softan-connect-switch-env' para cambiar el entorno activo.")
    else:
        print("? Validacion fallida. Resultado:")
        print(json.dumps(validation, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

