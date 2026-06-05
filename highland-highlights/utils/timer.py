from PySide6.QtCore import QTimer


def start_timer(parent, interval, callback):
    timer = QTimer(parent)
    timer.setInterval(interval)
    timer.timeout.connect(callback)
    timer.start()
