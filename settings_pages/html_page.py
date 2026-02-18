from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QComboBox, QPushButton, \
    QCheckBox


class HtmlPage(QWidget):
    def __init__(self, settings_window):
        super().__init__()
        self.settings_window = settings_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        html_group = QGroupBox("Настройки HTML")
        html_layout = QVBoxLayout()
        version_layout = QHBoxLayout()
        version_layout.addWidget(QLabel("Версия HTML по умолчанию:"))
        self.html_version_combo = QComboBox()
        self.html_version_combo.addItems(["HTML5", "HTML 4.01", "XHTML 1.0"])
        self.html_version_combo.setCurrentText(self.settings_window.config_data["html"]["default_version"])
        self.html_version_combo.currentIndexChanged.connect(self.settings_window.schedule_apply)
        version_layout.addWidget(self.html_version_combo)
        html_layout.addLayout(version_layout)
        encoding_layout = QHBoxLayout()
        encoding_layout.addWidget(QLabel("Кодировка по умолчанию:"))
        self.html_encoding_combo = QComboBox()
        self.html_encoding_combo.addItems(["UTF-8", "windows-1251", "KOI8-R"])
        self.html_encoding_combo.setCurrentText(self.settings_window.config_data["html"]["default_encoding"])
        self.html_encoding_combo.currentIndexChanged.connect(self.settings_window.schedule_apply)
        encoding_layout.addWidget(self.html_encoding_combo)
        html_layout.addLayout(encoding_layout)
        self.auto_format_check = QCheckBox("Автоматически форматировать код при открытии")
        self.auto_format_check.setChecked(self.settings_window.config_data["html"]["auto_format"])
        self.auto_format_check.stateChanged.connect(self.settings_window.schedule_apply)
        html_layout.addWidget(self.auto_format_check)
        html_group.setLayout(html_layout)
        layout.addWidget(html_group)
        self.apply_html_btn = QPushButton("Сохранить настройки HTML")
        self.apply_html_btn.clicked.connect(self.apply_html_settings_now)
        layout.addWidget(self.apply_html_btn)
        layout.addStretch()

    def apply_html_settings_now(self):
        if not self.settings_window.main_window or not self.settings_window.main_window.isVisible():
            self.settings_window.config_data["html"]["default_version"] = self.html_version_combo.currentText()
            self.settings_window.config_data["html"]["default_encoding"] = self.html_encoding_combo.currentText()
            self.settings_window.config_data["html"]["auto_format"] = self.auto_format_check.isChecked()
            self.settings_window.save_config()
            return
        self.settings_window.config_data["html"]["default_version"] = self.html_version_combo.currentText()
        self.settings_window.config_data["html"]["default_encoding"] = self.html_encoding_combo.currentText()
        self.settings_window.config_data["html"]["auto_format"] = self.auto_format_check.isChecked()
        self.settings_window.save_config()
        if self.settings_window.main_window:
            try:
                self.settings_window.main_window.config_data = self.settings_window.config_data
                if hasattr(self.settings_window.main_window, 'apply_html_settings'):
                    self.settings_window.main_window.apply_html_settings()
            except Exception:
                pass
