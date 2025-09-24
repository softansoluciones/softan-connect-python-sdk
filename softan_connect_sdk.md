# Softan Connect SDK (Python)

## Descripción
- SDK oficial para integrar aplicaciones con Softan Connect en Python.
- Expone funciones de alto nivel para crear y validar tokens y OTP.
- Incluye utilidades CLI para configurar credenciales y administrar entornos (stg/prod).

### Comandos CLI (referencia rápida)
| Comando                      | Propósito                                  |
|-----------------------------|---------------------------------------------|
| `softan-connect-install`    | Crear configuración inicial (stg)           |
| `softan-connect-add-env`    | Agregar/actualizar credenciales de `prod`   |
| `softan-connect-switch-env` | Cambiar entorno activo (stg/prod)           |

## Requisitos
- Python 3.9 o superior
- pip 21+

## Instalación
- Desde GitHub (origen único soportado)
Copiar y pegar:
```
pip install "git+https://github.com/softansoluciones/softan-connect-python-sdk.git"
```

### Instalación vía requirements.txt
- Agrega una de estas líneas a tu `requirements.txt` (copiar y pegar):
```
softan-connect @ git+https://github.com/softansoluciones/softan-connect-python-sdk.git
```
- (Recomendado) Fijar versión/tag específica:
Copiar y pegar:
```
softan-connect @ git+https://github.com/softansoluciones/softan-connect-python-sdk.git@v0.0.1
```

### Versionado
- Primer tag recomendado: `v0.0.1` (usado en los ejemplos anteriores).
- Instalación directa con versión fija (copiar y pegar):
```
pip install "git+https://github.com/softansoluciones/softan-connect-python-sdk.git@v0.0.1"
```

## Quickstart (3 pasos)
1) Instalar el SDK desde GitHub
Copiar y pegar:
```
pip install "git+https://github.com/softansoluciones/softan-connect-python-sdk.git@v0.0.1"
```
2) Crear configuración base (stg por defecto)
Copiar y pegar:
```
softan-connect-install
```
3) Usar en código (ejemplo: crear y consultar estado de token)
Copiar y pegar:
```python
from softan_connect import request_token, token_status

user_id = 12345
res_create = request_token({"user_id": user_id})

token = None
if isinstance(res_create, dict) and isinstance(res_create.get("Response"), dict):
    token = res_create["Response"].get("token")

if token:
    res_status = token_status({"token": token, "user_id": user_id})
    print(res_status)
else:
    print("No se obtuvo token en la creación. Revisa credenciales y entorno.")
```

## Primeros pasos (CLI)
- Instalar y crear la configuración (stg por defecto)
Copiar y pegar:
```
softan-connect-install
```
- Agregar/actualizar credenciales de producción
Copiar y pegar:
```
softan-connect-add-env
```
- Cambiar entorno activo (stg/prod)
Copiar y pegar:
```
softan-connect-switch-env
```

## Uso en código
Importa las funciones de alto nivel del paquete `softan_connect` y realiza llamadas según tu caso de uso.

Copiar y pegar:
```python
from softan_connect import request_token, token_status, request_otp, validate_otp

# Token: crear
res_create = request_token({"user_id": 12345})

# Token: estado
res_status = token_status({"token": "<TOKEN>", "user_id": 12345})

# OTP: crear
res_otp = request_otp({"user_id": 12345})

# OTP: validar
res_val = validate_otp({"otp_code": 123456, "user_id": 12345})
```

## Configuración
- Transparente para el usuario final: la configuración se gestiona automáticamente mediante los comandos CLI del SDK.
- No es necesario (ni recomendado) editar archivos de configuración manualmente ni versionarlos.

## Entornos
- Desarrollo: `stg` es el entorno por defecto.
- Producción: agrega credenciales con `softan-connect-add-env` y usa `softan-connect-switch-env` para activarlo.
- Todas las llamadas del SDK usan automáticamente el entorno activo para base URL y headers.

## Notas importantes
- TLS: la verificación está habilitada por defecto; si tu entorno stg presenta certificados no confiables, puedes pasar `verify=False` a las funciones de alto nivel por llamada (solo para desarrollo):
  - `request_token({...}, verify=False)`
- No incluyas `/public` en tus rutas; el SDK se encarga de la base URL.

## Solución de problemas
- 403 al llamar a tokens/otp: verifica que configuraste credenciales mediante los comandos CLI y que corresponden al entorno activo.
- 0 o 404: puede indicar datos inexistentes/inactivos o `user_id` inválido.

## Comandos disponibles
- `softan-connect-install` → Instala y configura el entorno `stg`.
- `softan-connect-add-env` → Agrega o actualiza credenciales de `prod`.
- `softan-connect-switch-env` → Cambia el entorno activo (stg/prod).

## Compatibilidad
- Python: 3.9+
- Sistemas: Windows, Linux, macOS

## Licencia
- Uso restringido a clientes/partners de Softan Soluciones y Code Builders House.

