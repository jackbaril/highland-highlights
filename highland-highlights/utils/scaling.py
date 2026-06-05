from functools import cache

from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication

from config import REFERENCE_SCREEN_HEIGHT, REFERENCE_SCREEN_WIDTH


@cache
def get_screen_geometry():
    return QGuiApplication.primaryScreen().availableGeometry()


@cache
def get_screen_height():
    return get_screen_geometry().height()


@cache
def get_screen_width():
    return get_screen_geometry().width()


@cache
def get_screen_scale_factor():
    return min(
        get_screen_width() / REFERENCE_SCREEN_WIDTH,
        get_screen_height() / REFERENCE_SCREEN_HEIGHT,
    )


def scale_dimension(base_dimension):
    return int(base_dimension * get_screen_scale_factor())


def scale_font_size(base_font_size):
    scaled_font_size = int(base_font_size * get_screen_scale_factor())
    return f"font-size: {scaled_font_size}px"


def scale_pixmap(
    pixmap,
    width,
    height,
    aspect_ratio=Qt.AspectRatioMode.KeepAspectRatio,
    transform=Qt.TransformationMode.SmoothTransformation,
):
    return pixmap.scaled(width, height, aspect_ratio, transform)
