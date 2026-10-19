# SPDX-FileCopyrightText: 2025 Jack Baril
# SPDX-License-Identifier: AGPL-3.0-or-later

from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import QLabel, QScrollArea, QWidget

from config import (
    DOCUMENT_DIRECTORY,
    PARAGRAPH_SPACING_PX,
    TEXT_SCROLL_INTERVAL_MS,
)
from utils.directory_watcher import DirectoryWatcher
from utils.docx_to_html import convert_docx_to_html, create_html_document
from utils.scale import scale_dimension_px
from utils.timer import start_timer


class ScrollingText(QScrollArea):
    def __init__(self):
        super().__init__()
        self._docx_file_watcher = DirectoryWatcher(
            DOCUMENT_DIRECTORY,
            "*.docx",
            self._update_text,
            convert_docx_to_html,
        )
        self._current_html = None
        self._paragraph_spacing_px = PARAGRAPH_SPACING_PX
        self._scroll_height = 0
        self._scroll_offset = 0

        self._labels = ScrollingText._create_labels(self._current_html)
        self._configure_scroll_area()
        self._create_scroll_area_widget()

        self._update_text()
        start_timer(self, TEXT_SCROLL_INTERVAL_MS, self._scroll_labels)

    def apply_scale(self, scale_factor):
        self._paragraph_spacing_px = scale_dimension_px(
            PARAGRAPH_SPACING_PX, scale_factor
        )
        self._update_labels()

    def _configure_scroll_area(self):
        self.setWidgetResizable(True)
        self.setEnabled(False)
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

    def _create_scroll_area_widget(self):
        scroll_area_widget = QWidget()
        for label in self._labels:
            label.setParent(scroll_area_widget)
        self.setWidget(scroll_area_widget)

    def _update_text(self):
        latest_html = self._docx_file_watcher.get_latest_file()
        if latest_html is not None:
            self._current_html = latest_html
            self._scroll_offset = 0
            self._update_labels()

    def _update_labels(self):
        if self._current_html is not None:
            html_document = create_html_document(
                self._current_html, self._paragraph_spacing_px
            )
            for label in self._labels:
                label.setText(html_document)
        self._resize_labels()

    def _resize_labels(self):
        width = self.viewport().width()
        label_height = max(self._labels[0].heightForWidth(width), 0)
        for label in self._labels:
            label.resize(width, label_height)

        if label_height > 0:
            self._scroll_height = label_height + self._paragraph_spacing_px
            self._scroll_offset %= self._scroll_height
        else:
            self._scroll_height = 0
        self._move_labels()

    def _scroll_labels(self):
        if self._scroll_height > 0:
            self._scroll_offset = (
                self._scroll_offset + 1
            ) % self._scroll_height
            self._move_labels()

    def _move_labels(self):
        for i, label in enumerate(self._labels):
            label.move(0, i * self._scroll_height - self._scroll_offset)

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() == QEvent.Type.FontChange:
            self._resize_labels()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._resize_labels()

    @staticmethod
    def _create_labels(text):
        return [ScrollingText._create_label(text) for _ in range(2)]

    @staticmethod
    def _create_label(text):
        label = QLabel()
        label.setText(text)
        label.setWordWrap(True)
        return label
