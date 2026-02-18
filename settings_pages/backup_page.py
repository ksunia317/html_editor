from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QPushButton, \
    QSpinBox, QCheckBox, QLineEdit,  QFileDialog



class BackupPage(QWidget):
    def __init__(self, settings_window):
        super().__init__()
        self.settings_window = settings_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        backup_group = QGroupBox("Резервное копирование")
        backup_layout = QVBoxLayout()
        self.backup_check = QCheckBox("Включить резервное копирование")
        self.backup_check.setChecked(self.settings_window.config_data["backup"]["enabled"])
        self.backup_check.stateChanged.connect(self.settings_window.schedule_apply)
        backup_layout.addWidget(self.backup_check)
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("Интервал резервного копирования (минут):"))
        self.backup_interval_spin = QSpinBox()
        self.backup_interval_spin.setRange(1, 60)
        self.backup_interval_spin.setValue(self.settings_window.config_data["backup"]["interval"])
        self.backup_interval_spin.valueChanged.connect(self.settings_window.schedule_apply)
        interval_layout.addWidget(self.backup_interval_spin)
        backup_layout.addLayout(interval_layout)
        location_layout = QHBoxLayout()
        location_layout.addWidget(QLabel("Папка для резервных копий:"))
        self.backup_location_edit = QLineEdit()
        self.backup_location_edit.setText(self.settings_window.config_data["backup"]["location"])
        self.backup_location_edit.textChanged.connect(self.settings_window.schedule_apply)
        location_layout.addWidget(self.backup_location_edit)
        backup_layout.addLayout(location_layout)
        self.choose_folder_btn = QPushButton("Выбрать папку")
        self.choose_folder_btn.clicked.connect(self.choose_backup_folder)
        backup_layout.addWidget(self.choose_folder_btn)
        backup_group.setLayout(backup_layout)
        layout.addWidget(backup_group)
        self.apply_backup_btn = QPushButton("Сохранить настройки резервного копирования")
        self.apply_backup_btn.clicked.connect(self.apply_backup_settings_now)
        layout.addWidget(self.apply_backup_btn)
        layout.addStretch()

    def choose_backup_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку для резервных копий")
        if folder:
            self.backup_location_edit.setText(folder)
            self.settings_window.schedule_apply()

    def apply_backup_settings_now(self):
        if not self.settings_window.main_window or not self.settings_window.main_window.isVisible():
            self.settings_window.config_data["backup"]["enabled"] = self.backup_check.isChecked()
            self.settings_window.config_data["backup"]["interval"] = self.backup_interval_spin.value()
            self.settings_window.config_data["backup"]["location"] = self.backup_location_edit.text()
            self.settings_window.save_config()
            return
        self.settings_window.config_data["backup"]["enabled"] = self.backup_check.isChecked()
        self.settings_window.config_data["backup"]["interval"] = self.backup_interval_spin.value()
        self.settings_window.config_data["backup"]["location"] = self.backup_location_edit.text()
        self.settings_window.save_config()
        if self.settings_window.main_window:
            try:
                self.settings_window.main_window.config_data = self.settings_window.config_data
            except Exception:
                pass