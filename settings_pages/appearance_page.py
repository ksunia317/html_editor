from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QComboBox, QPushButton


class AppearancePage(QWidget):
    def __init__(self, settings_window):
        super().__init__()
        self.settings_window = settings_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        theme_group = QGroupBox("Тема приложения")
        theme_layout = QVBoxLayout()
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Светлая тема", "Темная тема"])
        if self.settings_window.config_data.get("theme", "dark") == "light":
            self.theme_combo.setCurrentIndex(0)
        else:
            self.theme_combo.setCurrentIndex(1)
        self.theme_combo.currentIndexChanged.connect(self.settings_window.schedule_apply)
        theme_layout.addWidget(QLabel("Выберите тему:"))
        theme_layout.addWidget(self.theme_combo)
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        highlight_group = QGroupBox("Подсветка синтаксиса")
        highlight_layout = QVBoxLayout()
        theme_highlight_layout = QHBoxLayout()
        theme_highlight_layout.addWidget(QLabel("Тема подсветки:"))
        self.highlight_theme_combo = QComboBox()
        self.highlight_theme_combo.addItems(["По умолчанию", "Monokai", "Solarized", "Dracula"])
        current_highlight = self.settings_window.config_data.get("highlight_theme", "default")
        index_map = {"default": 0, "monokai": 1, "solarized": 2, "dracula": 3}
        self.highlight_theme_combo.setCurrentIndex(index_map.get(current_highlight, 0))
        self.highlight_theme_combo.currentIndexChanged.connect(self.settings_window.schedule_apply)
        theme_highlight_layout.addWidget(self.highlight_theme_combo)
        highlight_layout.addLayout(theme_highlight_layout)
        highlight_group.setLayout(highlight_layout)
        layout.addWidget(highlight_group)
        self.apply_appearance_btn = QPushButton("Сохранить настройки внешнего вида")
        self.apply_appearance_btn.clicked.connect(self.apply_settings_now)
        layout.addWidget(self.apply_appearance_btn)
        layout.addStretch()

    def apply_settings_now(self):
        if not self.settings_window.main_window or not self.settings_window.main_window.isVisible():
            self.settings_window.config_data["theme"] = "light" if self.theme_combo.currentIndex() == 0 else "dark"
            highlight_index = self.highlight_theme_combo.currentIndex()
            highlight_map = {0: "default", 1: "monokai", 2: "solarized", 3: "dracula"}
            self.settings_window.config_data["highlight_theme"] = highlight_map.get(highlight_index, "default")
            self.settings_window.save_config()
            return
        self.settings_window.config_data["theme"] = "light" if self.theme_combo.currentIndex() == 0 else "dark"
        highlight_index = self.highlight_theme_combo.currentIndex()
        highlight_map = {0: "default", 1: "monokai", 2: "solarized", 3: "dracula"}
        self.settings_window.config_data["highlight_theme"] = highlight_map.get(highlight_index, "default")
        self.settings_window.save_config()
        if self.settings_window.main_window:
            try:
                self.settings_window.main_window.theme = self.settings_window.config_data["theme"]
                self.settings_window.main_window.apply_theme()
                if hasattr(self.settings_window.main_window, 'highlight_code'):
                    self.settings_window.main_window.highlight_code()
            except Exception:
                pass
