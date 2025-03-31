# start_app.py
import subprocess
import sys
import time
from threading import Thread

from PySide6.QtWidgets import QApplication
from frontend.components.main_window import MainWindow


def run_backend():
    # Elindítjuk a backendet külön szálon
    subprocess.run(["uvicorn", "backend.main:app", "--reload"])



if __name__ == "__main__":
    # Először elindítjuk a backendet egy háttérszálon
    backend_thread = Thread(target=run_backend, daemon=True)
    backend_thread.start()

    # Kicsit várunk, hogy a backend elinduljon
    time.sleep(1.5)

    # Indítjuk a GUI-t
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
