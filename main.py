# main.py

try:
    from .client import make_request
    from .headers import build_runtime_headers
except ImportError:
    from client import make_request
    from headers import build_runtime_headers
import json

def main():
    print("🔧 Iniciando prueba de conexión con Softan Connect...\n")

    headers = build_runtime_headers()
    # El base_url ya incluye "/public"; el endpoint no debe repetirlo
    endpoint = "developers/validate"

    print("📡 Realizando petición al endpoint de validación...\n")
    response = make_request(endpoint, headers)

    print("✅ Resultado:")
    print(json.dumps(response, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
