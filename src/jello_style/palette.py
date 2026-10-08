r"""palette - the one shared colour vocabulary for every Jello-styled app.

Qt and Tkinter cannot share widgets, but they must read as one family. Both import their
colours from here, so a tweak lands everywhere:

    jello_style.qt_theme   builds the Qt stylesheet from these
    jello_style.tk_theme   configures Tk / ttk widgets from these

Stdlib only - no Qt, no Pillow - so a Tk app never drags PySide6 in.

App-specific colours (badges, rating frames, ...) belong in the app, not here.
"""

from __future__ import annotations

# ── Surfaces ───────────────────────────────────────────────────────────────────────────
BG = "#1b1b1b"          # window background
SURFACE = "#262626"     # panels, sidebars, toolbars, status bars
CARD = "#232323"        # cards and empty slots, one step darker than SURFACE
INPUT_BG = "#1f1f1f"    # text inputs and lists
BORDER = "#3d3d3d"
SPLITTER = "#303030"    # splitter handles
CHIP = "#2e2e2e"        # neutral chip / tag background

# ── Controls ───────────────────────────────────────────────────────────────────────────
BUTTON = "#333333"
BUTTON_HOVER = "#3d3d3d"
BUTTON_PRESSED = "#2a2a2a"
BUTTON_DISABLED = "#242424"

# ── Accent (reserved for the primary action and stat highlights) ───────────────────────
ACCENT = "#5a2d91"
ACCENT_HOVER = "#6d3aae"
ACCENT_PRESSED = "#47236f"

# ── Text ───────────────────────────────────────────────────────────────────────────────
TEXT = "#f0f0f0"
MUTED = "#9a9a9a"
TEXT_ON_ACCENT = "#f0e8ff"
TEXT_ON_LIGHT = "#1b1b1b"  # for badges on a light fill; TEXT is unreadable there

# ── Semantic (status messages and states only) ─────────────────────────────────────────
OK = "#3fa34d"
WARN = "#d9822b"
ERROR = "#d16060"
SECONDARY = "#1f6f64"   # teal - a second category next to ACCENT (e.g. chips by origin)
EXCLUDE = "#8a2d2d"     # excluded / negated filter state
HIGHLIGHT = "#ff7a18"   # transient mode frame (e.g. multi-select active)

# ── Type ───────────────────────────────────────────────────────────────────────────────
FONT_FAMILY = "Segoe UI"
FONT_MONO = "Consolas"

# Point sizes. Tk takes these directly; Qt uses them via the stylesheet / QFont.
SIZE_TITLE = 24
SIZE_HEADING = 11       # small, bold, spaced capitals - "SECTION TITLE"
SIZE_BODY = 12
SIZE_SMALL = 10
SIZE_BUTTON = 13

# ── Geometry ───────────────────────────────────────────────────────────────────────────
RADIUS = 4              # buttons, inputs
CHIP_RADIUS = 10
MARGIN = 20
GAP = 12
