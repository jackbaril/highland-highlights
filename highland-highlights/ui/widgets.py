# SPDX-FileCopyrightText: 2025 Jack Baril
# SPDX-License-Identifier: AGPL-3.0-or-later

from PySide6.QtWidgets import QFrame

from config import (
    CLOCK_COLOR,
    CLOCK_FONT_SIZE_PX,
    CLOCK_HEIGHT_PX,
    DATE_FONT_SIZE_PX,
    FONT_FAMILY,
    FONT_WEIGHT,
    SCROLLING_TEXT_FONT_SIZE_PX,
    SEPARATOR_COLOR,
    SEPARATOR_HEIGHT_PX,
    TEXT_BODY_COLOR,
    TEMPERATURE_FONT_SIZE_PX,
)
from utils.scale import scale_dimension_px, scale_font_size_px
from widgets.clock import Clock
from widgets.date import Date
from widgets.scrolling_text import ScrollingText
from widgets.slideshow import Slideshow
from widgets.weather import Weather


def create_clock_widget():
    return Clock()


def create_date_widget():
    return Date()


def create_scrolling_text_widget():
    return ScrollingText()


def create_separator_widget():
    separator_widget = QFrame()
    separator_widget.setFrameShape(QFrame.Shape.HLine)
    separator_widget.setStyleSheet(
        _format_styles(background_color=SEPARATOR_COLOR, border="none")
    )
    return separator_widget


def create_slideshow_widget():
    return Slideshow()


def create_weather_widget():
    return Weather()


def scale_clock_widget(clock_widget, scale_factor):
    clock_widget.setFixedHeight(
        scale_dimension_px(CLOCK_HEIGHT_PX, scale_factor)
    )
    clock_widget.setStyleSheet(
        _format_styles(
            color=CLOCK_COLOR,
            font_family=FONT_FAMILY,
            font_weight=FONT_WEIGHT,
            font_size=scale_font_size_px(CLOCK_FONT_SIZE_PX, scale_factor),
        )
    )


def scale_date_widget(date_widget, scale_factor):
    date_widget.setStyleSheet(
        _format_styles(
            color=TEXT_BODY_COLOR,
            font_family=FONT_FAMILY,
            font_weight=FONT_WEIGHT,
            font_size=scale_font_size_px(DATE_FONT_SIZE_PX, scale_factor),
        )
    )


def scale_scrolling_text_widget(scrolling_text_widget, scale_factor):
    scrolling_text_widget.setStyleSheet(
        _format_styles(
            font_family=FONT_FAMILY,
            font_weight=FONT_WEIGHT,
            font_size=scale_font_size_px(
                SCROLLING_TEXT_FONT_SIZE_PX, scale_factor
            ),
            border="none",
        )
    )


def scale_separator_widget(separator_widget, scale_factor):
    separator_widget.setFixedHeight(
        scale_dimension_px(SEPARATOR_HEIGHT_PX, scale_factor)
    )


def scale_weather_widget(weather_widget, scale_factor):
    weather_widget.setStyleSheet(
        _format_styles(
            color=TEXT_BODY_COLOR,
            font_family=FONT_FAMILY,
            font_weight=FONT_WEIGHT,
            font_size=scale_font_size_px(
                TEMPERATURE_FONT_SIZE_PX, scale_factor
            ),
        )
    )


def _format_styles(**properties):
    return "; ".join(
        f"{name.replace('_', '-')}: {value}"
        for name, value in properties.items()
    )
