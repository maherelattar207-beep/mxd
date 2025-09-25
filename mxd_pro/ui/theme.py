from PyQt5.QtWidgets import QLabel, QToolTip
from PyQt5.QtGui import QFont

class Theme:
    """Defines the color palette and styles for the application."""
    RED = "#C0392B"
    GOLD = "#D4AF37"
    BLACK = "#000000"
    DARK_GREY = "#1C1C1C"
    MEDIUM_GREY = "#2C3E50"
    LIGHT_GREY = "#BDC3C7"
    WHITE = "#ECF0F1"

    STYLESHEET = f"""
        QWidget {{
            background-color: {DARK_GREY};
            color: {WHITE};
            font-family: "Segoe UI", Arial, sans-serif;
        }}
        QMainWindow {{
            background-color: {BLACK};
        }}
        QGroupBox {{
            background-color: {MEDIUM_GREY};
            border: 1px solid {GOLD};
            border-radius: 5px;
            margin-top: 1ex;
            font-weight: bold;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 3px;
            color: {GOLD};
        }}
        QPushButton {{
            background-color: {RED};
            color: {WHITE};
            border: none;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: #E74C3C;
        }}
        QPushButton:pressed {{
            background-color: #A93226;
        }}
        QLabel {{
            background-color: transparent;
        }}
        QLineEdit, QTextEdit {{
            background-color: {DARK_GREY};
            border: 1px solid {MEDIUM_GREY};
            border-radius: 5px;
            padding: 5px;
            color: {WHITE};
        }}
        QTabWidget::pane {{
            border-top: 2px solid {GOLD};
        }}
        QTabBar::tab {{
            background: {MEDIUM_GREY};
            color: {WHITE};
            padding: 10px;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        }}
        QTabBar::tab:selected {{
            background: {DARK_GREY};
            border: 1px solid {GOLD};
            border-bottom: none;
        }}
        QToolTip {{
            background-color: {BLACK};
            color: {WHITE};
            border: 1px solid {GOLD};
            padding: 5px;
        }}
    """

class ToolTip(QLabel):
    """A custom QLabel for tooltips."""
    def __init__(self, text, parent=None):
        super().__init__("?", parent)
        self.setToolTip(text)
        font = QFont()
        font.setBold(True)
        self.setFont(font)
        self.setStyleSheet(f"background-color: {Theme.GOLD}; color: {Theme.BLACK}; border-radius: 8px; padding: 2px;")