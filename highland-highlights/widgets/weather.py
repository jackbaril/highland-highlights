# SPDX-FileCopyrightText: 2025 Jack Baril
# SPDX-License-Identifier: AGPL-3.0-or-later

import json
import os
from functools import partial
from urllib.parse import urlencode

from dotenv import load_dotenv
from PySide6.QtCore import QUrl
from PySide6.QtGui import QPixmap
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget

from config import (
    WEATHER_API_LOCATION,
    WEATHER_ICON_HEIGHT_PX,
    WEATHER_ICON_WIDTH_PX,
    WEATHER_LAYOUT_CONTENT_SPACING_PX,
    WEATHER_UPDATE_INTERVAL_MS,
)
from utils.box_layout import create_box_layout
from utils.scale import scale_dimension_px, scale_pixmap
from utils.timer import start_timer

WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"


class Weather(QWidget):
    def __init__(self):
        super().__init__()
        self._manager = QNetworkAccessManager()
        self._weather_icon_label = QLabel()
        self._temperature_label = QLabel()
        self._scale_factor = 1.0
        self._weather_icon = None

        self._create_layout()

        self._request_weather_data()
        start_timer(
            self, WEATHER_UPDATE_INTERVAL_MS, self._request_weather_data
        )

    def apply_scale(self, scale_factor):
        self._scale_factor = scale_factor
        self.layout().setSpacing(
            scale_dimension_px(
                WEATHER_LAYOUT_CONTENT_SPACING_PX, scale_factor
            )
        )
        self._update_weather_icon()

    def _create_layout(self):
        layout = create_box_layout(QHBoxLayout)
        layout.addWidget(self._weather_icon_label)
        layout.addWidget(self._temperature_label)
        self.setLayout(layout)

    def _request_weather_data(self):
        self._make_request(
            self._get_weather_api_url(), self._process_weather_data
        )

    def _process_weather_data(self, reply):
        raw_data = reply.readAll().data()
        weather_data = json.loads(raw_data.decode("utf-8"))
        reply.deleteLater()
        current_weather = weather_data["current"]
        self._request_weather_icon(current_weather)

    def _request_weather_icon(self, current_weather):
        icon_path = current_weather["condition"]["icon"]
        weather_icon_url = f"https:{icon_path}"
        self._make_request(
            weather_icon_url,
            partial(self._process_weather_icon, current_weather),
        )

    def _process_weather_icon(self, current_weather, reply):
        weather_icon = reply.readAll()
        reply.deleteLater()

        self._weather_icon = self._convert_weather_icon_to_pixmap(weather_icon)

        self._update_weather(current_weather)

    def _update_weather(self, current_weather):
        current_temperature = current_weather["temp_f"]
        self._temperature_label.setText(f"{current_temperature:.0f}°")
        self._update_weather_icon()

    def _update_weather_icon(self):
        if self._weather_icon is None:
            return

        pixmap_width = scale_dimension_px(
            WEATHER_ICON_WIDTH_PX, self._scale_factor
        )
        pixmap_height = scale_dimension_px(
            WEATHER_ICON_HEIGHT_PX, self._scale_factor
        )
        scaled_weather_icon = scale_pixmap(
            self._weather_icon, pixmap_width, pixmap_height
        )
        self._weather_icon_label.setPixmap(scaled_weather_icon)

    def _get_weather_api_url(self):
        query_parameters = {
            "key": self._get_weather_api_key(),
            "q": WEATHER_API_LOCATION,
        }
        query_string = urlencode(query_parameters)
        return f"{WEATHER_API_URL}?{query_string}"

    def _make_request(self, url, callback):
        request = QNetworkRequest(QUrl(url))
        reply = self._manager.get(request)
        reply.finished.connect(partial(callback, reply))

    @staticmethod
    def _convert_weather_icon_to_pixmap(weather_icon):
        pixmap = QPixmap()
        pixmap.loadFromData(weather_icon)
        return pixmap

    @staticmethod
    def _get_weather_api_key():
        load_dotenv()
        return os.getenv("WEATHER_API_KEY")
