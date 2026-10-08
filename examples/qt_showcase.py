"""Qt showcase - all the bells and whistles of jello_style in one interactive window.

Run: python examples/qt_showcase.py   (no install needed)

    Sidebar     search + tri-state chips that really filter the wall
    Wall        cards in a FlowLayout; click = select (detail pane), Ctrl+click =
                multi-select (HIGHLIGHT frame), right-click = context menu
    Controls    every button / input / check / progress variant, status colours
    Data        QTreeWidget + sortable QTableWidget with styled headers
    Palette     every palette colour; click a swatch to copy its hex
    Chrome      menu bar, toolbar with checkable actions, status bar with progress,
                tooltips everywhere, dark Windows title bar, F5 / Ctrl+Q shortcuts
"""

import random
import sys
from pathlib import Path

# Run straight from the repo without installing.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame, QGridLayout,
                               QHBoxLayout, QInputDialog, QLabel, QLineEdit, QMainWindow, QMenu, QMessageBox, QPlainTextEdit, QProgressBar,
                               QPushButton, QRadioButton, QScrollArea, QSpinBox, QSplitter,
                               QTableWidget, QTableWidgetItem, QTabWidget, QToolButton,
                               QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

import jello_style
from jello_style import palette as P
from jello_style import qt_theme

random.seed(7)
# App-specific colour: defined once, named, never inline (STYLE.md section 4).
TOP_BADGE = "#87ceeb"   # light badge -> needs TEXT_ON_LIGHT
TAGS = ["red", "blue", "green", "new", "favourite", "archived"]
ITEMS = [
    {"name": f"Item {i:02d}", "tags": random.sample(TAGS, random.randint(1, 3)),
     "score": random.randint(1, 5), "size": random.randint(80, 4000)}
    for i in range(1, 25)
]


def title(text: str, name: str = "SectionTitle") -> QLabel:
    label = QLabel(text.upper() if name == "SectionTitle" else text)
    label.setObjectName(name)
    return label


def badge(text: str, fill: str, fg: str) -> QLabel:
    """Small pill label - per-widget style is fine for one-off app-specific colours."""
    label = QLabel(text)
    label.setStyleSheet(f"background: {fill}; color: {fg}; border-radius: 6px;"
                        "padding: 1px 6px; font-size: 7pt; font-weight: bold;")
    return label


def restyle(widget: QWidget) -> None:
    """Re-apply the stylesheet after an objectName / property change."""
    widget.style().unpolish(widget)
    widget.style().polish(widget)


# ── Wall card ──────────────────────────────────────────────────────────────────────────

class WallCard(QFrame):
    def __init__(self, item: dict, window: "Showcase") -> None:
        super().__init__()
        self.item, self.showcase = item, window
        self.selected = False
        self.setObjectName("Card")
        self.setFixedSize(170, 150)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(f"{item['name']}\nTags: {', '.join(item['tags'])}\n"
                        "Click = select · Ctrl+click = multi-select · right-click = menu")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        cover = QLabel(item["name"][-2:])
        cover.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cover.setStyleSheet(f"background: {P.SURFACE}; color: {P.MUTED}; font-size: 20pt;"
                            "border-radius: 3px;")
        layout.addWidget(cover, 1)
        layout.addWidget(title(item["name"]))
        badges = QHBoxLayout(); badges.setSpacing(4)
        if "new" in item["tags"]:
            badges.addWidget(badge("NEW", P.SECONDARY, P.TEXT))
        if "favourite" in item["tags"]:
            badges.addWidget(badge("★", P.ACCENT, P.TEXT_ON_ACCENT))
        if item["score"] == 5:
            badges.addWidget(badge("TOP", TOP_BADGE, P.TEXT_ON_LIGHT))
        badges.addStretch()
        layout.addLayout(badges)

    def set_selected(self, selected: bool, multi: bool = False) -> None:
        self.selected = selected
        if not selected:
            self.setStyleSheet("")                                   # back to #Card
        else:
            color = P.HIGHLIGHT if multi else P.ACCENT
            self.setStyleSheet(f"QFrame#Card {{ border: 2px solid {color}; }}")

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            multi = bool(event.modifiers() & Qt.KeyboardModifier.ControlModifier)
            self.showcase.select(self, multi)
        super().mousePressEvent(event)

    def contextMenuEvent(self, event) -> None:  # noqa: N802
        menu = QMenu(self)
        menu.addAction("Select", lambda: self.showcase.select(self, False))
        menu.addAction("Copy name", lambda: self.showcase.copy(self.item["name"]))
        menu.addSeparator()
        tags = menu.addMenu("Tags")
        for tag in self.item["tags"]:
            tags.addAction(f"#{tag}")
        disabled = menu.addAction("Delete (disabled)")
        disabled.setEnabled(False)
        menu.exec(event.globalPos())


# ── Main window ────────────────────────────────────────────────────────────────────────

class Showcase(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"Jello Style {jello_style.__version__} - Qt showcase")
        self.resize(1280, 800)

        self.cards: list[WallCard] = []
        self.timer = QTimer(self, interval=30)
        self.timer.timeout.connect(self._tick)

        self.sidebar = self._build_sidebar()
        self.detail = self._build_detail()
        tabs = QTabWidget()
        tabs.addTab(self._build_wall(), "Wall")
        tabs.addTab(self._build_controls(), "Controls")
        tabs.addTab(self._build_data(), "Data")
        tabs.addTab(self._build_palette(), "Palette")
        tabs.setTabToolTip(0, "Cover wall - cards in a FlowLayout")
        tabs.setTabToolTip(3, "Every colour in jello_style.palette")

        splitter = QSplitter()
        for widget in (self.sidebar, tabs, self.detail):
            splitter.addWidget(widget)
        splitter.setSizes([250, 780, 250])
        splitter.setChildrenCollapsible(False)
        self.setCentralWidget(splitter)

        self._build_status_bar()
        self._build_menus_and_toolbar()
        self.apply_filters()
        self.set_status("Ready - hover anything for a tooltip", "Ok")

    # ── Sidebar ────────────────────────────────────────────────────────────────────────

    def _build_sidebar(self) -> QWidget:
        side = QWidget(); side.setObjectName("Sidebar")
        layout = QVBoxLayout(side)
        layout.setContentsMargins(P.GAP, P.GAP, P.GAP, P.GAP)
        layout.setSpacing(P.GAP // 2)

        layout.addWidget(title("Search"))
        self.search = QLineEdit(placeholderText="Filter by name…", clearButtonEnabled=True)
        self.search.setToolTip("Filters the wall as you type")
        self.search.textChanged.connect(self.apply_filters)
        layout.addWidget(self.search)

        layout.addSpacing(P.GAP // 2)
        layout.addWidget(title("Tags"))
        hint = QLabel("include → exclude → off"); hint.setToolTip("Click a chip to cycle")
        layout.addWidget(hint)
        holder = QWidget()
        flow = qt_theme.FlowLayout(holder)
        self.chips = []
        for tag in TAGS:
            count = sum(tag in item["tags"] for item in ITEMS)
            color = P.SECONDARY if tag in ("new", "archived") else P.ACCENT
            chip = qt_theme.TriStateChip(tag, count, include_color=color)
            chip.setToolTip(f"{count} items tagged #{tag}")
            chip.state_changed.connect(self.apply_filters)
            flow.addWidget(chip)
            self.chips.append(chip)
        layout.addWidget(holder)

        layout.addSpacing(P.GAP // 2)
        layout.addWidget(title("Sort"))
        self.sort = QComboBox()
        self.sort.addItems(["Name", "Score (high first)", "Size (large first)"])
        self.sort.currentIndexChanged.connect(self.apply_filters)
        layout.addWidget(self.sort)
        self.top_only = QCheckBox("Only score 4+")
        self.top_only.toggled.connect(self.apply_filters)
        layout.addWidget(self.top_only)

        reset = QPushButton("Reset filters"); reset.setToolTip("Clear search, chips and options")
        reset.clicked.connect(self.reset_filters)
        layout.addWidget(reset)
        layout.addStretch()
        self.count_label = title("", "SectionTitle")
        layout.addWidget(self.count_label)
        return side

    # ── Detail pane ────────────────────────────────────────────────────────────────────

    def _build_detail(self) -> QWidget:
        pane = QWidget(); pane.setObjectName("DetailPane")
        layout = QVBoxLayout(pane)
        layout.setContentsMargins(P.GAP, P.GAP, P.GAP, P.GAP)
        layout.addWidget(title("Details"))
        self.detail_name = title("Nothing selected", "Title")
        self.detail_name.setWordWrap(True)
        layout.addWidget(self.detail_name)
        self.detail_info = QLabel("Click a card on the wall.")
        self.detail_info.setWordWrap(True)
        layout.addWidget(self.detail_info)
        layout.addSpacing(P.GAP)
        layout.addWidget(title("Notes"))
        notes = QPlainTextEdit(placeholderText="QPlainTextEdit - type anything…")
        layout.addWidget(notes, 1)
        self.open_button = QPushButton("Open selected"); self.open_button.setObjectName("Primary")
        self.open_button.setToolTip("The one primary action of this pane")
        self.open_button.setEnabled(False)
        self.open_button.clicked.connect(self.open_selected)
        layout.addWidget(self.open_button)
        return pane

    # ── Tabs ───────────────────────────────────────────────────────────────────────────

    def _build_wall(self) -> QWidget:
        holder = QWidget()
        self.wall = qt_theme.FlowLayout(holder, margin=P.GAP, spacing=P.GAP)
        for item in ITEMS:
            card = WallCard(item, self)
            self.cards.append(card)
            self.wall.addWidget(card)
        self.empty = QLabel("Nothing matches the filters.")
        self.empty.setObjectName("Warn")
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.empty)
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setWidget(holder)
        layout.addWidget(scroll, 1)
        return page

    def _build_controls(self) -> QWidget:
        page = QWidget()
        grid = QGridLayout(page)
        grid.setContentsMargins(P.MARGIN, P.MARGIN, P.MARGIN, P.MARGIN)
        grid.setHorizontalSpacing(P.MARGIN)
        grid.setVerticalSpacing(P.GAP)
        grid.addWidget(title("Controls", "Title"), 0, 0, 1, 2)

        # Buttons card
        card, box = self._card("Buttons")
        row = QHBoxLayout()
        normal = QPushButton("Button"); normal.setToolTip("QPushButton")
        disabled = QPushButton("Disabled"); disabled.setEnabled(False)
        toggle = QPushButton("Toggle"); toggle.setCheckable(True)
        toggle.setToolTip("Checkable QPushButton - :checked state")
        primary = QPushButton("Primary"); primary.setObjectName("Primary")
        primary.setToolTip('setObjectName("Primary") - one per window')
        primary.clicked.connect(lambda: self.set_status("Primary clicked", "Ok"))
        for widget in (normal, disabled, toggle, primary):
            row.addWidget(widget)
        box.addLayout(row)
        row = QHBoxLayout()
        tool = QToolButton(); tool.setText("Tool ▾"); tool.setToolTip("QToolButton with a menu")
        tool.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        tool_menu = QMenu(tool)
        for text in ("First", "Second", "Third"):
            tool_menu.addAction(text, lambda _=False, t=text: self.set_status(f"Menu: {t}"))
        tool.setMenu(tool_menu)
        row.addWidget(tool)
        msg = QPushButton("Message box…"); msg.clicked.connect(self.show_message)
        ask = QPushButton("Input dialog…"); ask.clicked.connect(self.ask_input)
        row.addWidget(msg); row.addWidget(ask); row.addStretch()
        box.addLayout(row)
        grid.addWidget(card, 1, 0)

        # Inputs card
        card, box = self._card("Inputs")
        box.addWidget(QLineEdit(placeholderText="QLineEdit with placeholder", clearButtonEnabled=True))
        combo = QComboBox(); combo.addItems(["Read-only combo", "Second", "Third"])
        editable = QComboBox(); editable.setEditable(True)
        editable.addItems(["Editable combo", "Type your own"])
        spin = QSpinBox(); spin.setRange(0, 100); spin.setValue(42); spin.setSuffix(" %")
        spin.setToolTip("QSpinBox")
        row = QHBoxLayout(); row.addWidget(combo); row.addWidget(editable); row.addWidget(spin)
        box.addLayout(row)
        grid.addWidget(card, 1, 1)

        # Checks card
        card, box = self._card("Checks & radios")
        row = QHBoxLayout()
        row.addWidget(QCheckBox("Checkbox"))
        checked = QCheckBox("Checked"); checked.setChecked(True); row.addWidget(checked)
        off = QCheckBox("Disabled"); off.setEnabled(False); row.addWidget(off)
        box.addLayout(row)
        row = QHBoxLayout()
        for i, text in enumerate(("Small", "Medium", "Large")):
            radio = QRadioButton(text); radio.setChecked(i == 1); row.addWidget(radio)
        box.addLayout(row)
        grid.addWidget(card, 2, 0)

        # Progress card
        card, box = self._card("Progress")
        self.demo_progress = QProgressBar(); self.demo_progress.setValue(35)
        busy = QProgressBar(); busy.setRange(0, 0); busy.setToolTip("Indeterminate (range 0, 0)")
        run = QPushButton("Run job  (F5)"); run.clicked.connect(self.start_job)
        box.addWidget(self.demo_progress); box.addWidget(busy); box.addWidget(run)
        grid.addWidget(card, 2, 1)

        # Status card
        card, box = self._card("Status colours")
        row = QHBoxLayout()
        for kind in ("Ok", "Warn", "Error", ""):
            label = QLabel(f"{kind or 'Muted'} text")
            label.setObjectName(kind)
            row.addWidget(label)
        box.addLayout(row)
        row = QHBoxLayout()
        for kind in ("Ok", "Warn", "Error"):
            button = QPushButton(f"Status: {kind}")
            button.setToolTip("Sets the status bar message colour")
            button.clicked.connect(lambda _=False, k=kind: self.set_status(f"{k} message", k))
            row.addWidget(button)
        box.addLayout(row)
        grid.addWidget(card, 3, 0, 1, 2)

        grid.setRowStretch(4, 1)
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setWidget(page)
        return scroll

    def _build_data(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(P.MARGIN, P.MARGIN, P.MARGIN, P.MARGIN)
        splitter = QSplitter(Qt.Orientation.Vertical)

        tree = QTreeWidget()
        tree.setHeaderLabels(["Tag", "Items"])
        for tag in TAGS:
            parent = QTreeWidgetItem([f"#{tag}", ""])
            members = [item["name"] for item in ITEMS if tag in item["tags"]]
            parent.setText(1, str(len(members)))
            for name in members:
                parent.addChild(QTreeWidgetItem([name, ""]))
            tree.addTopLevelItem(parent)
        tree.expandItem(tree.topLevelItem(0))
        tree.setColumnWidth(0, 220)

        table = QTableWidget(len(ITEMS), 4)
        table.setHorizontalHeaderLabels(["Name", "Tags", "Score", "Size (MB)"])
        for row, item in enumerate(ITEMS):
            table.setItem(row, 0, QTableWidgetItem(item["name"]))
            table.setItem(row, 1, QTableWidgetItem(", ".join(item["tags"])))
            for col, key in ((2, "score"), (3, "size")):
                cell = QTableWidgetItem()
                cell.setData(Qt.ItemDataRole.DisplayRole, item[key])   # numeric sort
                table.setItem(row, col, cell)
        table.setSortingEnabled(True)
        table.horizontalHeader().setStretchLastSection(True)
        table.setToolTip("Click a header to sort")

        splitter.addWidget(tree)
        splitter.addWidget(table)
        layout.addWidget(title("Tree & table"))
        layout.addWidget(splitter, 1)
        return page

    def _build_palette(self) -> QWidget:
        page = QWidget()
        grid = QGridLayout(page)
        grid.setContentsMargins(P.MARGIN, P.MARGIN, P.MARGIN, P.MARGIN)
        names = [n for n in dir(P) if n.isupper() and isinstance(getattr(P, n), str)
                 and getattr(P, n).startswith("#")]
        for i, name in enumerate(names):
            value = getattr(P, name)
            swatch = QPushButton()
            swatch.setFixedSize(56, 26)
            swatch.setCursor(Qt.CursorShape.PointingHandCursor)
            swatch.setToolTip(f"palette.{name} = {value}\nClick to copy")
            swatch.setStyleSheet(f"QPushButton {{ background: {value}; border: 1px solid {P.BORDER}; }}"
                                 f"QPushButton:hover {{ border: 2px solid {P.TEXT}; }}")
            swatch.clicked.connect(lambda _=False, v=value: self.copy(v))
            row, col = i // 3, (i % 3) * 2
            grid.addWidget(swatch, row, col)
            grid.addWidget(QLabel(f"{name}\n{value}"), row, col + 1)
        grid.setRowStretch(len(names) // 3 + 1, 1)
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setWidget(page)
        return scroll

    def _card(self, heading: str) -> tuple[QFrame, QVBoxLayout]:
        card = QFrame(); card.setObjectName("Card")
        box = QVBoxLayout(card)
        box.setContentsMargins(P.GAP, P.GAP, P.GAP, P.GAP)
        box.addWidget(title(heading))
        return card, box

    # ── Chrome: menus, toolbar, status bar ─────────────────────────────────────────────

    def _build_menus_and_toolbar(self) -> None:
        bar = self.menuBar()
        file_menu = bar.addMenu("&File")
        file_menu.addAction("Message box…", self.show_message)
        file_menu.addAction("Input dialog…", self.ask_input)
        recent = file_menu.addMenu("Recent")
        for name in ("alpha.txt", "beta.txt"):
            recent.addAction(name)
        file_menu.addSeparator()
        quit_action = file_menu.addAction("Quit", self.close)
        quit_action.setShortcut(QKeySequence("Ctrl+Q"))

        view_menu = bar.addMenu("&View")
        for text, widget in (("Sidebar", self.sidebar), ("Detail pane", self.detail)):
            action = view_menu.addAction(text)
            action.setCheckable(True); action.setChecked(True)
            action.toggled.connect(widget.setVisible)

        job_action = QAction("Run job", self, shortcut=QKeySequence("F5"))
        job_action.setToolTip("Animate the progress bars (F5)")
        job_action.triggered.connect(self.start_job)
        select_all = QAction("Select all", self, shortcut=QKeySequence("Ctrl+A"))
        select_all.setToolTip("Multi-select every visible card (Ctrl+A)")
        select_all.triggered.connect(self.select_all)
        clear = QAction("Clear selection", self, shortcut=QKeySequence("Esc"))
        clear.triggered.connect(lambda: self.select(None, False))
        compact = QAction("Compact", self, checkable=True)
        compact.setToolTip("Checkable toolbar action - shrinks the cards")
        compact.toggled.connect(self.set_compact)
        edit_menu = bar.addMenu("&Edit")
        for action in (job_action, select_all, clear):
            edit_menu.addAction(action)

        help_menu = bar.addMenu("&Help")
        help_menu.addAction("About", lambda: QMessageBox.about(
            self, "About", f"jello_style {jello_style.__version__}\nQt showcase"))

        toolbar = self.addToolBar("Main")
        toolbar.setMovable(False)
        for action in (job_action, select_all, clear):
            toolbar.addAction(action)
        toolbar.addSeparator()
        toolbar.addAction(compact)

    def _build_status_bar(self) -> None:
        self.status = QLabel()
        self.progress = QProgressBar(); self.progress.setFixedWidth(200); self.progress.hide()
        version = QLabel(f"jello_style {jello_style.__version__}")
        version.setToolTip("Version of the installed / local package")
        self.statusBar().addWidget(self.status, 1)
        self.statusBar().addPermanentWidget(self.progress)
        self.statusBar().addPermanentWidget(version)

    # ── Behaviour ──────────────────────────────────────────────────────────────────────

    def set_status(self, message: str, kind: str = "") -> None:
        self.status.setText(message)
        self.status.setObjectName(kind)
        restyle(self.status)

    def copy(self, text: str) -> None:
        QApplication.clipboard().setText(text)
        self.set_status(f"Copied {text}", "Ok")

    def reset_filters(self) -> None:
        self.search.clear()
        for chip in self.chips:
            chip.set_state(chip.STATE_NEUTRAL)
        self.top_only.setChecked(False)
        self.sort.setCurrentIndex(0)
        self.apply_filters()

    def apply_filters(self) -> None:
        text = self.search.text().lower()
        keys = {0: lambda c: c.item["name"], 1: lambda c: -c.item["score"],
                2: lambda c: -c.item["size"]}
        shown = 0
        for card in self.cards:
            self.wall.removeWidget(card)
        for card in sorted(self.cards, key=keys[self.sort.currentIndex()]):
            tags = card.item["tags"]
            visible = (text in card.item["name"].lower()
                       and (not self.top_only.isChecked() or card.item["score"] >= 4)
                       and all(chip.label in tags for chip in self.chips
                               if chip.state == chip.STATE_INCLUDE)
                       and not any(chip.label in tags for chip in self.chips
                                   if chip.state == chip.STATE_EXCLUDE))
            self.wall.addWidget(card)
            card.setVisible(visible)
            shown += visible
        self.empty.setVisible(shown == 0)
        self.count_label.setText(f"{shown} / {len(self.cards)} SHOWN")

    def select(self, card: WallCard | None, multi: bool) -> None:
        if not multi:
            for other in self.cards:
                if other is not card:
                    other.set_selected(False)
        if card is not None:
            card.set_selected(not card.selected if multi else True, multi)
        chosen = [c for c in self.cards if c.selected]
        self.open_button.setEnabled(bool(chosen))
        if len(chosen) == 1:
            item = chosen[0].item
            self.detail_name.setText(item["name"])
            self.detail_info.setText(f"Tags: {', '.join('#' + t for t in item['tags'])}\n"
                                     f"Score: {'★' * item['score']}\nSize: {item['size']} MB")
        elif chosen:
            self.detail_name.setText(f"{len(chosen)} selected")
            self.detail_info.setText("Multi-select - HIGHLIGHT frame.")
        else:
            self.detail_name.setText("Nothing selected")
            self.detail_info.setText("Click a card on the wall.")

    def select_all(self) -> None:
        for card in self.cards:
            card.set_selected(card.isVisible(), multi=True)
        self.select(None, True)

    def set_compact(self, compact: bool) -> None:
        for card in self.cards:
            card.setFixedSize(130 if compact else 170, 115 if compact else 150)
        self.set_status("Compact cards" if compact else "Normal cards")

    def open_selected(self) -> None:
        names = [c.item["name"] for c in self.cards if c.selected]
        self.set_status(f"Opened {', '.join(names)}", "Ok")

    def show_message(self) -> None:
        answer = QMessageBox.question(self, "Question", "QMessageBox in the Jello style.\n"
                                      "Did it pick up the theme?")
        ok = answer == QMessageBox.StandardButton.Yes
        self.set_status("Message box: yes" if ok else "Message box: no", "Ok" if ok else "Warn")

    def ask_input(self) -> None:
        text, ok = QInputDialog.getText(self, "Input", "Type something:")
        if ok:
            self.set_status(f"You typed: {text}", "Ok")

    def start_job(self) -> None:
        if self.timer.isActive():
            return
        self.progress.setValue(0); self.progress.show()
        self.demo_progress.setValue(0)
        self.set_status("Working…", "Warn")
        self.timer.start()

    def _tick(self) -> None:
        value = self.progress.value() + 1
        self.progress.setValue(value)
        self.demo_progress.setValue(value)
        if value >= 100:
            self.timer.stop()
            QTimer.singleShot(600, self.progress.hide)
            self.set_status("Job finished", "Ok")


def main() -> None:
    app = QApplication(sys.argv)
    qt_theme.apply(app)
    window = Showcase()
    window.show()
    qt_theme.dark_title_bar(window)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
