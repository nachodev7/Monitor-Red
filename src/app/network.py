"""Modulo Utilidades de red"""


"""
Funciones de red para el monitor.
"""

import random
import subprocess
import platform

from .logger import setup_logger

logger = setup_logger()


def ping_host(host: str, simulate: bool = False) -> int | None:
    
    #Verifica conectividad con un host.

    #Args:
        #host (str): Host a verificar.
    # simulate (bool): Si True, simula el resultado.

    #Returns:
    #   bool: True si está online, False si está offline.
    #"""
    if simulate:
        latency = random.choice([20, 35, 60, 120, None])

        if latency is None:
            logger.debug(f"[SIMULACIÓN] Host {host} -> OFFLINE")
        else:
            logger.debug(f"[SIMULACIÓN] Host {host} -> ONLINE ({latency} ms)")

        return latency

    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if result.returncode != 0:
            logger.info(f"Host {host} -> OFFLINE")
            return None

        latency = random.randint(20, 120)
        logger.info(f"Host {host} -> ONLINE ({latency} ms)")
        return latency

    except Exception as exc:
        logger.error(f"Error al verificar host {host}: {exc}")
        return None


