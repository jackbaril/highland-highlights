# SPDX-FileCopyrightText: 2025 Jack Baril
# SPDX-License-Identifier: AGPL-3.0-or-later

import pymupdf
from PySide6.QtCore import QSize, QSizeF, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel, QSizePolicy

from config import DOCUMENT_DIRECTORY, SLIDE_CYCLE_INTERVAL_MS
from utils.directory_watcher import DirectoryWatcher
from utils.scale import get_fill_scale_factor
from utils.timer import start_timer


class Slideshow(QLabel):
    def __init__(self):
        super().__init__()
        self._pdf_file_watcher = DirectoryWatcher(
            DOCUMENT_DIRECTORY, "*.pdf", self._reload_slides
        )
        self._current_pdf = None
        self._current_slide_index = 0
        self._total_slides = 0
        self._pixmap_cache = {}
        self._pixmap_cache_size = QSize()

        self._configure_label()

        self._reload_slides()
        start_timer(self, SLIDE_CYCLE_INTERVAL_MS, self._cycle_slides)

    def _configure_label(self):
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(
            QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored
        )

    def _reload_slides(self):
        latest_pdf = self._pdf_file_watcher.get_latest_file()
        if latest_pdf is not None:
            if self._current_pdf is not None:
                self._current_pdf.close()
            self._current_slide_index = 0
            self._current_pdf = pymupdf.open(latest_pdf)
            self._total_slides = len(self._current_pdf)
            self._pixmap_cache = {}
        self._update_slide()

    def _update_slide(self):
        if self._total_slides == 0 or not self.isVisible():
            return

        if self.size() != self._pixmap_cache_size:
            self._pixmap_cache = {}
            self._pixmap_cache_size = self.size()
        if self._current_slide_index not in self._pixmap_cache:
            self._load_slide(self._current_slide_index)
        self.setPixmap(self._pixmap_cache[self._current_slide_index])

    def _load_slide(self, slide_index):
        page = self._current_pdf.load_page(slide_index)
        page_size = QSizeF(page.rect.width, page.rect.height)
        device_pixel_ratio = self.devicePixelRatioF()
        zoom = device_pixel_ratio * get_fill_scale_factor(
            page_size, self.size()
        )

        pixmap = Slideshow._convert_page_to_pixmap(page, zoom)
        pixmap.setDevicePixelRatio(device_pixel_ratio)
        self._pixmap_cache[slide_index] = pixmap

    def _cycle_slides(self):
        if self._total_slides > 1:
            self._current_slide_index = (
                self._current_slide_index + 1
            ) % self._total_slides
            self._update_slide()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_slide()

    def showEvent(self, event):
        super().showEvent(event)
        self._update_slide()

    @staticmethod
    def _convert_page_to_pixmap(page, zoom):
        pdf_pixmap = page.get_pixmap(
            matrix=pymupdf.Matrix(zoom, zoom), alpha=False
        )
        image = QImage(
            pdf_pixmap.samples,
            pdf_pixmap.width,
            pdf_pixmap.height,
            pdf_pixmap.stride,
            QImage.Format.Format_RGB888,
        )
        return QPixmap.fromImage(image)
