Changelog

0.0.1 - Initial release
- First public SDK release for Python.
- Installation supported from GitHub:
  - Package name: `softan-connect`
  - Module import: `softan_connect`
- High-level services:
  - Tokens: `request_token`, `token_status`
  - OTP: `request_otp`, `validate_otp`
- CLI tools:
  - `softan-connect-install` (crea configuración base en stg)
  - `softan-connect-add-env` (agrega/actualiza prod)
  - `softan-connect-switch-env` (cambia entorno activo)
- Environments:
  - `stg` por defecto; `prod` gestionado vía CLI
  - Todas las llamadas usan el entorno activo automáticamente
- Headers estandarizados: `X-API-KEY`, `X-Connect-Info`, `X-Connect-SDK`
- TLS verificable: parámetro `verify` (por defecto True)
- Packaging:
  - `pyproject.toml` con console scripts
  - `sdk_meta.json` incluido como package data
- Tests:
  - Unit tests de validación de payloads y endpoints (sin red)

