from PySide6.QtWidgets import QPushButton, QDialog, QApplication, QMessageBox, QTextEdit, QLineEdit
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt


def find_button_by_text(window, text):
    return next((btn for btn in window.findChildren(QPushButton) if btn.text() == text), None)


def find_dialog():
    for widget in QApplication.allWidgets():
        if isinstance(widget, QDialog) and widget.isVisible():
            return widget
    return None

def fill_task_dialog(dialog, title, description):
    """Kitölti a feladat létrehozó dialógust (már biztosan betöltött állapotban)."""
    QTest.qWait(500)  # hosszabb wait, hogy a layout/render is biztosan megtörténjen

    title_input = dialog.findChild(QLineEdit)
    desc_input = dialog.findChild(QTextEdit)

    assert title_input is not None, "Név mező nem található"
    assert desc_input is not None, "Leírás mező nem található"

    # Biztonság kedvéért fókusz beállítás
    title_input.setFocus()
    QTest.qWait(50)
    title_input.setText(title)

    desc_input.setFocus()
    QTest.qWait(50)
    desc_input.setPlainText(description)

    QTest.qWait(200)

    # Ellenőrzés
    assert title_input.text() == title, f"Név mező nem frissült: '{title_input.text()}'"
    assert desc_input.toPlainText() == description, f"Leírás mező nem frissült: '{desc_input.toPlainText()}'"

def accept_messagebox_yes():
    for widget in QApplication.topLevelWidgets():
        if isinstance(widget, QMessageBox):
            yes_button = widget.button(QMessageBox.Yes)
            if yes_button:
                QTest.mouseClick(yes_button, Qt.LeftButton)
                break

def wait_for_dialog(qtbot, timeout=2000):
    """Megvárja, hogy megjelenjen egy aktív QDialog, majd visszaadja."""
    qtbot.waitUntil(lambda: any(
        isinstance(w, QDialog) and w.isVisible()
        for w in QApplication.allWidgets()
    ), timeout=timeout)

    return next(
        (w for w in QApplication.allWidgets() if isinstance(w, QDialog) and w.isVisible()),
        None
    )

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt
import time

def accept_messagebox_ok(timeout=2000):
    from PySide6.QtWidgets import QApplication, QMessageBox
    from PySide6.QtTest import QTest
    from PySide6.QtCore import Qt
    import time

    start_time = time.time()
    while time.time() - start_time < timeout / 1000:
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, QMessageBox):
                ok_button = widget.button(QMessageBox.Ok)
                if ok_button and ok_button.isVisible():
                    QTest.qWait(100)
                    QTest.mouseClick(ok_button, Qt.LeftButton)
                    return
        QTest.qWait(100)

