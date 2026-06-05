from pathlib import Path

from PySide6.QtCore import QFileSystemWatcher


class DirectoryWatcher:
    def __init__(
        self,
        watch_directory,
        file_extension_filter,
        on_directory_update,
        on_new_file_detected=None,
    ):
        self._watch_directory = Path(watch_directory)
        self._file_extension_filter = file_extension_filter
        self._on_new_file_detected = on_new_file_detected
        self._last_mtime = None

        self._watcher = QFileSystemWatcher()
        self._watcher.addPath(str(self._watch_directory))
        self._watcher.directoryChanged.connect(on_directory_update)

    def get_latest_file(self):
        files = list(self._watch_directory.glob(self._file_extension_filter))
        if not files:
            return None

        latest_file, latest_mtime = max(
            ((file, file.stat().st_mtime) for file in files),
            key=lambda pair: pair[1],
        )
        if latest_mtime == self._last_mtime:
            return None

        self._last_mtime = latest_mtime
        if self._on_new_file_detected:
            return self._on_new_file_detected(latest_file)
        return latest_file
