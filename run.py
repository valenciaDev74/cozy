import sys
from PyQt6.QtWidgets import QApplication
from src.views.tray import SystemTray
from src.core.engine import Engine
from src.infrastructure.x11_adapter import X11DisplayAdapter
from src.core.calculator import GammaCalculator


def main():
    # init an engine, for now just x11
    try:
        engine = Engine(X11DisplayAdapter(), GammaCalculator())
    except Exception as e:
        print(f"Critical Error: {e}")
        sys.exit(1)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setQuitOnLastWindowClosed(False)

    tray = SystemTray(engine, parent=None)
    tray.show()

    # main loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
