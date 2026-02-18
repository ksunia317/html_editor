from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLabel



class AboutPage(QWidget):
    def __init__(self, settings_window):
        super().__init__()
        self.settings_window = settings_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        about_group = QGroupBox("О программе")
        about_layout = QVBoxLayout()
        with open("docs/about.txt", "r", encoding="utf-8") as f:
            about_label = QLabel(f.read())
        about_label.setWordWrap(True)
        about_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        about_layout.addWidget(about_label)
        about_group.setLayout(about_layout)
        layout.addWidget(about_group)
        layout.addStretch()
