"""tk_theme - the Jello look for Tkinter apps. Stdlib only.

    import tkinter as tk
    from jello_style import tk_theme

    root = tk.Tk()
    tk_theme.apply_dark(root)                 # BEFORE creating any widget
    tk_theme.StyledButton(root, text="Go", primary=True).pack()

`apply_dark` sets option-database defaults, so plain tk.Label / tk.Frame / tk.Entry made
afterwards are already dark; widgets created before it keep the light defaults. It also
switches ttk to the "clam" theme, the only built-in ttk theme that honours colours.

Ported from Project Jello's JelloSidecar.py.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from . import palette as P
from ._win import dark_title_bar as _dark_title_bar

FONT_TITLE = (P.FONT_FAMILY, P.SIZE_TITLE, "bold")
FONT_HEADING = (P.FONT_FAMILY, P.SIZE_HEADING, "bold")   # small, spaced caps
FONT_BODY = (P.FONT_FAMILY, P.SIZE_BODY)
FONT_SMALL = (P.FONT_FAMILY, P.SIZE_SMALL)
FONT_BUTTON = (P.FONT_FAMILY, P.SIZE_BUTTON, "bold")
FONT_MONO = (P.FONT_MONO, P.SIZE_SMALL)


def apply_dark(root: tk.Tk) -> ttk.Style:
    """Dark defaults for every Tk and ttk widget created after this call."""
    root.configure(bg=P.BG)
    add = root.option_add
    add("*Font", FONT_BODY)
    add("*Background", P.BG)
    add("*Foreground", P.TEXT)
    add("*activeBackground", P.BUTTON_HOVER)
    add("*activeForeground", P.TEXT)
    add("*highlightThickness", 0)
    add("*selectBackground", P.ACCENT)
    add("*selectForeground", P.TEXT_ON_ACCENT)
    add("*insertBackground", P.TEXT)               # text cursor
    add("*disabledForeground", P.MUTED)
    for cls in ("Entry", "Text", "Listbox", "Spinbox"):
        add(f"*{cls}.Background", P.INPUT_BG)
        add(f"*{cls}.relief", "flat")
        add(f"*{cls}.borderWidth", 4)
    add("*Menu.Background", P.SURFACE)
    add("*Menu.activeBackground", P.ACCENT)
    add("*Menu.relief", "flat")
    add("*TCombobox*Listbox.Background", P.SURFACE)
    add("*TCombobox*Listbox.selectBackground", P.ACCENT)

    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure(".", background=P.BG, foreground=P.TEXT, fieldbackground=P.INPUT_BG,
                    bordercolor=P.BORDER, lightcolor=P.BORDER, darkcolor=P.BORDER,
                    troughcolor=P.BG, focuscolor=P.ACCENT, font=FONT_BODY)
    style.configure("TButton", background=P.BUTTON, padding=(12, 5), relief="flat")
    style.map("TButton", background=[("pressed", P.BUTTON_PRESSED), ("active", P.BUTTON_HOVER),
                                     ("disabled", P.BUTTON_DISABLED)],
              foreground=[("disabled", P.MUTED)])
    style.configure("Primary.TButton", background=P.ACCENT, foreground=P.TEXT_ON_ACCENT)
    style.map("Primary.TButton", background=[("pressed", P.ACCENT_PRESSED),
                                             ("active", P.ACCENT_HOVER)])
    style.configure("TCombobox", background=P.BUTTON, arrowcolor=P.TEXT)
    style.map("TCombobox", fieldbackground=[("readonly", P.BUTTON)],
              selectbackground=[("readonly", P.BUTTON)])
    style.configure("TCheckbutton", foreground=P.MUTED, indicatorbackground=P.INPUT_BG)
    style.map("TCheckbutton", indicatorbackground=[("selected", P.ACCENT)],
              background=[("active", P.BG)])
    style.configure("TProgressbar", background=P.ACCENT, troughcolor=P.INPUT_BG)
    for orient in ("Vertical", "Horizontal"):
        style.configure(f"{orient}.TScrollbar", background=P.BORDER, troughcolor=P.BG,
                        arrowcolor=P.MUTED, relief="flat")
        style.map(f"{orient}.TScrollbar", background=[("active", P.BUTTON_HOVER)])
    style.configure("Treeview", background=P.INPUT_BG, fieldbackground=P.INPUT_BG)
    style.map("Treeview", background=[("selected", P.ACCENT)])
    style.configure("Treeview.Heading", background=P.SURFACE, relief="flat")
    style.configure("TNotebook", background=P.BG)
    style.configure("TNotebook.Tab", background=P.SURFACE, foreground=P.MUTED, padding=(16, 6))
    style.map("TNotebook.Tab", background=[("selected", P.BUTTON)],
              foreground=[("selected", P.TEXT)])
    return style


def dark_title_bar(window: tk.Tk | tk.Toplevel) -> bool:
    """Dark Windows caption bar. Call after the window exists (e.g. after update_idletasks)."""
    window.update_idletasks()
    import ctypes
    try:
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
    except AttributeError:          # not Windows
        return False
    return _dark_title_bar(hwnd)


class StyledButton(tk.Button):
    """Flat button with hover, pressed, and disabled states. `primary` = accent colour."""

    def __init__(self, master: tk.Misc, primary: bool = False, **kwargs: object) -> None:
        self._base = P.ACCENT if primary else P.BUTTON
        self._hover = P.ACCENT_HOVER if primary else P.BUTTON_HOVER
        self._pressed = P.ACCENT_PRESSED if primary else P.BUTTON_PRESSED
        self._enabled = True
        kwargs.setdefault("font", FONT_BUTTON)
        super().__init__(
            master,
            bg=self._base,
            fg=P.TEXT_ON_ACCENT if primary else P.TEXT,
            activebackground=self._pressed,
            activeforeground=P.TEXT,
            disabledforeground=P.MUTED,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            cursor="hand2",
            **kwargs,
        )
        self.bind("<Enter>", self._on_enter, add="+")
        self.bind("<Leave>", self._on_leave, add="+")

    def _on_enter(self, _event: object) -> None:
        if self._enabled:
            self.configure(bg=self._hover)

    def _on_leave(self, _event: object) -> None:
        if self._enabled:
            self.configure(bg=self._base)

    @property
    def enabled(self) -> bool:
        return self._enabled

    def set_enabled(self, enabled: bool) -> None:
        """Toggle the disabled look so dead controls read as dead."""
        self._enabled = enabled
        if enabled:
            self.configure(state=tk.NORMAL, bg=self._base, cursor="hand2")
        else:
            self.configure(state=tk.DISABLED, bg=P.BUTTON_DISABLED, cursor="")


def panel(master: tk.Misc, **kwargs: object) -> tk.Frame:
    """SURFACE-coloured frame - sidebars, headers, status strips."""
    kwargs.setdefault("bg", P.SURFACE)
    return tk.Frame(master, **kwargs)


def card(master: tk.Misc, **kwargs: object) -> tk.Frame:
    """CARD-coloured frame with a 1 px BORDER outline."""
    kwargs.setdefault("bg", P.CARD)
    kwargs.setdefault("highlightbackground", P.BORDER)
    kwargs.setdefault("highlightthickness", 1)
    return tk.Frame(master, **kwargs)


def section_title(master: tk.Misc, text: str, **kwargs: object) -> tk.Label:
    """Small bold caps heading, like Qt's #SectionTitle. Pass bg= to match the parent."""
    kwargs.setdefault("font", FONT_HEADING)
    kwargs.setdefault("fg", P.TEXT)
    kwargs.setdefault("anchor", "w")
    return tk.Label(master, text=text.upper(), **kwargs)


class StatusStrip:
    """One label that reports outcomes: info (muted), success, warn, error."""

    def __init__(self, label: tk.Label) -> None:
        self.label = label

    def _set(self, message: str, colour: str) -> None:
        try:
            self.label.configure(text=message, fg=colour)
        except tk.TclError:          # window already destroyed
            pass

    def info(self, message: str) -> None:
        self._set(message, P.MUTED)

    def success(self, message: str) -> None:
        self._set(message, P.OK)

    def warn(self, message: str) -> None:
        self._set(message, P.WARN)

    def error(self, message: str) -> None:
        self._set(message, P.ERROR)
