import pymupdf

from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel

from config import DOCUMENT_DIRECTORY, SLIDE_CYCLE_INTERVAL, SLIDESHOW_DPI
from utils.directory_watcher import DirectoryWatcher
from utils.scaling import get_screen_height, get_screen_width, scale_pixmap
from utils.timer import start_timer


class Slideshow(QLabel):
    def __init__(self):
        super().__init__()
        self._pdf_file_watcher = DirectoryWatcher(
            DOCUMENT_DIRECTORY, "*.pdf", self._reload_pages
        )
        self._current_pdf = None
        self._current_slide = 0
        self._total_slides = 0
        self._pixmap_cache = []

        self._reload_pages()
        start_timer(self, SLIDE_CYCLE_INTERVAL, self._cycle_slides)

    def _reload_pages(self):
        latest_pdf = self._pdf_file_watcher.get_latest_file()
        if latest_pdf is not None:
            self._current_slide = 0
            self._current_pdf = latest_pdf
            self._load_pages(latest_pdf)
        self._update_slide()

    def _load_pages(self, pdf_path):
        with pymupdf.open(pdf_path) as pdf:
            self._pixmap_cache = []
            self._total_slides = len(pdf)
            screen_width = get_screen_width()
            screen_height = get_screen_height()

            for slide in range(self._total_slides):
                page = pdf.load_page(slide)
                pixmap = Slideshow._convert_page_to_pixmap(page)
                scaled_slide = scale_pixmap(
                    pixmap, screen_width, screen_height
                )
                self._pixmap_cache.append(scaled_slide)

    def _update_slide(self):
        if self._pixmap_cache:
            current_pixmap = self._pixmap_cache[self._current_slide]
            self.setPixmap(current_pixmap)

    def _cycle_slides(self):
        if self._total_slides > 1:
            self._current_slide = (
                self._current_slide + 1
            ) % self._total_slides
            self._update_slide()

    @staticmethod
    def _convert_page_to_pixmap(page):
        pixmap = page.get_pixmap(dpi=SLIDESHOW_DPI, alpha=False)
        image = QImage(
            pixmap.samples,
            pixmap.width,
            pixmap.height,
            pixmap.stride,
            QImage.Format.Format_RGB888,
        )
        pixmap = QPixmap.fromImage(image)
        return pixmap
