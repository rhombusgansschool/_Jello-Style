"""qt_theme - the Jello stylesheet and small widgets for PySide6 apps.

    from PySide6.QtWidgets import QApplication
    from jello_style import qt_theme

    app = QApplication(sys.argv)
    qt_theme.apply(app)                       # once, before building windows

Styling is driven by object names, not per-widget setStyleSheet calls:

    button.setObjectName("Primary")           # the one accent button per window
    label.setObjectName("SectionTitle")       # small bold caps heading
    label.setObjectName("Title")              # big window / item title
    panel.setObjectName("Sidebar")            # SURFACE-coloured panel (also "DetailPane",
                                              #   "Panel")
    frame.setObjectName("Card")               # CARD-coloured, bordered box
    label.setObjectName("Ok" | "Warn" | "Error")   # status text colours

Ported from Project Jello's MediaLib/theme.py.
"""

from __future__ import annotations

from PySide6.QtCore import QPoint, QRect, QSize, Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QApplication, QLayout, QLayoutItem, QPushButton,
                               QSizePolicy, QWidget)

from . import palette as P
from ._win import dark_title_bar as _dark_title_bar


def app_stylesheet() -> str:
    return f"""
        QMainWindow, QDialog, QListView, QTreeWidget, QScrollArea, QAbstractScrollArea {{
            background: {P.BG}; border: none; color: {P.TEXT}; }}
        QWidget#Sidebar, QWidget#DetailPane, QWidget#Panel {{ background: {P.SURFACE}; }}
        QFrame#Card {{ background: {P.CARD}; border: 1px solid {P.BORDER};
            border-radius: {P.RADIUS}px; }}
        QToolBar {{ background: {P.SURFACE}; border: none; padding: 6px; spacing: 8px; }}
        QLabel {{ color: {P.MUTED}; background: transparent; }}
        QLabel#SectionTitle {{ color: {P.TEXT}; font-weight: bold; letter-spacing: 1px; }}
        QLabel#Title {{ color: {P.TEXT}; font-size: {P.SIZE_TITLE}pt; font-weight: bold; }}
        QLabel#Ok {{ color: {P.OK}; }}
        QLabel#Warn {{ color: {P.WARN}; }}
        QLabel#Error {{ color: {P.ERROR}; }}
        QLineEdit, QPlainTextEdit, QTextEdit, QListWidget, QTableWidget, QSpinBox {{
            background: {P.INPUT_BG}; color: {P.TEXT}; border: 1px solid {P.BORDER};
            border-radius: {P.RADIUS}px; padding: 4px;
            selection-background-color: {P.ACCENT}; }}
        QComboBox, QPushButton, QToolButton {{
            background: {P.BUTTON}; color: {P.TEXT}; border: 1px solid {P.BORDER};
            border-radius: {P.RADIUS}px; padding: 5px 12px; }}
        QPushButton:hover, QComboBox:hover, QToolButton:hover {{ background: {P.BUTTON_HOVER}; }}
        QPushButton:pressed, QToolButton:pressed {{ background: {P.BUTTON_PRESSED}; }}
        QPushButton:disabled, QToolButton:disabled {{ background: {P.BUTTON_DISABLED};
            color: {P.MUTED}; }}
        QPushButton#Primary {{ background: {P.ACCENT}; border-color: {P.ACCENT};
            color: {P.TEXT_ON_ACCENT}; }}
        QPushButton#Primary:hover {{ background: {P.ACCENT_HOVER}; }}
        QPushButton#Primary:pressed {{ background: {P.ACCENT_PRESSED}; }}
        QCheckBox, QRadioButton {{ color: {P.MUTED}; spacing: 6px; }}
        QCheckBox::indicator {{ width: 14px; height: 14px; border: 1px solid {P.BORDER};
            border-radius: 3px; background: {P.INPUT_BG}; }}
        QCheckBox::indicator:checked {{ background: {P.ACCENT}; border-color: {P.ACCENT}; }}
        QComboBox QAbstractItemView {{ background: {P.SURFACE}; color: {P.TEXT};
            selection-background-color: {P.ACCENT}; }}
        QProgressBar {{ background: {P.INPUT_BG}; border: 1px solid {P.BORDER};
            border-radius: {P.RADIUS}px; color: {P.TEXT}; text-align: center; }}
        QProgressBar::chunk {{ background: {P.ACCENT}; border-radius: {P.RADIUS}px; }}
        QStatusBar {{ background: {P.SURFACE}; color: {P.MUTED}; }}
        QTabWidget::pane {{ border: 1px solid {P.BORDER}; }}
        QTabBar::tab {{ background: {P.SURFACE}; color: {P.MUTED}; padding: 6px 16px; }}
        QTabBar::tab:selected {{ background: {P.BUTTON}; color: {P.TEXT}; }}
        QHeaderView::section {{ background: {P.SURFACE}; color: {P.TEXT};
            border: none; padding: 4px; }}
        QTreeWidget {{ background: {P.INPUT_BG}; border: 1px solid {P.BORDER};
            border-radius: {P.RADIUS}px; }}
        QSplitter::handle {{ background: {P.SPLITTER}; width: 3px; }}
        QScrollBar:vertical {{ background: {P.BG}; width: 12px; }}
        QScrollBar::handle:vertical {{ background: {P.BORDER}; border-radius: 6px;
            min-height: 40px; }}
        QScrollBar:horizontal {{ background: {P.BG}; height: 12px; }}
        QScrollBar::handle:horizontal {{ background: {P.BORDER}; border-radius: 6px;
            min-width: 40px; }}
        QScrollBar::add-line, QScrollBar::sub-line {{ width: 0; height: 0; }}
        QPushButton:checked, QToolButton:checked {{ background: {P.ACCENT_PRESSED};
            border-color: {P.ACCENT}; }}
        QRadioButton::indicator {{ width: 12px; height: 12px; border: 1px solid {P.BORDER};
            border-radius: 7px; background: {P.INPUT_BG}; }}
        QRadioButton::indicator:checked {{ background: {P.ACCENT}; border-color: {P.ACCENT}; }}
        QTableWidget, QTableView {{ gridline-color: {P.BORDER}; }}
        QTableCornerButton::section {{ background: {P.SURFACE}; border: none; }}
        QMenuBar {{ background: {P.SURFACE}; color: {P.TEXT}; }}
        QMenuBar::item {{ background: transparent; padding: 4px 10px; }}
        QMenuBar::item:selected {{ background: {P.BUTTON_HOVER}; }}
        QMenu {{ background: {P.SURFACE}; color: {P.TEXT}; border: 1px solid {P.BORDER}; }}
        QMenu::item {{ padding: 5px 24px 5px 20px; }}
        QMenu::item:selected {{ background: {P.ACCENT}; }}
        QMenu::item:disabled {{ color: {P.MUTED}; }}
        QMenu::separator {{ height: 1px; background: {P.BORDER}; margin: 4px 8px; }}
        QToolTip {{ background: {P.SURFACE}; color: {P.TEXT}; border: 1px solid {P.BORDER};
            padding: 4px; }}
    """


def apply(app: QApplication) -> None:
    """Set the Jello font and stylesheet on the whole application. Call once."""
    app.setFont(QFont(P.FONT_FAMILY, 9))
    app.setStyleSheet(app_stylesheet())


def dark_title_bar(window: QWidget) -> bool:
    """Dark Windows caption bar for a top-level window. Call after show()."""
    return _dark_title_bar(int(window.winId()))


class FlowLayout(QLayout):
    """Left-to-right wrap layout (Qt ships none) - used for chip rows."""

    def __init__(self, parent: QWidget | None = None, margin: int = 0, spacing: int = 6) -> None:
        super().__init__(parent)
        self.setContentsMargins(margin, margin, margin, margin)
        self._spacing = spacing
        self._items: list[QLayoutItem] = []

    def addItem(self, item: QLayoutItem) -> None:  # noqa: N802
        self._items.append(item)

    def count(self) -> int:
        return len(self._items)

    def itemAt(self, index: int) -> QLayoutItem | None:  # noqa: N802
        return self._items[index] if 0 <= index < len(self._items) else None

    def takeAt(self, index: int) -> QLayoutItem | None:  # noqa: N802
        return self._items.pop(index) if 0 <= index < len(self._items) else None

    def expandingDirections(self) -> Qt.Orientation:  # noqa: N802
        return Qt.Orientation(0)

    def hasHeightForWidth(self) -> bool:  # noqa: N802
        return True

    def heightForWidth(self, width: int) -> int:  # noqa: N802
        return self._layout(QRect(0, 0, width, 0), apply=False)

    def setGeometry(self, rect: QRect) -> None:  # noqa: N802
        super().setGeometry(rect)
        self._layout(rect, apply=True)

    def sizeHint(self) -> QSize:  # noqa: N802
        return self.minimumSize()

    def minimumSize(self) -> QSize:  # noqa: N802
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        margins = self.contentsMargins()
        size += QSize(margins.left() + margins.right(), margins.top() + margins.bottom())
        return size

    def _layout(self, rect: QRect, apply: bool) -> int:
        margins = self.contentsMargins()
        x = rect.x() + margins.left()
        y = rect.y() + margins.top()
        line_height = 0
        right = rect.right() - margins.right()
        for item in self._items:
            hint = item.sizeHint()
            if x + hint.width() > right and line_height > 0:
                x = rect.x() + margins.left()
                y += line_height + self._spacing
                line_height = 0
            if apply:
                item.setGeometry(QRect(QPoint(x, y), hint))
            x += hint.width() + self._spacing
            line_height = max(line_height, hint.height())
        return y + line_height + margins.bottom() - rect.y()


class TriStateChip(QPushButton):
    """Filter chip cycling neutral -> include -> exclude -> neutral.

    `include_color` colours the include state - ACCENT by default, SECONDARY for a
    second category so the two origins stay distinguishable side by side.
    """

    STATE_NEUTRAL, STATE_INCLUDE, STATE_EXCLUDE = 0, 1, 2
    state_changed = Signal()

    def __init__(self, label: str, count: int = 0, include_color: str = P.ACCENT) -> None:
        text = f"{label}  ({count})" if count else label
        super().__init__(text)
        self.label = label
        self.include_color = include_color
        self.state = self.STATE_NEUTRAL
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.clicked.connect(self._cycle)
        self._restyle()

    def set_state(self, state: int) -> None:
        self.state = state % 3
        self._restyle()

    def _cycle(self) -> None:
        self.set_state(self.state + 1)
        self.state_changed.emit()

    def _restyle(self) -> None:
        base = (f"background: %s; color: {P.TEXT}; border: 1px solid {P.BORDER};"
                f"border-radius: {P.CHIP_RADIUS}px; padding: 3px 10px; font-size: 8pt;")
        if self.state == self.STATE_INCLUDE:
            style = base % self.include_color + f"border-color: {self.include_color};"
        elif self.state == self.STATE_EXCLUDE:
            style = base % P.EXCLUDE + "text-decoration: line-through;"
        else:
            style = base % P.CHIP
        self.setStyleSheet(style)
