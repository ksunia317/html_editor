import sys
import json
from pathlib import Path

from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QFrame, QHBoxLayout, QPushButton, QLineEdit, \
    QListWidget, QTabWidget, QTextBrowser, QTextEdit, QSplitter, QFileDialog, QListWidgetItem
from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import HtmlFormatter
from res.themes.light.light_theme_strings import CustomHTMLStyleLight
from res.themes.dark.dark_theme_strings import CustomHTMLStyleDark
from ui.settings_window import SettingsWindow
from res.themes.light.light_theme import apply_light_theme
from res.themes.dark.dark_theme import apply_dark_theme


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.theme = "dark"
        self.current_dir = Path(__file__).parent
        self.notes_data = self.load_notes()
        self.current_note_id = None
        self.initUI()
        self.apply_theme()
        self.highlihting()
        self.load_notes_to_list()

    def initUI(self):
        self.showMaximized()
        self.setWindowTitle('Notes')
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.left_column = QFrame()
        self.left_column.setMinimumWidth(150)
        self.left_column.setMaximumWidth(400)
        self.top_layout = QHBoxLayout()
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.settings_button = QPushButton()
        self.settings_button.setFixedSize(36, 36)
        self.update_settings_icon()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск...")
        self.top_layout.addWidget(self.settings_button)
        self.top_layout.addWidget(self.search_input)
        self.notes_list = QListWidget()
        self.notes_list.itemClicked.connect(self.load_note_content)
        self.new_note_button = QPushButton("Новая заметка")
        self.new_note_button.clicked.connect(self.create_new_note)
        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(10, 10, 10, 10)
        self.left_layout.addLayout(self.top_layout)
        self.left_layout.addWidget(self.new_note_button)
        self.left_layout.addWidget(self.notes_list)
        self.left_column.setLayout(self.left_layout)
        self.center_widget = QWidget()
        self.center_widget.setMinimumWidth(300)
        self.center_layout = QVBoxLayout(self.center_widget)
        self.center_layout.setContentsMargins(10, 10, 10, 10)
        self.tabs = QTabWidget()
        self.tabs.setFixedHeight(50)
        self.note_input = QTextEdit()
        self.note_input.setPlaceholderText("Введите текст...")
        self.note_input.setMaximumHeight(400)
        self.note_input.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.text_browser = QTextBrowser()
        self.text_browser.setMaximumHeight(400)
        self.center_layout.addWidget(self.tabs)
        self.center_layout.addWidget(self.note_input)
        self.center_layout.addWidget(self.text_browser)
        self.right_column = QFrame()
        self.right_column.setMinimumWidth(150)
        self.right_column.setMaximumWidth(400)
        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(10, 10, 10, 10)
        self.column_title = QLineEdit()
        self.column_title.setPlaceholderText("Название записи")
        self.column_title.textChanged.connect(self.update_note_title)
        self.save_button = QPushButton("Сохранить")
        self.right_layout.addWidget(self.column_title)
        self.right_layout.addWidget(self.save_button)
        self.right_layout.addStretch()
        self.right_column.setLayout(self.right_layout)
        self.splitter.addWidget(self.left_column)
        self.splitter.addWidget(self.center_widget)
        self.splitter.addWidget(self.right_column)
        self.splitter.setSizes([200, 500, 200])
        self.main_layout.addWidget(self.splitter)
        self.note_input.textChanged.connect(self.highlihting)
        self.settings_button.clicked.connect(self.open_settings)
        self.note_input.textChanged.connect(self.format_text)
        self.note_input.textChanged.connect(self.update_current_note)
        self.save_button.clicked.connect(self.save_file)

    def load_notes(self):
        notes_file = self.current_dir / "notes.json"
        if notes_file.exists():
            try:
                with open(notes_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []

    def save_notes(self):
        notes_file = self.current_dir / "notes.json"
        with open(notes_file, 'w', encoding='utf-8') as f:
            json.dump(self.notes_data, f, ensure_ascii=False, indent=2)

    def create_new_note(self):
        note_id = len(self.notes_data)
        new_note = {
            "id": note_id,
            "title": f"Новая заметка {note_id + 1}",
            "content": ""
        }
        self.notes_data.append(new_note)
        self.save_notes()
        item = QListWidgetItem(new_note["title"])
        item.setData(Qt.ItemDataRole.UserRole, note_id)
        self.notes_list.addItem(item)
        self.notes_list.setCurrentItem(item)
        self.load_note_content(item)

    def load_notes_to_list(self):
        self.notes_list.clear()
        for note in self.notes_data:
            item = QListWidgetItem(note["title"])
            item.setData(Qt.ItemDataRole.UserRole, note["id"])
            self.notes_list.addItem(item)

    def load_note_content(self, item):
        note_id = item.data(Qt.ItemDataRole.UserRole)
        self.current_note_id = note_id
        for note in self.notes_data:
            if note["id"] == note_id:
                self.column_title.setText(note["title"])
                self.note_input.blockSignals(True)
                self.note_input.setPlainText(note["content"])
                self.note_input.blockSignals(False)
                self.format_text()
                break

    def update_note_title(self):
        """Обновить заголовок текущей заметки"""
        if self.current_note_id is not None:
            new_title = self.column_title.text()
            for note in self.notes_data:
                if note["id"] == self.current_note_id:
                    note["title"] = new_title
                    current_item = self.notes_list.currentItem()
                    if current_item:
                        current_item.setText(new_title)
                    self.save_notes()
                    break

    def update_current_note(self):
        if self.current_note_id is not None:
            for note in self.notes_data:
                if note["id"] == self.current_note_id:
                    note["content"] = self.note_input.toPlainText()
                    self.save_notes()
                    break

    def update_settings_icon(self):
        if self.theme == "light":
            icon_path = self.current_dir / "res" / "icons" / "light_settings_icon.png"
        else:
            icon_path = self.current_dir / "res" / "icons" / "dark_settings_icon.png"
        pixmap = QPixmap(str(icon_path))
        self.settings_button.setIcon(QIcon(pixmap))
        self.settings_button.setIconSize(QSize(36, 36))

    def open_settings(self):
        self.settings_window = SettingsWindow(self.theme, self)
        self.settings_window.show()

    def apply_theme(self):
        if self.theme == "light":
            apply_light_theme(QApplication.instance())
        else:
            apply_dark_theme(QApplication.instance())
        self.update_settings_icon()

    def highlihting(self):
        scrollbar = self.note_input.verticalScrollBar()
        scroll_pos = scrollbar.value()
        cursor = self.note_input.textCursor()
        cursor_pos = cursor.position()
        html_code = self.note_input.toPlainText()
        if not html_code.strip():
            return
        try:
            formatter = HtmlFormatter(
                style=CustomHTMLStyleLight if self.theme == "light" else CustomHTMLStyleDark,
                linenos=False,
                noclasses=True,
                nobackground=True,
                cssstyles='font-family: Consolas, "Courier New", monospace; font-size: 12px;'
            )
            highlighted_html = highlight(html_code, HtmlLexer(), formatter)
            self.note_input.blockSignals(True)
            self.note_input.setHtml(highlighted_html)
            self.note_input.blockSignals(False)
            scrollbar.setValue(scroll_pos)
            new_cursor = self.note_input.textCursor()
            new_cursor.setPosition(min(cursor_pos, len(html_code)))
            self.note_input.setTextCursor(new_cursor)
        except Exception:
            self.note_input.blockSignals(True)
            self.note_input.setPlainText(html_code)
            self.note_input.blockSignals(False)
            new_cursor = self.note_input.textCursor()
            new_cursor.setPosition(min(cursor_pos, len(html_code)))
            self.note_input.setTextCursor(new_cursor)

    def format_text(self):
        try:
            self.text_browser.setHtml(self.note_input.toPlainText())
        except Exception:
            print(self.note_input.toPlainText())

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить текст", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            text = self.text_browser.toPlainText()
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())