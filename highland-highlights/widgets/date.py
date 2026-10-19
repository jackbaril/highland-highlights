# SPDX-FileCopyrightText: 2025 Jack Baril
# SPDX-License-Identifier: AGPL-3.0-or-later

from PySide6.QtCore import QDate
from PySide6.QtWidgets import QLabel


class Date(QLabel):
    def __init__(self):
        super().__init__()
        self.update_date()

    def update_date(self):
        current_date = QDate.currentDate().toString("dddd, MMMM d")
        self.setText(current_date)
