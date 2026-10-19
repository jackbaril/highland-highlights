# SPDX-FileCopyrightText: 2025 Jack Baril
# SPDX-License-Identifier: AGPL-3.0-or-later

from PySide6.QtCore import QDate, QTime, Signal
from PySide6.QtWidgets import QLabel

from config import CLOCK_UPDATE_INTERVAL_MS
from utils.timer import start_timer


class Clock(QLabel):
    date_changed = Signal()

    def __init__(self):
        super().__init__()
        self._current_day = QDate.currentDate().day()

        self._update_time()
        start_timer(self, CLOCK_UPDATE_INTERVAL_MS, self._update_time)

    def _update_time(self):
        current_day = QDate.currentDate().day()
        if current_day != self._current_day:
            self.date_changed.emit()
            self._current_day = current_day

        current_time = QTime.currentTime()
        hour = current_time.hour() % 12 or 12
        formatted_time = (
            f"{hour:02}:{current_time.minute():02}:{current_time.second():02}"
        )
        self.setText(formatted_time)
