from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtGui import QAction, QIcon
import threading
from src.utils import smooth_transition


class SystemTray(QSystemTrayIcon):
    def __init__(self, engine, parent=None):
        icon = QIcon.fromTheme("display-brightness-symbolic")
        if icon.isNull():
            icon = QIcon.fromTheme("computer")

        super().__init__(icon, parent)

        self.engine = engine
        self.parent_window = parent
        self.menu = QMenu(parent)

        self.act_info = QAction("Cozy Monitor v1.0", self)
        self.act_info.setEnabled(False)
        self.menu.addAction(self.act_info)

        self.menu.addSeparator()

        self.act_activate = QAction("Activate Night Mode", self)
        self.act_activate.setCheckable(True)
        self.act_activate.setChecked(False)
        self.act_activate.triggered.connect(self.on_toggle_click)
        self.menu.addAction(self.act_activate)

        self.menu.addSeparator()

        self.act_quit = QAction("Quit", self)
        self.act_quit.triggered.connect(self.secure_quit)
        self.menu.addAction(self.act_quit)

        self.setContextMenu(self.menu)
        self.activated.connect(self.on_icon_click)

    def on_toggle_click(self, checked):
        target_temp = 0.3 if checked else 1.0
        status = "ON" if checked else "OFF"
        self.act_info.setText(f"Cozy Monitor: {status}")

        if checked:
            self.engine.is_active = True

        def transition_wrapper():
            smooth_transition(self.engine, target_temp, 2.0)
            if not checked:
                self.engine.restore()

        t = threading.Thread(
            target=transition_wrapper,
            daemon=True,
        )
        t.start()

    def on_icon_click(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.parent_window and self.parent_window.isVisible():
                self.parent_window.hide()
            elif self.parent_window:
                self.parent_window.show()
                self.parent_window.activateWindow()

    def update_state(self, is_active):
        self.act_activate.setChecked(is_active)
        status = "ON" if is_active else "OFF"
        self.act_info.setText(f"Cozy Monitor: {status}")

    def secure_quit(self):
        self.engine.stop()
        QApplication.instance().quit()
