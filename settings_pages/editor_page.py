from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QPushButton, \
    QSpinBox, QCheckBox


class EditorPage(QWidget):
    def __init__(self, settings_window):
        super().__init__()
        self.settings_window = settings_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        editor_group = QGroupBox("Настройки редактора")
        editor_layout = QVBoxLayout()
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("Размер шрифта:"))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 24)
        self.font_size_spin.setValue(self.settings_window.config_data["editor"]["font_size"])
        self.font_size_spin.valueChanged.connect(self.settings_window.schedule_apply)
        font_layout.addWidget(self.font_size_spin)
        editor_layout.addLayout(font_layout)
        tab_layout = QHBoxLayout()
        tab_layout.addWidget(QLabel("Размер табуляции (пробелов):"))
        self.tab_size_spin = QSpinBox()
        self.tab_size_spin.setRange(2, 8)
        self.tab_size_spin.setValue(self.settings_window.config_data["editor"]["tab_size"])
        self.tab_size_spin.valueChanged.connect(self.settings_window.schedule_apply)
        tab_layout.addWidget(self.tab_size_spin)
        editor_layout.addLayout(tab_layout)
        self.show_lines_check = QCheckBox("Показывать номера строк")
        self.show_lines_check.setChecked(self.settings_window.config_data["editor"]["show_line_numbers"])
        self.show_lines_check.stateChanged.connect(self.settings_window.schedule_apply)
        editor_layout.addWidget(self.show_lines_check)
        editor_group.setLayout(editor_layout)
        layout.addWidget(editor_group)
        autosave_group = QGroupBox("Автосохранение")
        autosave_layout = QVBoxLayout()
        self.autosave_check = QCheckBox("Включить автосохранение")
        self.autosave_check.setChecked(self.settings_window.config_data["editor"]["auto_save"])
        self.autosave_check.stateChanged.connect(self.settings_window.schedule_apply)
        autosave_layout.addWidget(self.autosave_check)
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("Интервал автосохранения (минут):"))
        self.autosave_interval_spin = QSpinBox()
        self.autosave_interval_spin.setRange(1, 30)
        self.autosave_interval_spin.setValue(self.settings_window.config_data["editor"]["auto_save_interval"])
        self.autosave_interval_spin.valueChanged.connect(self.settings_window.schedule_apply)
        interval_layout.addWidget(self.autosave_interval_spin)
        autosave_layout.addLayout(interval_layout)
        autosave_group.setLayout(autosave_layout)
        layout.addWidget(autosave_group)
        self.apply_editor_btn = QPushButton("Применить настройки")
        self.apply_editor_btn.clicked.connect(self.apply_editor_settings)
        layout.addWidget(self.apply_editor_btn)
        layout.addStretch()

    def apply_editor_settings(self):
        self.settings_window.config_data["editor"]["font_size"] = self.font_size_spin.value()
        self.settings_window.config_data["editor"]["tab_size"] = self.tab_size_spin.value()
        self.settings_window.config_data["editor"]["show_line_numbers"] = self.show_lines_check.isChecked()
        self.settings_window.config_data["editor"]["auto_save"] = self.autosave_check.isChecked()
        self.settings_window.config_data["editor"]["auto_save_interval"] = self.autosave_interval_spin.value()
        self.settings_window.save_config()
        if self.settings_window.main_window:
            self.settings_window.main_window.config_data = self.settings_window.config_data
            self.settings_window.main_window.apply_editor_settings()
            if hasattr(self.settings_window.main_window, 'setup_auto_save'):
                self.settings_window.main_window.setup_auto_save()
