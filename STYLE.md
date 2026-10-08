# Jello Style — agent guide

Read this before building or changing any UI in a repo that uses `jello-style`.
It is the single source of truth for the look: dark greys, one purple accent, Segoe UI.
**Use the package; never re-derive or hard-code its colours.**

| Toolkit | When | Module |
|---|---|---|
| **PySide6 (Qt)** | bigger, long-lived apps | `jello_style.qt_theme` |
| **Tkinter** | small one-off tools, stdlib only | `jello_style.tk_theme` |
| either | colours, fonts, spacing | `jello_style.palette` (stdlib) |

---

## 1. Installing

Pin a tag so a later style change never surprises an app:

```bash
pip install "jello-style @ git+https://github.com/rhombusgansschool/_Jello-Style.git@v0.1.0"
pip install "jello-style[qt] @ git+https://github.com/rhombusgansschool/_Jello-Style.git@v0.1.0"
```

The second form also pulls PySide6. In `requirements.txt` / `pyproject.toml` use the same
`jello-style @ git+https://…@v0.1.0` string.

### ⚠ If the install fails — STOP and tell the user

If installing from GitHub fails for **any** reason (no network, repo private or renamed,
tag missing, git not found, auth prompt), do **not** work around it silently:

1. **Tell the user** it failed and show the error output.
2. **Ask** whether to install from the local checkout instead, which normally sits next
   to the project at `..\_Jello-Style`:

   ```bash
   pip install -e ..\_Jello-Style
   ```

   (`-e` = editable: edits in `_Jello-Style` take effect without reinstalling.)
3. Only proceed once the user says yes. If `..\_Jello-Style` does not exist either, ask
   the user where it is.

**Never** fall back to copying the colours/stylesheet into the project, vendoring the
files, or inventing a "close enough" palette. A silent copy is exactly the drift this
package exists to prevent.

Check it works: `python -c "import jello_style; print(jello_style.__version__)"`

---

## 2. Qt (PySide6)

```python
app = QApplication(sys.argv)
from jello_style import qt_theme
qt_theme.apply(app)            # once, before building windows
...
window.show()
qt_theme.dark_title_bar(window)  # optional, Windows: dark caption bar
```

Style through **object names**, read by the global stylesheet:

| `setObjectName(...)` | On | Look |
|---|---|---|
| `"Primary"` | `QPushButton` | accent purple — the main action |
| `"SectionTitle"` | `QLabel` | small bold spaced caps heading, white |
| `"Title"` | `QLabel` | large bold title |
| `"Sidebar"` / `"DetailPane"` / `"Panel"` | `QWidget` | SURFACE background |
| `"Card"` | `QFrame` | CARD background, 1 px border, rounded |
| `"Ok"` / `"Warn"` / `"Error"` | `QLabel` | status colours |

Extra widgets: `FlowLayout` (wrapping row — Qt has none) and `TriStateChip` (filter chip:
neutral → include → exclude; pass `include_color=palette.SECONDARY` for a second category).

Rules:
- **Do not** call `setStyleSheet` on individual widgets for anything the global sheet
  covers. Add an object name; if a new look is genuinely needed, add it to
  `qt_theme.app_stylesheet()` in this repo.
- After changing a widget's object name at runtime, call
  `w.style().unpolish(w); w.style().polish(w)` or the stylesheet won't re-apply.

## 3. Tkinter

```python
root = tk.Tk()
from jello_style import tk_theme
tk_theme.apply_dark(root)      # BEFORE creating any widget
```

`apply_dark` sets option-database defaults (so plain `tk.Label`, `tk.Frame`, `tk.Entry`
come out dark) and switches ttk to the `clam` theme. Widgets created **before** the call
keep light defaults.

| Helper | Use |
|---|---|
| `StyledButton(master, primary=False, …)` | flat button with hover/pressed/disabled; `.set_enabled(bool)` |
| `ttk.Button(style="Primary.TButton")` | the ttk equivalent |
| `panel(master)` / `card(master)` | SURFACE frame / bordered CARD frame |
| `section_title(master, "text", bg=…)` | caps heading — pass `bg` matching the parent |
| `StatusStrip(label).info/success/warn/error(msg)` | status line colouring |
| `FONT_TITLE`, `FONT_HEADING`, `FONT_BODY`, `FONT_SMALL`, `FONT_BUTTON`, `FONT_MONO` | font tuples |
| `dark_title_bar(root)` | dark Windows caption bar |

Rules:
- A child of a `panel()` must be given `bg=palette.SURFACE` explicitly — the option
  database only knows the global BG.
- Never import PySide6 (or `jello_style.qt_theme`) from a Tk app.

## 4. Design rules (both toolkits)

- **Colours come from `palette`.** No hex literals in app code. An app-specific colour
  (a badge, a rating frame) is defined once as a named constant in the *app*, next to a
  comment saying what it marks.
- **One accent.** `ACCENT` purple is for the single primary action per window, selection,
  checked states and stat highlights. Everything else is grey (`BUTTON`).
- **Text hierarchy:** `TEXT` (white) for headings and values, `MUTED` (grey) for labels and
  secondary text. Text on an accent fill uses `TEXT_ON_ACCENT`; on a light fill
  `TEXT_ON_LIGHT`.
- **Semantic colours are for meaning only:** `OK` / `WARN` / `ERROR` for status messages,
  `EXCLUDE` for negated filters, `HIGHLIGHT` for a temporary mode frame.
- **Surfaces step:** `BG` window → `SURFACE` panels/toolbars/status bars → `CARD` items →
  `INPUT_BG` fields. Borders are `BORDER`, 1 px.
- **Spacing:** `MARGIN` (20) around windows, `GAP` (12) between groups. Radius 4, chips 10.
- **Dead controls look dead:** disable with the provided disabled state, don't hide.
- **Headings are short caps** (`SectionTitle` / `section_title`) — "FILTERS", not "Filters:".

## 5. Running without a console

- **Start GUI apps with `pythonw`** (or a `.pyw` file) so no console window opens;
  keep `python` for debugging.
- **Under pythonw there is no stdout/stderr**: log to `app.log`, show uncaught errors in a
  message box (Qt: `sys.excepthook`; Tk: `root.report_callback_exception` — Tk otherwise
  prints callback errors to the missing stderr and they vanish).
- **Console programs (ffmpeg, cmd, git…) need `creationflags=subprocess.CREATE_NO_WINDOW`**
  or each one flashes its own console window.
- **Tk: never touch widgets from a worker thread** — hand results back via a `queue` polled
  with `after()`.

## 6. Gotchas (learned the hard way in Project Jello)

- **Tk `winfo_reqwidth()` is the *requested* size, not the placed size** (~14 px for an
  empty label). Never size images from it; pass sizes explicitly.
- **`overrideredirect(True)` removes a Tk window from the taskbar and Alt-Tab.** If you go
  borderless, clear `WS_EX_TOOLWINDOW` / set `WS_EX_APPWINDOW` via ctypes, and give the
  user an escape hatch (✕ button, `Esc`).
- **An animating GIF in Tk holds its file open**; Windows refuses to delete an open file.
  Stop the animation before unlinking.
- **Tk's clipboard is text-only.** For images use Pillow's `ImageGrab.grabclipboard()`.
- **Qt has no wrapping layout** — use `FlowLayout`, don't nest HBoxes.

## 7. Changing the style itself

Changes go in **this** repo (`_Jello-Style`), never in a consuming app:

1. Edit `palette.py` / `qt_theme.py` / `tk_theme.py`.
2. Run `python examples/qt_example.py` and `python examples/tk_example.py` and let the
   user look — do not take screenshots unless the user asks.
3. Bump `version` in `pyproject.toml` **and** `__version__` in `__init__.py`.
4. The user commits and tags (`v0.2.0`); apps opt in by moving their pin.

Keep `palette.py` stdlib-only and keep `__init__.py` from importing `qt_theme`.
