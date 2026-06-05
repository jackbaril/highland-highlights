from PySide6.QtCore import QDate
from PySide6.QtWidgets import QLabel


class Date(QLabel):
    def __init__(self):
        super().__init__()
        self.update_date()

    def update_date(self):
        current_date = QDate.currentDate().toString("dddd, MMMM d")
        self.setText(current_date)
