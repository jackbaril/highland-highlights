from PySide6.QtCore import Signal, QDate, QTime
from PySide6.QtWidgets import QLabel

from config import CLOCK_UPDATE_INTERVAL
from utils.timer import start_timer


class Clock(QLabel):
    date_changed = Signal()

    def __init__(self):
        super().__init__()
        self._today = QDate.currentDate().day()
        self._update_time()
        start_timer(self, CLOCK_UPDATE_INTERVAL, self._update_time)

    def _update_time(self):
        today = QDate.currentDate().day()
        if today != self._today:
            self.date_changed.emit()
            self._today = today

        current_time = QTime.currentTime()
        hour = current_time.hour() % 12 or 12
        formatted_time = (
            f"{hour:02}:{current_time.minute():02}:{current_time.second():02}"
        )
        self.setText(formatted_time)
