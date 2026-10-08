"""jello_style - the Project Jello look for PySide6 and Tkinter apps.

    from jello_style import palette                 # colours only, stdlib
    from jello_style.qt_theme import apply           # needs the [qt] extra
    from jello_style.tk_theme import apply_dark      # stdlib

The Qt and Tk modules are not imported here on purpose: importing the package must never
pull PySide6 into a Tk app.
"""

from __future__ import annotations

from . import palette

__version__ = "0.1.0"
__all__ = ["palette", "__version__"]
