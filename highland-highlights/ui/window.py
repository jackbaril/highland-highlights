# SPDX-FileCopyrightText: 2025 Jack Baril
# SPDX-License-Identifier: AGPL-3.0-or-later

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QSizePolicy, QWidget

from config import APP_ICON_PATH, APP_NAME, BACKGROUND_COLOR
from ui.layout import Layout
from utils.scale import get_screen_scale_factor


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self._layout = Layout()

        self._create_central_widget()
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon(APP_ICON_PATH))
        self.setCursor(Qt.CursorShape.BlankCursor)

    def _create_central_widget(self):
        central_widget = QWidget(self)
        central_widget.setLayout(self._layout)
        central_widget.setSizePolicy(
            QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored
        )
        self.setCentralWidget(central_widget)
        self.setStyleSheet(f"background-color: {BACKGROUND_COLOR}")

    def keyPressEvent(self, event):
        full_screen = Qt.WindowState.WindowFullScreen
        if event.key() == Qt.Key.Key_F11:
            self.setWindowState(self.windowState() ^ full_screen)
        if event.key() == Qt.Key.Key_Escape and self.isFullScreen():
            self.setWindowState(self.windowState() & ~full_screen)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._layout.apply_scale(get_screen_scale_factor(event.size()))
