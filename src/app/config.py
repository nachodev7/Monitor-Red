"""
Gestión de configuración de la aplicación.
"""

import json
from pathlib import Path
from .logger import setup_logger

logger = setup_logger()

CONFIG_PATH = Path("config.json")


def load_config() -> dict:
    
    # Carga y valida la configuración desde config.json.
    
    if not CONFIG_PATH.exists():
        logger.error("config.json no encontrado")
        raise FileNotFoundError("config.json no encontrado")

    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        config = json.load(file)

    _validate_config(config)
    logger.info("Configuración cargada correctamente")
    return config


def _validate_config(config: dict) -> None:
    required_keys = {"mode", "interval_seconds", "hosts"}

    if not required_keys.issubset(config):
        raise ValueError("Configuración inválida")

    if config["mode"] not in {"simulation", "production"}:
        raise ValueError("Modo inválido")

    if not isinstance(config["hosts"], list) or not config["hosts"]:
        raise ValueError("Lista de hosts inválida")


def save_config(config: dict) -> None:
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)