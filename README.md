# Jello Style

The look of Project Jello — dark greys, one purple accent, Segoe UI — packaged for reuse
in **PySide6 (Qt)** and **Tkinter** apps. Both toolkits read one palette, so apps built
with either look like the same family.

```bash
# Tk apps (stdlib only)
pip install "jello-style @ git+https://github.com/rhombusgansschool/_Jello-Style.git@v0.1.0"
# Qt apps (pulls PySide6)
pip install "jello-style[qt] @ git+https://github.com/rhombusgansschool/_Jello-Style.git@v0.1.0"
# local checkout next to your project
pip install -e ..\_Jello-Style
```

```python
from jello_style import qt_theme;  qt_theme.apply(app)       # Qt
from jello_style import tk_theme;  tk_theme.apply_dark(root)  # Tk
from jello_style import palette;   palette.ACCENT             # raw colours
```

## Examples

One window per toolkit showing every styled element — buttons, inputs, chips, cards,
status colours, tabs, list and a palette swatch tab. They run straight from the repo,
no install needed:

```bash
python examples/qt_example.py
python examples/tk_example.py
python examples/qt_showcase.py   # the works: wall, menus, dialogs, tooltips, tables…
```

**Agents and contributors: read [STYLE.md](STYLE.md)** — usage rules, object names,
install fallback, gotchas. In a consuming repo, add this to its `CLAUDE.md` / `AGENTS.md`:

> UI must use the `jello-style` package. Read its `STYLE.md` (in the installed package's
> repo, or `..\_Jello-Style\STYLE.md`) before building UI. If installing it fails, tell
> the user and ask to install from `..\_Jello-Style` instead.

| Layout | |
|---|---|
| `src/jello_style/palette.py` | every colour, font, size — stdlib |
| `src/jello_style/qt_theme.py` | `apply()`, `app_stylesheet()`, `FlowLayout`, `TriStateChip` |
| `src/jello_style/tk_theme.py` | `apply_dark()`, `StyledButton`, `panel`, `card`, `StatusStrip`, fonts |
| `examples/` | one runnable window per toolkit |
