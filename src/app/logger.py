"""

Configuracion de logs para consola y archivo.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "monitor.log"


def setup_logger() -> logging.Logger:
    """
    Configura y devuelve el logger principal de la aplicación.
    """
    logger = logging.getLogger("monitor_red")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Archivo rotativo
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=1_000_000, backupCount=3
    )
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
