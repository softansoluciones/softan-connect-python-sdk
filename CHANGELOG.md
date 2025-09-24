Changelog

0.0.2 - Config storage update
- Default install now writes `sdk_config.json` inside `config/softan_connect/`.
- CLI helpers create the directory before saving and keep working with the env var override.
- Tolerant JSON loader avoids crashes if the config is missing or corrupt.

0.0.1 - Initial release
- First public SDK release for Python.
- Installation supported from GitHub:
  - Package name: `softan-connect`
  - Module import: `softan_connect`
- High-level services:
  - Tokens: `request_token`, `token_status`
  - OTP: `request_otp`, `validate_otp`
- CLI tools:
  - `softan-connect-install` (crea configuracion base en stg)
  - `softan-connect-add-env` (agrega/actualiza prod)
  - `softan-connect-switch-env` (cambia entorno activo)
- Environments:
  - `stg` por defecto; `prod` gestionado via CLI
  - Todas las llamadas usan el entorno activo automaticamente
- Headers estandarizados: `X-API-KEY`, `X-Connect-Info`, `X-Connect-SDK`
- TLS verificable: parametro `verify` (por defecto True)
- Packaging:
  - `pyproject.toml` con console scripts
  - `sdk_meta.json` incluido como package data
- Tests:
  - Unit tests de validacion de payloads y endpoints (sin red)
