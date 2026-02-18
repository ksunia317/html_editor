import json

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QFrame, QVBoxLayout, QListWidget, QStackedWidget

from settings_pages.about_page import AboutPage
from settings_pages.backup_page import BackupPage
from settings_pages.docs_page import DocsPage
from settings_pages.html_page import HtmlPage
from settings_pages.editor_page import EditorPage
from settings_pages.appearance_page import AppearancePage


class SettingsWindow(QWidget):
    def __init__(self, theme="light", parent=None):
        super().__init__(parent, Qt.WindowType.Window)
        self.main_window = parent
        self.theme = theme
        self.config_file = "data/config.json"
        self.config_data = self.load_config()
        self.initUI()
        self.apply_timer = QTimer()
        self.apply_timer.setSingleShot(True)
        self.apply_timer.setInterval(500)
        self.apply_timer.timeout.connect(self.apply_all_settings)

    def initUI(self):
        self.resize(800, 600)
        self.setWindowTitle('Settings')
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.left_column = QFrame()
        self.left_column.setFixedWidth(200)
        self.settings_list = QListWidget()
        self.settings_list.addItems(
            ["Внешний вид", "Редактор", "HTML", "Резервное копирование", "Документация", "О программе"])
        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(10, 10, 10, 10)
        self.left_layout.addWidget(self.settings_list)
        self.left_column.setLayout(self.left_layout)
        self.right_column = QFrame()
        self.settings_stack = QStackedWidget()
        self.appearance_page = AppearancePage(self)
        self.editor_page = EditorPage(self)
        self.html_page = HtmlPage(self)
        self.backup_page = BackupPage(self)
        self.docs_page = DocsPage(self)
        self.about_page = AboutPage(self)
        self.settings_stack.addWidget(self.appearance_page)
        self.settings_stack.addWidget(self.editor_page)
        self.settings_stack.addWidget(self.html_page)
        self.settings_stack.addWidget(self.backup_page)
        self.settings_stack.addWidget(self.docs_page)
        self.settings_stack.addWidget(self.about_page)
        self.settings_list.currentRowChanged.connect(self.settings_stack.setCurrentIndex)
        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(10, 10, 10, 10)
        self.right_layout.addWidget(self.settings_stack)
        self.right_column.setLayout(self.right_layout)
        self.main_layout.addWidget(self.left_column)
        self.main_layout.addWidget(self.right_column)

    def load_config(self):
        with open(self.config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            if "highlight_theme" not in config:
                config["highlight_theme"] = "default"
            return config

    def save_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config_data, f, ensure_ascii=False, indent=2)

    def schedule_apply(self):
        self.apply_timer.start()

    def apply_all_settings(self):
        if not self.main_window or not self.main_window.isVisible():
            self.config_data["theme"] = "light" if self.appearance_page.theme_combo.currentIndex() == 0 else "dark"
            highlight_index = self.appearance_page.highlight_theme_combo.currentIndex()
            highlight_map = {0: "default", 1: "monokai", 2: "solarized", 3: "dracula"}
            self.config_data["highlight_theme"] = highlight_map.get(highlight_index, "default")
            self.config_data["editor"]["font_size"] = self.editor_page.font_size_spin.value()
            self.config_data["editor"]["tab_size"] = self.editor_page.tab_size_spin.value()
            self.config_data["editor"]["show_line_numbers"] = self.editor_page.show_lines_check.isChecked()
            self.config_data["editor"]["auto_save"] = self.editor_page.autosave_check.isChecked()
            self.config_data["editor"]["auto_save_interval"] = self.editor_page.autosave_interval_spin.value()
            self.config_data["html"]["default_version"] = self.html_page.html_version_combo.currentText()
            self.config_data["html"]["default_encoding"] = self.html_page.html_encoding_combo.currentText()
            self.config_data["html"]["auto_format"] = self.html_page.auto_format_check.isChecked()
            self.config_data["backup"]["enabled"] = self.backup_page.backup_check.isChecked()
            self.config_data["backup"]["interval"] = self.backup_page.backup_interval_spin.value()
            self.config_data["backup"]["location"] = self.backup_page.backup_location_edit.text()
            self.save_config()
            return
        self.config_data["theme"] = "light" if self.appearance_page.theme_combo.currentIndex() == 0 else "dark"
        highlight_index = self.appearance_page.highlight_theme_combo.currentIndex()
        highlight_map = {0: "default", 1: "monokai", 2: "solarized", 3: "dracula"}
        self.config_data["highlight_theme"] = highlight_map.get(highlight_index, "default")
        self.config_data["editor"]["font_size"] = self.editor_page.font_size_spin.value()
        self.config_data["editor"]["tab_size"] = self.editor_page.tab_size_spin.value()
        self.config_data["editor"]["show_line_numbers"] = self.editor_page.show_lines_check.isChecked()
        self.config_data["editor"]["auto_save"] = self.editor_page.autosave_check.isChecked()
        self.config_data["editor"]["auto_save_interval"] = self.editor_page.autosave_interval_spin.value()
        self.config_data["html"]["default_version"] = self.html_page.html_version_combo.currentText()
        self.config_data["html"]["default_encoding"] = self.html_page.html_encoding_combo.currentText()
        self.config_data["html"]["auto_format"] = self.html_page.auto_format_check.isChecked()
        self.config_data["backup"]["enabled"] = self.backup_page.backup_check.isChecked()
        self.config_data["backup"]["interval"] = self.backup_page.backup_interval_spin.value()
        self.config_data["backup"]["location"] = self.backup_page.backup_location_edit.text()
        self.save_config()
        if self.main_window:
            try:
                self.main_window.theme = self.config_data["theme"]
                self.main_window.config_data = self.config_data
                self.main_window.apply_theme()
                self.main_window.apply_editor_settings()
                if hasattr(self.main_window, 'setup_auto_save'):
                    self.main_window.setup_auto_save()
                if hasattr(self.main_window, 'highlight_code'):
                    self.main_window.highlight_code()
                if hasattr(self.main_window, 'current_note_id') and self.main_window.current_note_id:
                    if hasattr(self.main_window, 'format_text'):
                        self.main_window.format_text()
            except Exception:
                pass

    def closeEvent(self, event):
        self.apply_timer.stop()
        if self.main_window and self.main_window.isVisible():
            self.apply_all_settings()
        else:
            self.config_data["theme"] = "light" if self.appearance_page.theme_combo.currentIndex() == 0 else "dark"
            highlight_index = self.appearance_page.highlight_theme_combo.currentIndex()
            highlight_map = {0: "default", 1: "monokai", 2: "solarized", 3: "dracula"}
            self.config_data["highlight_theme"] = highlight_map.get(highlight_index, "default")
            self.config_data["editor"]["font_size"] = self.editor_page.font_size_spin.value()
            self.config_data["editor"]["tab_size"] = self.editor_page.tab_size_spin.value()
            self.config_data["editor"]["show_line_numbers"] = self.editor_page.show_lines_check.isChecked()
            self.config_data["editor"]["auto_save"] = self.editor_page.autosave_check.isChecked()
            self.config_data["editor"]["auto_save_interval"] = self.editor_page.autosave_interval_spin.value()
            self.config_data["html"]["default_version"] = self.html_page.html_version_combo.currentText()
            self.config_data["html"]["default_encoding"] = self.html_page.html_encoding_combo.currentText()
            self.config_data["html"]["auto_format"] = self.html_page.auto_format_check.isChecked()
            self.config_data["backup"]["enabled"] = self.backup_page.backup_check.isChecked()
            self.config_data["backup"]["interval"] = self.backup_page.backup_interval_spin.value()
            self.config_data["backup"]["location"] = self.backup_page.backup_location_edit.text()
            self.save_config()
        event.accept()
