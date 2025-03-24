# gui/style.py

LIGHT_STYLE = """
QMainWindow, QDialog {
    background-color: #ffffff;
    color: #000000;
    border-radius: 12px;
}
QPushButton {
    background-color: #4a90e2;
    color: #ffffff;
    border-radius: 10px;
    padding: 6px 12px;
}
QPushButton:hover {
    background-color: #357ABD;
}
QLineEdit, QTextEdit {
    background-color: #f0f0f0;
    color: #000000;
    border-radius: 8px;
    padding: 5px;
    border: none;
}
QLabel {
    color: #000000;
}
QListWidget {
    background-color: #f0f0f0;
    color: #000000;
    border-radius: 8px;
}
QScrollBar:vertical {
    background: #d0d0d0;
    width: 12px;
    border-radius: 6px;
}
QTableWidget {
    background-color: #ffffff;
    color: #000000;
    gridline-color: #cccccc;
    selection-background-color: #4a90e2;
    selection-color: #ffffff;
    border-radius: 6px;
}
QHeaderView::section {
    background-color: #e0e0e0;
    color: #000000;
    padding: 4px;
    border: 1px solid #ccc;
    font-weight: bold;
}
QTableCornerButton::section {
    background-color: #e0e0e0;
    border: 1px solid #ccc;
}
"""

DARK_STYLE = """
QMainWindow, QDialog {
    background-color: #2b2b2b;
    color: #ffffff;
    border-radius: 12px;
}
QPushButton {
    background-color: #4a90e2;
    color: #ffffff;
    border-radius: 10px;
    padding: 6px 12px;
}
QPushButton:hover {
    background-color: #357ABD;
}
QLineEdit, QTextEdit {
    background-color: #404040;
    color: #ffffff;
    border-radius: 8px;
    padding: 5px;
    border: none;
}
QLabel {
    color: #ffffff;
}
QListWidget {
    background-color: #3c3f41;
    color: #ffffff;
    border-radius: 8px;
}
QScrollBar:vertical {
    background: #404040;
    width: 12px;
    border-radius: 6px;
}
QTableWidget {
    background-color: #3c3f41;
    color: #ffffff;
    gridline-color: #555555;
    selection-background-color: #4a90e2;
    selection-color: #ffffff;
    border-radius: 6px;
}
QHeaderView::section {
    background-color: #2e2e2e;
    color: #ffffff;
    padding: 4px;
    border: 1px solid #444;
    font-weight: bold;
}
QTableCornerButton::section {
    background-color: #2e2e2e;
    border: 1px solid #444;
}
"""

def get_theme_style(theme: str) -> str:
    if theme.lower() == "light":
        return LIGHT_STYLE
    return DARK_STYLE


FLOATING_STYLE = """
#FloatingWidget {
    background-color: transparent;
    border: 2px solid #4a90e2;
    border-radius: 10px;
}
#FloatingWidget QLabel {
    font-weight: bold;
}
#FloatingWidget QPushButton {
    background-color: #4a90e2;
    color: white;
    border-radius: 6px;
    padding: 5px 10px;
}
#FloatingWidget QPushButton:hover {
    background-color: #357ABD;
}
"""


def get_theme_style(theme: str, is_floating=False) -> str:
    base = LIGHT_STYLE if theme == "light" else DARK_STYLE
    return base + FLOATING_STYLE if is_floating else base

