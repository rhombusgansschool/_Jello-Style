"""Qt showcase - every jello_style element in one window. Run: python examples/qt_example.py"""

import sys
from pathlib import Path

# Run straight from the repo without installing.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame, QGridLayout,
                               QHBoxLayout, QLabel, QLineEdit, QListWidget, QMainWindow,
                               QProgressBar, QPushButton, QRadioButton, QScrollArea,
                               QSplitter, QTabWidget, QVBoxLayout, QWidget)

from jello_style import palette as P
from jello_style import qt_theme


def section(layout: QVBoxLayout, title: str) -> None:
    label = QLabel(title.upper())
    label.setObjectName("SectionTitle")
    layout.addWidget(label)


def build_sidebar() -> QWidget:
    side = QWidget()
    side.setObjectName("Sidebar")
    layout = QVBoxLayout(side)
    section(layout, "Chips")
    layout.addWidget(QLabel("Click to cycle"))
    chips = QWidget()
    flow = qt_theme.FlowLayout(chips)
    for name in ("red", "blue", "green", "favourite", "new", "archived"):
        color = P.SECONDARY if name == "new" else P.ACCENT
        flow.addWidget(qt_theme.TriStateChip(name, count=3, include_color=color))
    layout.addWidget(chips)
    section(layout, "Options")
    layout.addWidget(QCheckBox("Checkbox"))
    checked = QCheckBox("Checked"); checked.setChecked(True)
    layout.addWidget(checked)
    layout.addWidget(QRadioButton("Radio button"))
    layout.addStretch()
    return side


def build_controls() -> QWidget:
    page = QWidget()
    layout = QVBoxLayout(page)
    layout.setContentsMargins(P.MARGIN, P.MARGIN, P.MARGIN, P.MARGIN)
    layout.setSpacing(P.GAP)

    title = QLabel("Jello Style"); title.setObjectName("Title")
    layout.addWidget(title)
    layout.addWidget(QLabel("Plain QLabel text is muted grey."))

    section(layout, "Buttons")
    row = QHBoxLayout()
    row.addWidget(QPushButton("Button"))
    disabled = QPushButton("Disabled"); disabled.setEnabled(False)
    row.addWidget(disabled)
    primary = QPushButton("Primary"); primary.setObjectName("Primary")
    row.addWidget(primary)
    row.addStretch()
    layout.addLayout(row)

    section(layout, "Inputs")
    layout.addWidget(QLineEdit(placeholderText="QLineEdit…"))
    combo = QComboBox(); combo.addItems(["QComboBox", "Second", "Third"])
    layout.addWidget(combo)
    progress = QProgressBar(); progress.setValue(60)
    layout.addWidget(progress)

    section(layout, "Status text")
    for kind in ("Ok", "Warn", "Error"):
        label = QLabel(f"{kind} message"); label.setObjectName(kind)
        layout.addWidget(label)

    section(layout, "Card")
    card = QFrame(); card.setObjectName("Card")
    card_layout = QVBoxLayout(card)
    heading = QLabel("CARD TITLE"); heading.setObjectName("SectionTitle")
    card_layout.addWidget(heading)
    card_layout.addWidget(QLabel("A QFrame named \"Card\" - CARD background, 1 px border."))
    layout.addWidget(card)
    layout.addStretch()

    scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setWidget(page)
    return scroll


def build_palette() -> QWidget:
    page = QWidget()
    grid = QGridLayout(page)
    grid.setContentsMargins(P.MARGIN, P.MARGIN, P.MARGIN, P.MARGIN)
    names = [n for n in dir(P) if n.isupper() and isinstance(getattr(P, n), str)
             and getattr(P, n).startswith("#")]
    for i, name in enumerate(names):
        swatch = QLabel(); swatch.setFixedSize(48, 24)
        swatch.setStyleSheet(f"background: {getattr(P, name)}; border: 1px solid {P.BORDER};")
        grid.addWidget(swatch, i // 2, (i % 2) * 2)
        grid.addWidget(QLabel(f"{name}  {getattr(P, name)}"), i // 2, (i % 2) * 2 + 1)
    grid.setRowStretch(len(names) // 2 + 1, 1)
    return page


def main() -> None:
    app = QApplication(sys.argv)
    qt_theme.apply(app)

    tabs = QTabWidget()
    tabs.addTab(build_controls(), "Controls")
    items = QListWidget(); items.addItems([f"List item {i}" for i in range(1, 30)])
    tabs.addTab(items, "List")
    tabs.addTab(build_palette(), "Palette")

    splitter = QSplitter()
    splitter.addWidget(build_sidebar())
    splitter.addWidget(tabs)
    splitter.setSizes([260, 640])

    window = QMainWindow()
    window.setWindowTitle("Jello Style - Qt example")
    window.addToolBar("Main").addWidget(QPushButton("Toolbar button"))
    window.setCentralWidget(splitter)
    window.statusBar().showMessage("Status bar")
    window.resize(900, 620)
    window.show()
    qt_theme.dark_title_bar(window)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
