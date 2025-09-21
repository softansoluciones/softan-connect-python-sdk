import json
import os
from sdk import SDK_CONFIG_PATH


def main():
    print("\n?? Cambiar entorno activo del SDK")

    if not os.path.exists(SDK_CONFIG_PATH):
        print("? No se encontró el archivo de configuración del SDK.")
        return

    with open(SDK_CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    environments = config.get("environments", {})
    active = config.get("active_environment")

    if not environments:
        print("? No hay entornos configurados en sdk_config.json.")
        return

    env_names = list(environments.keys())

    if len(env_names) == 1:
        print(f"? Solo existe el entorno '{env_names[0]}'. No hay otros para cambiar.")
        return

    if len(env_names) == 2 and active in env_names:
        other = [e for e in env_names if e != active][0]
        opt = input(f"?? El entorno activo es '{active}'. ¿Cambiar a '{other}'? (s/n): ").strip().lower()
        if opt in ("s", "si", "sí", "y", "yes"):
            config["active_environment"] = other
            with open(SDK_CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)
            print(f"\n? Entorno activo cambiado a: {other}")
        else:
            print("? No se realizaron cambios.")
        return

    print("\n?? Entornos disponibles:")
    for idx, name in enumerate(env_names, 1):
        marker = " (activo)" if name == active else ""
        print(f"  {idx}. {name}{marker}")

    try:
        choice = int(input("\n?? Elige un entorno (número): ").strip())
        selected_env = env_names[choice - 1]
    except (ValueError, IndexError):
        print("? Selección inválida.")
        return

    if selected_env == active:
        print(f"? '{selected_env}' ya es el entorno activo.")
        return

    config["active_environment"] = selected_env
    with open(SDK_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    print(f"\n? Entorno activo cambiado a: {selected_env}")


if __name__ == "__main__":
    main()

