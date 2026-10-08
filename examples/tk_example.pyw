"""Tk showcase - every jello_style element in one window. Run: python examples/tk_example.py"""

import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk

# Run straight from the repo without installing.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jello_style import palette as P
from jello_style import tk_theme


def build_sidebar(root: tk.Tk) -> None:
    side = tk_theme.panel(root, width=200, padx=P.GAP, pady=P.GAP)
    side.pack(side="left", fill="y")
    side.pack_propagate(False)
    # Children of a panel need bg=SURFACE; ttk ones need a style variant.
    ttk.Style().configure("Side.TCheckbutton", background=P.SURFACE)
    ttk.Style().map("Side.TCheckbutton", background=[("active", P.SURFACE)])
    tk_theme.section_title(side, "Options", bg=P.SURFACE).pack(fill="x")
    for text, value in (("Checkbox", False), ("Checked", True)):
        ttk.Checkbutton(side, text=text, variable=tk.BooleanVar(side, value),
                        style="Side.TCheckbutton").pack(anchor="w", pady=2)
    tk.Label(side, text="Labels on a panel\nneed bg=SURFACE", bg=P.SURFACE, fg=P.MUTED,
             font=tk_theme.FONT_SMALL, justify="left").pack(anchor="w", pady=(P.GAP, 0))


def build_controls(parent: tk.Misc) -> tk.Frame:
    page = tk.Frame(parent, padx=P.MARGIN, pady=P.MARGIN)
    tk.Label(page, text="Jello Style", font=tk_theme.FONT_TITLE, anchor="w").pack(fill="x")
    tk.Label(page, text="Body text", fg=P.MUTED, anchor="w").pack(fill="x")

    tk_theme.section_title(page, "Buttons").pack(fill="x", pady=(P.GAP, 4))
    row = tk.Frame(page)
    row.pack(fill="x")
    tk_theme.StyledButton(row, text="Button", padx=12, pady=4).pack(side="left")
    disabled = tk_theme.StyledButton(row, text="Disabled", padx=12, pady=4)
    disabled.set_enabled(False)
    disabled.pack(side="left", padx=(P.GAP, 0))
    tk_theme.StyledButton(row, text="Primary", primary=True, padx=12, pady=4).pack(
        side="left", padx=(P.GAP, 0))
    ttk.Button(row, text="ttk Button").pack(side="left", padx=(P.GAP, 0))
    ttk.Button(row, text="ttk Primary", style="Primary.TButton").pack(side="left", padx=(P.GAP, 0))

    tk_theme.section_title(page, "Inputs").pack(fill="x", pady=(P.GAP, 4))
    entry = tk.Entry(page)
    entry.insert(0, "tk.Entry")
    entry.pack(fill="x")
    combo = ttk.Combobox(page, values=["ttk.Combobox", "Second", "Third"], state="readonly")
    combo.current(0)
    combo.pack(fill="x", pady=4)
    ttk.Progressbar(page, value=60).pack(fill="x")

    tk_theme.section_title(page, "Status strip").pack(fill="x", pady=(P.GAP, 4))
    for method in ("info", "success", "warn", "error"):
        label = tk.Label(page, anchor="w", font=tk_theme.FONT_SMALL)
        label.pack(fill="x")
        getattr(tk_theme.StatusStrip(label), method)(f"StatusStrip.{method}()")

    tk_theme.section_title(page, "Card").pack(fill="x", pady=(P.GAP, 4))
    card = tk_theme.card(page, padx=P.GAP, pady=P.GAP)
    card.pack(fill="x")
    tk_theme.section_title(card, "Card title", bg=P.CARD).pack(fill="x")
    tk.Label(card, text="tk_theme.card() - CARD background, 1 px border.", bg=P.CARD,
             fg=P.MUTED, anchor="w").pack(fill="x")
    return page


def build_list(parent: tk.Misc) -> tk.Frame:
    page = tk.Frame(parent, padx=P.GAP, pady=P.GAP)
    listbox = tk.Listbox(page, activestyle="none")
    scroll = ttk.Scrollbar(page, orient="vertical", command=listbox.yview)
    listbox.configure(yscrollcommand=scroll.set)
    for i in range(1, 40):
        listbox.insert("end", f"List item {i}")
    listbox.pack(side="left", fill="both", expand=True)
    scroll.pack(side="left", fill="y")
    return page


def build_palette(parent: tk.Misc) -> tk.Frame:
    page = tk.Frame(parent, padx=P.MARGIN, pady=P.MARGIN)
    names = [n for n in dir(P) if n.isupper() and isinstance(getattr(P, n), str)
             and getattr(P, n).startswith("#")]
    for i, name in enumerate(names):
        row, col = i // 2, (i % 2) * 2
        tk.Frame(page, bg=getattr(P, name), width=48, height=22, highlightthickness=1,
                 highlightbackground=P.BORDER).grid(row=row, column=col, pady=2)
        tk.Label(page, text=f"{name}  {getattr(P, name)}", font=tk_theme.FONT_SMALL,
                 fg=P.MUTED, anchor="w", width=26).grid(row=row, column=col + 1, padx=(6, 0))
    return page


def main() -> None:
    root = tk.Tk()
    root.title("Jello Style - Tk example")
    root.geometry("900x620")
    tk_theme.apply_dark(root)                 # BEFORE any widget

    strip = tk.Label(root, anchor="w", bg=P.SURFACE, font=tk_theme.FONT_SMALL, padx=P.GAP)
    strip.pack(side="bottom", fill="x")
    tk_theme.StatusStrip(strip).success("Ready")

    build_sidebar(root)
    notebook = ttk.Notebook(root)
    notebook.pack(side="left", fill="both", expand=True)
    notebook.add(build_controls(notebook), text="Controls")
    notebook.add(build_list(notebook), text="List")
    notebook.add(build_palette(notebook), text="Palette")

    tk_theme.dark_title_bar(root)
    root.mainloop()


if __name__ == "__main__":
    main()
