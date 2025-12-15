
from tkinter import Tk
from .gui import MonitorApp
from .logger import setup_logger

logger = setup_logger()


def main():
    logger.info("Iniciando Monitor de Red")
    root = Tk()
    MonitorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
