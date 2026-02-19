import os
import json
import tempfile
import webbrowser
import re
from datetime import datetime

from PyQt6.QtGui import QIcon, QPixmap, QKeySequence, QShortcut
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QFrame, QHBoxLayout, QPushButton, QLineEdit, \
    QListWidget, QTabWidget, QTextBrowser, QSplitter, QFileDialog, QListWidgetItem, QLabel, QComboBox, \
    QGroupBox, QMessageBox, QTextEdit
from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import HtmlFormatter
from code_editor import CodeEditor
from search_dialog import SearchDialog
from settings_window import SettingsWindow
from res.themes.light.light_theme import apply_light_theme
from res.themes.dark.dark_theme import apply_dark_theme
from res.themes.light.light_theme_strings import CustomHTMLStyleLight
from res.themes.dark.dark_theme_strings import CustomHTMLStyleDark
from res.themes.light.monokai_light import MonokaiLightStyle
from res.themes.light.solarized_light import SolarizedLightStyle
from res.themes.light.dracula_light import DraculaLightStyle
from res.themes.dark.monokai_dark import MonokaiDarkStyle
from res.themes.dark.solarized_dark import SolarizedDarkStyle
from res.themes.dark.dracula_dark import DraculaDarkStyle


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.theme = "dark"
        self.config_file = "data/config.json"
        self.config_data = self.load_config()
        self.theme = self.config_data.get("theme", "dark")
        self.notes_data = self.load_notes()
        self.filtered_notes = []
        self.current_note_id = None
        self.open_tabs = {}
        self.cur_file_path = None
        self.search_dialog = None
        self.auto_save_timer = None
        self.initUI()
        self.apply_theme()
        self.apply_editor_settings()
        self.highlight_code()
        self.load_notes_to_list()
        self.update_ui_state()
        self.setup_hot_keys()
        self.setup_auto_save()

    def initUI(self):
        self.showMaximized()
        self.setWindowTitle('HTML Editor')
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
        self.search_input.setPlaceholderText("Поиск файлов...")
        self.search_input.textChanged.connect(self.search_notes)
        self.top_layout.addWidget(self.settings_button)
        self.top_layout.addWidget(self.search_input)
        self.notes_list = QListWidget()
        self.notes_list.itemClicked.connect(self.load_note_content)
        self.new_note_button = QPushButton("Новый файл")
        self.new_note_button.clicked.connect(self.create_new_note)
        self.import_button = QPushButton("Импорт проекта")
        self.import_button.clicked.connect(self.import_project)
        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(10, 10, 10, 10)
        self.left_layout.addLayout(self.top_layout)
        self.left_layout.addWidget(self.new_note_button)
        self.left_layout.addWidget(self.import_button)
        self.left_layout.addWidget(self.notes_list)
        self.left_column.setLayout(self.left_layout)
        self.center_widget = QWidget()
        self.center_widget.setMinimumWidth(300)
        self.center_layout = QVBoxLayout(self.center_widget)
        self.center_layout.setContentsMargins(10, 10, 10, 10)
        self.tabs = QTabWidget()
        self.tabs.setFixedHeight(50)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.setTabsClosable(True)
        self.note_input = CodeEditor(self)
        self.note_input.setPlaceholderText("Введите HTML код...")
        self.note_input.setMaximumHeight(400)
        self.text_browser = QTextBrowser()
        self.text_browser.setMaximumHeight(400)
        self.center_layout.addWidget(self.tabs)
        self.center_layout.addWidget(self.note_input)
        self.center_layout.addWidget(self.text_browser)
        self.right_column = QFrame()
        self.right_column.setMinimumWidth(250)
        self.right_column.setMaximumWidth(400)
        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(10, 10, 10, 10)
        self.file_info_group = QGroupBox("Информация о файле")
        file_info_layout = QVBoxLayout()
        self.column_title = QLineEdit()
        self.column_title.setPlaceholderText("Название файла")
        self.column_title.textChanged.connect(self.update_title)
        file_info_layout.addWidget(QLabel("Название:"))
        file_info_layout.addWidget(self.column_title)
        self.created_date_label = QLabel("Создан: -")
        file_info_layout.addWidget(self.created_date_label)
        self.modified_date_label = QLabel("Изменен: -")
        file_info_layout.addWidget(self.modified_date_label)
        self.file_size_label = QLabel("Размер: 0 байт")
        file_info_layout.addWidget(self.file_size_label)
        self.line_count_label = QLabel("Строк: 0")
        file_info_layout.addWidget(self.line_count_label)
        self.file_info_group.setLayout(file_info_layout)
        self.right_layout.addWidget(self.file_info_group)
        self.html_group = QGroupBox("Параметры HTML")
        html_layout = QVBoxLayout()
        html_layout.addWidget(QLabel("Версия HTML:"))
        self.html_version = QComboBox()
        self.html_version.addItems(["HTML5", "HTML 4.01", "XHTML 1.0"])
        self.html_version.setCurrentText(self.config_data["html"]["default_version"])
        self.html_version.currentTextChanged.connect(self.update_html_template)
        html_layout.addWidget(self.html_version)
        html_layout.addWidget(QLabel("Кодировка:"))
        self.encoding = QComboBox()
        self.encoding.addItems(["UTF-8", "windows-1251", "KOI8-R"])
        self.encoding.setCurrentText(self.config_data["html"]["default_encoding"])
        self.encoding.currentTextChanged.connect(self.update_encoding)
        html_layout.addWidget(self.encoding)
        self.html_group.setLayout(html_layout)
        self.right_layout.addWidget(self.html_group)
        self.preview_group = QGroupBox("Превью")
        preview_layout = QVBoxLayout()
        self.open_in_browser_btn = QPushButton("Открыть в браузере")
        self.open_in_browser_btn.clicked.connect(self.open_in_browser)
        preview_layout.addWidget(self.open_in_browser_btn)
        self.preview_group.setLayout(preview_layout)
        self.right_layout.addWidget(self.preview_group)
        self.export_group = QGroupBox("Действия с файлом")
        export_layout = QVBoxLayout()
        self.save_button = QPushButton("Сохранить как...")
        self.save_button.clicked.connect(self.save_file)
        export_layout.addWidget(self.save_button)
        self.delete_button = QPushButton("Удалить файл")
        self.delete_button.clicked.connect(self.delete_current_note)
        export_layout.addWidget(self.delete_button)
        self.export_group.setLayout(export_layout)
        self.right_layout.addWidget(self.export_group)
        self.right_layout.addStretch()
        self.right_column.setLayout(self.right_layout)
        self.splitter.addWidget(self.left_column)
        self.splitter.addWidget(self.center_widget)
        self.splitter.addWidget(self.right_column)
        self.splitter.setSizes([200, 500, 250])
        self.main_layout.addWidget(self.splitter)
        self.note_input.textChanged.connect(self.on_text_changed)
        self.settings_button.clicked.connect(self.open_settings)
        self.tabs.currentChanged.connect(self.tab_changed)
        self.info_label = QLabel("Откройте или создайте файл")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.info_label.font()
        font.setPointSize(14)
        self.info_label.setFont(font)
        self.center_layout.insertWidget(0, self.info_label)
        self.info_label.hide()

    def load_config(self):
        with open(self.config_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config_data, f, ensure_ascii=False, indent=2)

    def apply_editor_settings(self):
        if hasattr(self, 'note_input'):
            font = self.note_input.font()
            font.setPointSize(self.config_data["editor"]["font_size"])
            font.setFamily('Consolas, "Courier New", monospace')
            self.note_input.setFont(font)
            self.note_input.setTabStopDistance(self.config_data["editor"]["tab_size"] * 10)
            self.note_input.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
            self.note_input.update_line_number()
            if hasattr(self, 'text_browser'):
                pass
            if self.current_note_id is not None:
                self.highlight_code()

    def setup_auto_save(self):
        if self.auto_save_timer:
            self.auto_save_timer.stop()
        if self.config_data["editor"]["auto_save"]:
            self.auto_save_timer = QTimer()
            self.auto_save_timer.timeout.connect(self.auto_save)
            interval = self.config_data["editor"]["auto_save_interval"] * 60 * 1000
            self.auto_save_timer.start(interval)

    def auto_save(self):
        if self.current_note_id is not None:
            for note in self.notes_data:
                if note["id"] == self.current_note_id:
                    note["content"] = self.note_input.toPlainText()
                    note["modified"] = datetime.now().isoformat()
                    self.save_notes()
                    if self.cur_file_path:
                        with open(self.cur_file_path, 'w', encoding='utf-8') as file:
                            file.write(note["content"])
                    if self.config_data["backup"]["enabled"]:
                        self.create_backup(note)
                    return

    def create_backup(self, note):
        backup_dir = self.config_data["backup"]["location"]
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = re.sub(r'[^\w\-_\. ]', '_', note["title"])
        backup_file = os.path.join(backup_dir, f"{safe_title}_{timestamp}.html")
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(note["content"])
        self.cleanup_old_backups(safe_title)

    def cleanup_old_backups(self, title):
        backup_dir = self.config_data["backup"]["location"]
        max_backups = 5
        backups = []
        for file in os.listdir(backup_dir):
            if file.startswith(f"{title}_") and file.endswith(".html"):
                file_path = os.path.join(backup_dir, file)
                backups.append((os.path.getmtime(file_path), file_path))
        backups.sort()
        while len(backups) > max_backups:
            os.remove(backups.pop(0)[1])

    def setup_hot_keys(self):
        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.save_shortcut.activated.connect(self.save_cntrls)
        self.undo_shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.undo_shortcut.activated.connect(self.undo_action)
        self.find_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        self.find_shortcut.activated.connect(self.show_search_dialog)
        self.new_tab_shortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        self.new_tab_shortcut.activated.connect(self.create_new_note)
        self.close_tab_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        self.close_tab_shortcut.activated.connect(self.close_cur_tab)
        self.format_shortcut = QShortcut(QKeySequence("Ctrl+Alt+L"), self)
        self.format_shortcut.activated.connect(self.auto_format_code)
        self.delete_shortcut = QShortcut(QKeySequence("Delete"), self)
        self.delete_shortcut.activated.connect(self.delete_current_note)

    def delete_current_note(self):
        if self.current_note_id is None:
            QMessageBox.information(self, "Удаление", "Нет открытого файла для удаления")
            return
        note_title = ""
        for note in self.notes_data:
            if note["id"] == self.current_note_id:
                note_title = note["title"]
                break
        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить файл '{note_title}'?\nЭто действие нельзя отменить.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.notes_data = [note for note in self.notes_data if note["id"] != self.current_note_id]
            tabs_to_close = []
            for tab_index, note_id in self.open_tabs.items():
                if note_id == self.current_note_id:
                    tabs_to_close.append(tab_index)
            for tab_index in sorted(tabs_to_close, reverse=True):
                self.close_tab(tab_index)
            self.save_notes()
            self.load_notes_to_list()
            if self.search_input.text():
                self.search_notes()

    def show_search_dialog(self):
        if self.current_note_id is None:
            QMessageBox.information(self, "Поиск", "Откройте документ для поиска")
            return
        if not self.search_dialog:
            self.search_dialog = SearchDialog(self)
        self.search_dialog.show()
        self.search_dialog.raise_()
        self.search_dialog.search_input.setFocus()
        self.search_dialog.search_input.selectAll()

    def save_cntrls(self):
        if self.current_note_id is None:
            return
        if self.cur_file_path is None:
            self.save_file()
        else:
            text = self.note_input.toPlainText()
            with open(self.cur_file_path, 'w', encoding='utf-8') as file:
                file.write(text)
            for note in self.notes_data:
                if note["id"] == self.current_note_id:
                    note["modified"] = datetime.now().isoformat()
                    self.save_notes()
                    self.update_dates()
                    break
            if self.config_data["backup"]["enabled"]:
                for note in self.notes_data:
                    if note["id"] == self.current_note_id:
                        self.create_backup(note)
                        return

    def undo_action(self):
        if self.current_note_id is not None:
            self.note_input.undo()

    def close_cur_tab(self):
        current_index = self.tabs.currentIndex()
        if current_index >= 0:
            self.close_tab(current_index)

    def auto_format_code(self):
        if self.current_note_id is None:
            return
        if not self.config_data["html"]["auto_format"]:
            reply = QMessageBox.question(self, "Автоформатирование",
                                         "Автоформатирование отключено в настройках. Включить сейчас?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.config_data["html"]["auto_format"] = True
                self.save_config()
            else:
                return
        html_code = self.note_input.toPlainText()
        if not html_code.strip():
            return
        formatted_code = self.format_html(html_code)
        cursor = self.note_input.textCursor()
        cursor_pos = cursor.position()
        self.note_input.blockSignals(True)
        self.note_input.setPlainText(formatted_code)
        self.note_input.blockSignals(False)
        new_cursor = self.note_input.textCursor()
        new_cursor.setPosition(min(cursor_pos, len(formatted_code)))
        self.note_input.setTextCursor(new_cursor)
        self.highlight_code()
        self.format_text()
        self.update_current_note()

    def format_html(self, html_code):
        lines = [line.rstrip() for line in html_code.split('\n')]
        format_lines = []
        level = 0
        size = self.config_data["editor"]["tab_size"]
        tag = re.compile(r'<(/?)([\w-]+)([^>]*)>')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                if format_lines and format_lines[-1] != '':
                    format_lines.append('')
                i += 1
                continue
            if line.startswith('<!--'):
                format_lines.append(' ' * (level * size) + line)
                i += 1
                continue
            tags = list(tag.finditer(line))
            if not tags:
                format_lines.append(' ' * (level * size) + line)
                i += 1
                continue
            if len(tags) == 1:
                tag_match = tags[0]
                is_closing = tag_match.group(1) == '/'
                tag_name = tag_match.group(2).lower()
                void_tags = ['area', 'base', 'br', 'col', 'embed', 'hr', 'img',
                             'input', 'link', 'meta', 'param', 'source', 'track', 'wbr']
                closings = tag_name in void_tags or '/>' in tag_match.group(3)
                if is_closing:
                    level = max(0, level - 1)
                    format_lines.append(' ' * (level * size) + line)
                elif closings:
                    format_lines.append(' ' * (level * size) + line)
                else:
                    format_lines.append(' ' * (level * size) + line)
                    level += 1
            else:
                last_pos = 0
                for tag_match in tags:
                    tag_start = tag_match.start()
                    tag_end = tag_match.end()
                    if tag_start > last_pos:
                        text = line[last_pos:tag_start].strip()
                        if text:
                            format_lines.append(' ' * (level * size) + text)
                    tag_text = line[tag_start:tag_end]
                    is_closing = tag_match.group(1) == '/'
                    tag_name = tag_match.group(2).lower()
                    void_tags = ['area', 'base', 'br', 'col', 'embed', 'hr', 'img',
                                 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr']
                    closings = tag_name in void_tags or '/>' in tag_match.group(3)
                    if is_closing:
                        level = max(0, level - 1)
                        format_lines.append(' ' * (level * size) + tag_text)
                    elif closings:
                        format_lines.append(' ' * (level * size) + tag_text)
                    else:
                        format_lines.append(' ' * (level * size) + tag_text)
                        level += 1
                    last_pos = tag_end
                if last_pos < len(line):
                    text = line[last_pos:].strip()
                    if text:
                        format_lines.append(' ' * (level * size) + text)
            i += 1
        result = []
        prev_empty = False
        for line in format_lines:
            if line == '':
                if not prev_empty:
                    result.append(line)
                    prev_empty = True
            else:
                result.append(line)
                prev_empty = False
        return '\n'.join(result)

    def save_file(self):
        if self.current_note_id is None:
            return
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить текст", "",
                                                   "HTML Files (*.html);;Text Files (*.txt);;All Files (*)")
        if file_name:
            text = self.note_input.toPlainText()
            with open(file_name, 'w', encoding="UTF-8") as file:
                file.write(text)
            self.cur_file_path = file_name
            for note in self.notes_data:
                if note["id"] == self.current_note_id:
                    note["modified"] = datetime.now().isoformat()
                    self.save_notes()
                    self.update_dates()
                    break
            if self.config_data["backup"]["enabled"]:
                for note in self.notes_data:
                    if note["id"] == self.current_note_id:
                        self.create_backup(note)
                        return

    def load_note_content(self, item):
        note_id = item.data(Qt.ItemDataRole.UserRole)
        for tab_index, open_note_id in self.open_tabs.items():
            if open_note_id == note_id:
                self.tabs.setCurrentIndex(tab_index)
                self.update_ui_state()
                return
        for note in self.notes_data:
            if note["id"] == note_id:
                if "created" not in note:
                    note["created"] = datetime.now().isoformat()
                if "modified" not in note:
                    note["modified"] = datetime.now().isoformat()
                if "html_version" not in note:
                    note["html_version"] = self.config_data["html"]["default_version"]
                if "encoding" not in note:
                    note["encoding"] = self.config_data["html"]["default_encoding"]
                tab_index = self.tabs.addTab(QWidget(), note["title"])
                self.open_tabs[tab_index] = note_id
                self.tabs.setCurrentIndex(tab_index)
                self.current_note_id = note_id
                self.cur_file_path = None
                self.column_title.blockSignals(True)
                self.column_title.setText(note["title"])
                self.column_title.blockSignals(False)
                self.html_version.setCurrentText(note.get("html_version", self.config_data["html"]["default_version"]))
                self.encoding.setCurrentText(note.get("encoding", self.config_data["html"]["default_encoding"]))
                self.note_input.blockSignals(True)
                self.note_input.setPlainText(note["content"])
                self.note_input.blockSignals(False)
                if self.config_data["html"]["auto_format"] and note["content"].strip():
                    self.auto_format_code()
                else:
                    self.highlight_code()
                    self.format_text()
                self.update_file_stats()
                self.update_dates()
                self.update_ui_state()
                return

    def create_new_note(self):
        note_id = len(self.notes_data)
        now = datetime.now().isoformat()
        new_note = {
            "id": note_id,
            "title": f"Новый файл {note_id + 1}",
            "content": "",
            "created": now,
            "modified": now,
            "html_version": self.config_data["html"]["default_version"],
            "encoding": self.config_data["html"]["default_encoding"]
        }
        self.notes_data.append(new_note)
        self.save_notes()
        self.load_notes_to_list()
        self.search_input.clear()
        for i in range(self.notes_list.count()):
            item = self.notes_list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == note_id:
                self.notes_list.setCurrentItem(item)
                self.load_note_content(item)
                return

    def close_tab(self, index):
        if index in self.open_tabs:
            if self.search_dialog:
                self.search_dialog.close()
                self.search_dialog = None
            del self.open_tabs[index]
            self.tabs.removeTab(index)
            new_open_tabs = {}
            for i in range(self.tabs.count()):
                if i < index:
                    new_open_tabs[i] = self.open_tabs[i]
                else:
                    new_open_tabs[i] = self.open_tabs[i + 1]
            self.open_tabs = new_open_tabs
            if self.tabs.count() > 0:
                self.tabs.setCurrentIndex(self.tabs.count() - 1)
            else:
                self.current_note_id = None
                self.cur_file_path = None
                self.column_title.clear()
                self.note_input.clear()
                self.text_browser.clear()
                self.update_file_stats()
                self.clear_dates()
                self.update_ui_state()

    def on_text_changed(self):
        if self.current_note_id is not None:
            self.highlight_code()
            self.format_text()
            self.update_current_note()
            self.update_file_stats()

    def update_ui_state(self):
        has_open_files = self.current_note_id is not None
        self.tabs.setVisible(has_open_files)
        self.note_input.setVisible(has_open_files)
        self.text_browser.setVisible(has_open_files)
        self.right_column.setVisible(has_open_files)
        self.info_label.setVisible(not has_open_files)
        if hasattr(self, 'delete_button'):
            self.delete_button.setEnabled(has_open_files)

    def import_project(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Импорт проекта", "",
                                                   "Текстовые файлы (*.txt);;HTML файлы (*.html *.htm);;Все файлы (*)")
        if file_path:
            is_html = file_path.lower().endswith(('.html', '.htm'))
            content = None
            for encoding in ['utf-8', 'windows-1251', 'cp1251', 'koi8-r']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except Exception:
                    continue
            if content is None:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            note_id = len(self.notes_data)
            now = datetime.now().isoformat()
            file_name = os.path.basename(file_path)
            title = os.path.splitext(file_name)[0]
            new_note = {
                "id": note_id,
                "title": title,
                "content": content,
                "created": now,
                "modified": now,
                "html_version": self.config_data["html"]["default_version"],
                "encoding": self.config_data["html"]["default_encoding"],
                "is_html": is_html
            }
            self.notes_data.append(new_note)
            self.save_notes()
            self.load_notes_to_list()
            self.search_input.clear()
            for i in range(self.notes_list.count()):
                item = self.notes_list.item(i)
                if item.data(Qt.ItemDataRole.UserRole) == note_id:
                    self.notes_list.setCurrentItem(item)
                    self.load_note_content(item)
                    return

    def tab_changed(self, index):
        if index >= 0 and index in self.open_tabs:
            note_id = self.open_tabs[index]
            self.current_note_id = note_id
            self.cur_file_path = None
            for note in self.notes_data:
                if note["id"] == note_id:
                    self.column_title.blockSignals(True)
                    self.column_title.setText(note["title"])
                    self.column_title.blockSignals(False)
                    self.html_version.blockSignals(True)
                    self.encoding.blockSignals(True)
                    self.html_version.setCurrentText(
                        note.get("html_version", self.config_data["html"]["default_version"]))
                    self.encoding.setCurrentText(note.get("encoding", self.config_data["html"]["default_encoding"]))
                    self.html_version.blockSignals(False)
                    self.encoding.blockSignals(False)
                    self.note_input.blockSignals(True)
                    self.note_input.setPlainText(note["content"])
                    self.note_input.blockSignals(False)
                    self.highlight_code()
                    self.format_text()
                    self.update_file_stats()
                    self.update_dates()
                    self.update_ui_state()
                    return

    def update_title(self, new_title):
        if self.current_note_id is not None:
            for note in self.notes_data:
                if note["id"] == self.current_note_id:
                    note["title"] = new_title
                    note["modified"] = datetime.now().isoformat()
                    for i in range(self.notes_list.count()):
                        item = self.notes_list.item(i)
                        if item.data(Qt.ItemDataRole.UserRole) == self.current_note_id:
                            item.setText(new_title)
                            break
                    for tab_index, note_id in self.open_tabs.items():
                        if note_id == self.current_note_id:
                            self.tabs.setTabText(tab_index, new_title)
                            break
                    self.save_notes()
                    if self.search_input.text():
                        self.search_notes()
                    self.update_dates()
                    return

    def update_current_note(self):
        if self.current_note_id is not None:
            for note in self.notes_data:
                if note["id"] == self.current_note_id:
                    note["content"] = self.note_input.toPlainText()
                    note["modified"] = datetime.now().isoformat()
                    self.save_notes()
                    if self.search_input.text():
                        self.search_notes()
                    self.update_dates()
                    return

    def update_file_stats(self):
        if self.current_note_id is None:
            return
        text = self.note_input.toPlainText()
        size_bytes = len(text.encode('utf-8'))
        if size_bytes < 1024:
            size_str = f"{size_bytes} байт"
        elif size_bytes < 1024 * 1024:
            size_str = f"{size_bytes / 1024:.1f} КБ"
        else:
            size_str = f"{size_bytes / (1024 * 1024):.1f} МБ"
        self.file_size_label.setText(f"Размер: {size_str}")
        lines = text.count('\n') + 1 if text else 0
        self.line_count_label.setText(f"Строк: {lines}")

    def update_dates(self):
        if self.current_note_id is not None:
            for note in self.notes_data:
                if note["id"] == self.current_note_id:
                    created = note.get("created", "")
                    modified = note.get("modified", "")
                    if created:
                        try:
                            created_dt = datetime.fromisoformat(created)
                            self.created_date_label.setText(f"Создан: {created_dt.strftime('%d.%m.%Y %H:%M')}")
                        except Exception:
                            self.created_date_label.setText("Создан: -")
                    if modified:
                        try:
                            modified_dt = datetime.fromisoformat(modified)
                            self.modified_date_label.setText(f"Изменен: {modified_dt.strftime('%d.%m.%Y %H:%M')}")
                        except Exception:
                            self.modified_date_label.setText("Изменен: -")
                    return

    def clear_dates(self):
        self.created_date_label.setText("Создан: -")
        self.modified_date_label.setText("Изменен: -")

    def update_html_template(self, version):
        if self.current_note_id is not None:
            for note in self.notes_data:
                if note["id"] == self.current_note_id:
                    note["html_version"] = version
                    self.save_notes()
                    return

    def update_encoding(self, encoding):
        if self.current_note_id is not None:
            for note in self.notes_data:
                if note["id"] == self.current_note_id:
                    note["encoding"] = encoding
                    self.save_notes()
                    return

    def open_in_browser(self):
        if self.current_note_id is None:
            return
        for note in self.notes_data:
            if note["id"] == self.current_note_id:
                break
        html_content = self.note_input.toPlainText()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html_content)
            temp_file = f.name
        webbrowser.open('file://' + temp_file)

    def load_notes(self):
        notes_file = "data/codes.json"
        if not os.path.exists(notes_file) or os.path.getsize(notes_file) == 0:
            return []
        try:
            with open(notes_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except Exception:
            return []

    def save_notes(self):
        with open("data/codes.json", 'w', encoding='utf-8') as f:
            json.dump(self.notes_data, f, ensure_ascii=False, indent=2)

    def load_notes_to_list(self):
        self.notes_list.clear()
        notes_to_show = self.filtered_notes if self.filtered_notes else self.notes_data
        for note in notes_to_show:
            item = QListWidgetItem(note["title"])
            item.setData(Qt.ItemDataRole.UserRole, note["id"])
            self.notes_list.addItem(item)

    def search_notes(self):
        search_text = self.search_input.text().lower()
        if not search_text:
            self.filtered_notes = []
        else:
            self.filtered_notes = [
                note for note in self.notes_data
                if search_text in note["title"].lower() or search_text in note["content"].lower()]
        self.load_notes_to_list()

    def update_settings_icon(self):
        if self.theme == "light":
            icon_path = "res/icons/light_settings_icon.png"
        else:
            icon_path = "res/icons/dark_settings_icon.png"
        if os.path.exists(icon_path):
            pixmap = QPixmap(str(icon_path))
            self.settings_button.setIcon(QIcon(pixmap))
            self.settings_button.setIconSize(QSize(24, 24))

    def open_settings(self):
        self.settings_window = SettingsWindow(self.theme, self)
        self.settings_window.show()

    def apply_theme(self):
        if self.theme == "light":
            apply_light_theme(QApplication.instance())
        else:
            apply_dark_theme(QApplication.instance())
        self.update_settings_icon()
        if hasattr(self, 'note_input'):
            self.note_input.update_line_number()
            self.note_input.line_number_area.update()

    def highlight_code(self):
        if self.current_note_id is None:
            return
        if hasattr(self.note_input, 'is_highlighting') and self.note_input.is_highlighting:
            return
        self.note_input.is_highlighting = True
        scrollbar = self.note_input.verticalScrollBar()
        scroll_pos = scrollbar.value()
        cursor = self.note_input.textCursor()
        cursor_pos = cursor.position()
        html_code = self.note_input.toPlainText()
        if not html_code.strip():
            self.note_input.is_highlighting = False
            return
        highlight_theme = self.config_data.get("highlight_theme", "default")
        if self.theme == "light":
            if highlight_theme == "monokai":
                style = MonokaiLightStyle
            elif highlight_theme == "solarized":
                style = SolarizedLightStyle
            elif highlight_theme == "dracula":
                style = DraculaLightStyle
            else:
                style = CustomHTMLStyleLight
        else:
            if highlight_theme == "monokai":
                style = MonokaiDarkStyle
            elif highlight_theme == "solarized":
                style = SolarizedDarkStyle
            elif highlight_theme == "dracula":
                style = DraculaDarkStyle
            else:
                style = CustomHTMLStyleDark
        font_size = self.config_data["editor"]["font_size"]
        formatter = HtmlFormatter(
            style=style,
            linenos=False,
            noclasses=True,
            nobackground=True,
            cssstyles=f'font-family: Consolas, "Courier New", monospace; font-size: {font_size}px;'
        )
        highlighted_html = highlight(html_code, HtmlLexer(), formatter)
        self.note_input.blockSignals(True)
        self.note_input.setHtml(highlighted_html)
        self.note_input.blockSignals(False)
        font = self.note_input.font()
        font.setPointSize(font_size)
        font.setFamily('Consolas, "Courier New", monospace')
        self.note_input.setFont(font)
        self.note_input.setTabStopDistance(self.config_data["editor"]["tab_size"] * 10)
        self.note_input.update_line_number()
        scrollbar.setValue(scroll_pos)
        new_cursor = self.note_input.textCursor()
        new_cursor.setPosition(min(cursor_pos, len(html_code)))
        self.note_input.setTextCursor(new_cursor)
        self.note_input.is_highlighting = False

    def format_text(self):
        if self.current_note_id is not None:
            text = self.note_input.toPlainText()
            self.text_browser.setHtml(text)

    def apply_all_settings_from_settings(self):
        self.config_data = self.load_config()
        self.theme = self.config_data.get("theme", "dark")
        self.apply_theme()
        self.apply_editor_settings()
        self.setup_auto_save()
        self.highlight_code()
        if self.current_note_id:
            self.format_text()