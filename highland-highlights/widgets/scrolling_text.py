from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QScrollArea, QWidget

from config import (
    DOCUMENT_DIRECTORY,
    PARAGRAPH_SPACING,
    TEXT_SCROLL_INTERVAL,
)
from utils.directory_watcher import DirectoryWatcher
from utils.docx_to_html_converter import convert_docx_to_html
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
        self._current_docx = None
        self._scroll_height = 0
        self._scroll_offset = 0

        self._labels = ScrollingText._create_labels(self._current_docx)
        self._configure_scroll_area()
        self._create_scroll_area_widget()

        self._update_text()
        start_timer(self, TEXT_SCROLL_INTERVAL, self._scroll_labels)

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
        latest_docx = self._docx_file_watcher.get_latest_file()
        if latest_docx is not None:
            self._current_docx = latest_docx
            for label in self._labels:
                label.setText(self._current_docx)
            self._scroll_offset = 0
            self._resize_labels()

    def _resize_labels(self):
        width = self.viewport().width()
        label_height = max(self._labels[0].heightForWidth(width), 0)
        for label in self._labels:
            label.resize(width, label_height)

        if label_height > 0:
            self._scroll_height = label_height + PARAGRAPH_SPACING
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
