# SPDX-FileCopyrightText: 2025 Jack Baril
# SPDX-License-Identifier: AGPL-3.0-or-later

import sys

from PySide6.QtWidgets import QApplication

from ui.window import Window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.showFullScreen()
    sys.exit(app.exec())
