# SPDX-FileCopyrightText: 2025 Jack Baril
# SPDX-License-Identifier: AGPL-3.0-or-later

from PySide6.QtCore import Qt

from config import REFERENCE_SCREEN_HEIGHT_PX, REFERENCE_SCREEN_WIDTH_PX


def get_fill_scale_factor(size, target_size):
    return max(
        target_size.width() / size.width(),
        target_size.height() / size.height(),
    )


def get_screen_scale_factor(screen_size):
    return min(
        screen_size.width() / REFERENCE_SCREEN_WIDTH_PX,
        screen_size.height() / REFERENCE_SCREEN_HEIGHT_PX,
    )


def scale_dimension_px(base_dimension_px, scale_factor):
    return int(base_dimension_px * scale_factor)


def scale_font_size_px(base_font_size_px, scale_factor):
    scaled_font_size = max(int(base_font_size_px * scale_factor), 1)
    return f"{scaled_font_size}px"


def scale_pixmap(
    pixmap,
    width,
    height,
    aspect_ratio=Qt.AspectRatioMode.KeepAspectRatio,
    transform=Qt.TransformationMode.SmoothTransformation,
):
    return pixmap.scaled(width, height, aspect_ratio, transform)
