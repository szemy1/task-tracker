from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTextEdit, QPushButton, QLabel, QHBoxLayout,
    QFileDialog, QSplitter
)
from PySide6.QtCore import Qt
from PySide6.QtWebEngineWidgets import QWebEngineView
from markdown import markdown
import os
from datetime import datetime
from gui.style import get_theme_style
from PySide6.QtCore import QSettings
import markdown
import html.parser


class NoteEditorDialog(QDialog):
    def __init__(self, task):
        super().__init__()
        self.setWindowTitle("📝 Feladatjegyzet")
        self.setMinimumSize(800, 600)
        
        theme = QSettings().value("theme", "dark")
        self.setStyleSheet(get_theme_style(theme))

        self.setWindowFlags(Qt.Window)

        self.task = task
        self.layout_mode = "vertical"  # vagy "horizontal"

        # 🛠 Jegyzetfájl elérési út meghatározása
        safe_title = self.task.title.replace(":", "").replace(" ", "_").replace("/", "_")
        date_str = self.task.start_time.strftime("%Y-%m-%d") if self.task.start_time else "unknown"
        folder = os.path.join("notes", date_str)
        os.makedirs(folder, exist_ok=True)
        self.note_path = os.path.join(folder, f"{safe_title}.md")

        # Widgetek
        self.editor = QTextEdit()
        self.preview = QWebEngineView()

        # ✍️ Betöltés sablonból vagy meglévő jegyzetből
        self.load_template_or_existing_note()

        # Splitter létrehozása
        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.editor)
        self.splitter.addWidget(self.preview)

        # Gombok
        self.save_button = QPushButton("💾 Mentés")
        self.save_button.clicked.connect(self.save_note)

        self.export_button = QPushButton("📁 Mentés másként")
        self.export_button.clicked.connect(self.export_note)

        self.preview_button = QPushButton("🔄 Előnézet frissítése")
        self.preview_button.clicked.connect(self.update_preview)

        self.toggle_button = QPushButton("🔃 Nézet váltás")
        self.toggle_button.clicked.connect(self.toggle_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.preview_button)
        button_layout.addWidget(self.toggle_button)

        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(self.splitter)
        self.setLayout(layout)

        self.update_preview()

    def load_template_or_existing_note(self):
        if os.path.exists(self.note_path):
            with open(self.note_path, "r", encoding="utf-8") as f:
                self.editor.setPlainText(f.read())
        else:
            template_path = os.path.join("config", "note_template.md")

            # 🔧 Automatikus sablon létrehozás, ha nem létezik
            if not os.path.exists(template_path):
                with open(template_path, "w", encoding="utf-8") as f:
                    f.write("""# Jegyzet – {{title}}

**Leírás:**  
{{description}}

**Kezdés:** {{start_time}}  
**Befejezés:** {{end_time}}

---

## Teendők / Összegzés

- [ ] Rövid összefoglalás a feladatról
- [ ] Tanulságok
- [ ] Következő lépések

---

## Megjegyzések

<!-- Ide jöhet bármilyen további jegyzet -->
""")

            with open(template_path, "r", encoding="utf-8") as f:
                template = f.read()

            note_text = template \
                .replace("{{title}}", self.task.title) \
                .replace("{{description}}", self.task.description or "-") \
                .replace("{{start_time}}", str(self.task.start_time or "-")) \
                .replace("{{end_time}}", str(self.task.end_time or "-"))

            self.editor.setPlainText(note_text)

    def save_note(self):
        with open(self.note_path, "w", encoding="utf-8") as f:
            f.write(self.editor.toPlainText())
        print(f"[AUTO-MENTÉS] Jegyzet mentve ide: {self.note_path}")
        self.accept()

    def export_note(self):
        path, _ = QFileDialog.getSaveFileName(self, "Jegyzet mentése", self.note_path, "Markdown fájl (*.md)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
            print(f"[EXPORT] Jegyzet mentve ide: {path}")

    def update_preview(self):
        html = markdown.markdown(self.editor.toPlainText(), extensions=["tables", "fenced_code"])
        self.preview.setHtml(html)

    def toggle_layout(self):
    # Csak az orientációt állítjuk, nem törlünk és nem hozunk létre új QSplitter-t
        new_orientation = Qt.Horizontal if self.layout_mode == "vertical" else Qt.Vertical
        self.layout_mode = "horizontal" if self.layout_mode == "vertical" else "vertical"
        self.splitter.setOrientation(new_orientation)

