# SPDX-FileCopyrightText: 2025 Jack Baril
# SPDX-License-Identifier: AGPL-3.0-or-later

def create_box_layout(layout_class, spacing=0, alignment=None):
    layout = layout_class()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(spacing)
    if alignment is not None:
        layout.setAlignment(alignment)
    return layout
