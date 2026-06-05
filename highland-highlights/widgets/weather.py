from functools import partial
import json

from PySide6.QtCore import QUrl
from PySide6.QtGui import QPixmap
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget

from config import (
    WEATHER_API_URL,
    WEATHER_ICON_HEIGHT,
    WEATHER_ICON_WIDTH,
    WEATHER_LAYOUT_CONTENT_SPACING,
    WEATHER_UPDATE_INTERVAL,
)
from utils.box_layout import create_box_layout
from utils.scaling import scale_dimension, scale_pixmap
from utils.timer import start_timer


class Weather(QWidget):
    def __init__(self):
        super().__init__()
        self._manager = QNetworkAccessManager()
        self._weather_icon_label = QLabel()
        self._temperature_label = QLabel()

        self._create_layout()

        self._get_weather_data()
        start_timer(self, WEATHER_UPDATE_INTERVAL, self._get_weather_data)

    def _create_layout(self):
        layout = create_box_layout(
            QHBoxLayout, spacing=WEATHER_LAYOUT_CONTENT_SPACING
        )
        layout.addWidget(self._weather_icon_label)
        layout.addWidget(self._temperature_label)
        self.setLayout(layout)

    def _get_weather_data(self):
        self._make_request(WEATHER_API_URL, self._process_weather_data)

    def _process_weather_data(self, reply):
        raw_data = reply.readAll().data()
        weather_data = json.loads(raw_data.decode("utf-8"))
        reply.deleteLater()
        current_weather = weather_data["current"]
        self._get_weather_icon(current_weather)

    def _get_weather_icon(self, current_weather):
        icon_path = current_weather["condition"]["icon"]
        weather_icon_url = f"https:{icon_path}"
        self._make_request(
            weather_icon_url,
            partial(self._process_weather_icon, current_weather),
        )

    def _process_weather_icon(self, current_weather, reply):
        weather_icon = reply.readAll()
        reply.deleteLater()

        pixmap = self._convert_weather_icon_to_pixmap(weather_icon)
        pixmap_width = scale_dimension(WEATHER_ICON_WIDTH)
        pixmap_height = scale_dimension(WEATHER_ICON_HEIGHT)
        scaled_weather_icon = scale_pixmap(pixmap, pixmap_width, pixmap_height)

        self._update_weather(current_weather, scaled_weather_icon)

    def _update_weather(self, current_weather, scaled_weather_icon):
        current_temperature = current_weather["temp_f"]
        self._temperature_label.setText(f"{current_temperature:.0f}°")
        self._weather_icon_label.setPixmap(scaled_weather_icon)

    def _make_request(self, url, callback):
        request = QNetworkRequest(QUrl(url))
        reply = self._manager.get(request)
        reply.finished.connect(partial(callback, reply))

    @staticmethod
    def _convert_weather_icon_to_pixmap(weather_icon):
        pixmap = QPixmap()
        pixmap.loadFromData(weather_icon)
        return pixmap
