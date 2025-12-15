"""
Módulo para registrar eventos de red.
"""

from datetime import datetime
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "events.log"


def log_event(host: str, status: str) -> None:

#Registra un evento de estado de host.


    LOG_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} | {host} | {status}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(line)

def read_events() -> list[tuple[str, str, str]]:
    
#Lee los eventos del log y devuelve una lista de tuplas (timestamp, host, status)
    
    if not LOG_FILE.exists():
        return []

    events = []
    with open(LOG_FILE, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(" | ")
            if len(parts) == 3:
                events.append(tuple(parts))
    return events
