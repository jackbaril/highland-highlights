from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QWidget

from config import APP_ICON_PATH, APP_NAME, BACKGROUND_COLOR
from ui.layout import Layout


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self._create_central_widget()
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon(APP_ICON_PATH))
        self.setCursor(Qt.CursorShape.BlankCursor)

    def _create_central_widget(self):
        central_widget = QWidget(self)
        central_widget.setLayout(Layout())
        self.setCentralWidget(central_widget)
        self.setStyleSheet(BACKGROUND_COLOR)

    def keyPressEvent(self, event):
        full_screen = Qt.WindowState.WindowFullScreen
        if event.key() == Qt.Key.Key_F11:
            self.setWindowState(self.windowState() ^ full_screen)
        if event.key() == Qt.Key.Key_Escape and self.isFullScreen():
            self.setWindowState(self.windowState() & ~full_screen)
