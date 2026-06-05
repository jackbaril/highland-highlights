from PySide6.QtWidgets import QFrame

from config import (
    CLOCK_COLOR,
    CLOCK_FONT_SIZE,
    CLOCK_HEIGHT,
    DATE_FONT_SIZE,
    FONT_FAMILY,
    FONT_WEIGHT,
    SCROLLING_TEXT_FONT_SIZE,
    SEPARATOR_COLOR,
    SEPARATOR_HEIGHT,
    TEXT_BODY_COLOR,
    TEMPERATURE_FONT_SIZE,
)
from utils.scaling import scale_dimension, scale_font_size
from widgets.clock import Clock
from widgets.date import Date
from widgets.scrolling_text import ScrollingText
from widgets.slideshow import Slideshow
from widgets.weather import Weather


def create_clock_widget():
    clock_widget = Clock()
    clock_widget.setFixedHeight(scale_dimension(CLOCK_HEIGHT))
    clock_widget.setStyleSheet(
        _join_styles(
            CLOCK_COLOR,
            FONT_FAMILY,
            FONT_WEIGHT,
            scale_font_size(CLOCK_FONT_SIZE),
        )
    )
    return clock_widget


def create_date_widget():
    date_widget = Date()
    date_widget.setStyleSheet(
        _join_styles(
            TEXT_BODY_COLOR,
            FONT_FAMILY,
            FONT_WEIGHT,
            scale_font_size(DATE_FONT_SIZE),
        )
    )
    return date_widget


def create_scrolling_text_widget():
    scrolling_text_widget = ScrollingText()
    scrolling_text_widget.setStyleSheet(
        _join_styles(
            FONT_FAMILY,
            FONT_WEIGHT,
            scale_font_size(SCROLLING_TEXT_FONT_SIZE),
            "border: none",
        )
    )
    return scrolling_text_widget


def create_separator_widget():
    separator_widget = QFrame()
    separator_widget.setFrameShape(QFrame.Shape.HLine)
    separator_widget.setFixedHeight(scale_dimension(SEPARATOR_HEIGHT))
    separator_widget.setStyleSheet(
        _join_styles(SEPARATOR_COLOR, "border: none")
    )
    return separator_widget


def create_slideshow_widget():
    slideshow_widget = Slideshow()
    return slideshow_widget


def create_weather_widget():
    weather_widget = Weather()
    weather_widget.setStyleSheet(
        _join_styles(
            TEXT_BODY_COLOR,
            FONT_FAMILY,
            FONT_WEIGHT,
            scale_font_size(TEMPERATURE_FONT_SIZE),
        )
    )
    return weather_widget


def _join_styles(*styles):
    return "; ".join(styles)
