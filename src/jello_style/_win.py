"""_win - Windows-only touches shared by both toolkits. No-ops elsewhere."""

from __future__ import annotations

import sys

_DWMWA_USE_IMMERSIVE_DARK_MODE = 20   # Windows 10 20H1+ / Windows 11


def dark_title_bar(hwnd: int) -> bool:
    """Ask DWM for a dark caption bar on a top-level window. Returns True on success."""
    if sys.platform != "win32" or not hwnd:
        return False
    try:
        import ctypes
        value = ctypes.c_int(1)
        result = ctypes.windll.dwmapi.DwmSetWindowAttribute(
            ctypes.c_void_p(hwnd), _DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(value), ctypes.sizeof(value))
        return result == 0
    except (OSError, AttributeError):
        return False
