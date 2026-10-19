# SPDX-FileCopyrightText: 2025 Jack Baril
# SPDX-License-Identifier: AGPL-3.0-or-later

from PySide6.QtCore import QTimer


def start_timer(parent, interval_ms, callback):
    timer = QTimer(parent)
    timer.setInterval(interval_ms)
    timer.timeout.connect(callback)
    timer.start()
