from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout

from config import DATE_WEATHER_LAYOUT_CONTENT_SPACING
from ui.widgets import (
    create_clock_widget,
    create_date_widget,
    create_scrolling_text_widget,
    create_separator_widget,
    create_slideshow_widget,
    create_weather_widget,
)
from utils.box_layout import create_box_layout


class Layout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self._clock_widget = create_clock_widget()
        self._date_widget = create_date_widget()
        self._scrolling_text_widget = create_scrolling_text_widget()
        self._separator_widget = create_separator_widget()
        self._slideshow_widget = create_slideshow_widget()
        self._weather_widget = create_weather_widget()

        self._clock_widget.date_changed.connect(self._date_widget.update_date)
        self._create_layout()

    def _create_layout(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
        self.addLayout(self._create_top_layout())
        self.addWidget(self._separator_widget)
        self.addWidget(self._slideshow_widget)

    def _create_top_layout(self):
        top_layout = create_box_layout(QHBoxLayout)
        top_layout.addLayout(self._create_clock_date_weather_layout(), 1)
        top_layout.addWidget(self._scrolling_text_widget, 1)
        return top_layout

    def _create_clock_date_weather_layout(self):
        clock_date_weather_layout = create_box_layout(
            QVBoxLayout, alignment=Qt.AlignmentFlag.AlignCenter
        )
        clock_date_weather_layout.addWidget(self._clock_widget)
        clock_date_weather_layout.addLayout(self._create_date_weather_layout())
        return clock_date_weather_layout

    def _create_date_weather_layout(self):
        date_weather_layout = create_box_layout(
            QHBoxLayout,
            spacing=DATE_WEATHER_LAYOUT_CONTENT_SPACING,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        date_weather_layout.addWidget(self._date_widget)
        date_weather_layout.addWidget(self._weather_widget)
        return date_weather_layout
