# SPDX-FileCopyrightText: 2025 Jack Baril
# SPDX-License-Identifier: AGPL-3.0-or-later

from pathlib import Path

from PySide6.QtCore import QFileSystemWatcher


class DirectoryWatcher:
    def __init__(
        self,
        watch_directory,
        file_pattern,
        on_directory_update,
        convert_file=None,
    ):
        self._watch_directory = Path(watch_directory)
        self._file_pattern = file_pattern
        self._convert_file = convert_file
        self._last_mtime = None

        self._watcher = QFileSystemWatcher()
        self._watcher.addPath(str(self._watch_directory))
        self._watcher.directoryChanged.connect(on_directory_update)

    def get_latest_file(self):
        files = list(self._watch_directory.glob(self._file_pattern))
        if not files:
            return None

        latest_file, latest_mtime = max(
            ((file, file.stat().st_mtime) for file in files),
            key=lambda pair: pair[1],
        )
        if latest_mtime == self._last_mtime:
            return None

        self._last_mtime = latest_mtime
        if self._convert_file:
            return self._convert_file(latest_file)
        return latest_file
