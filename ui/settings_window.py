import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QFrame, QHBoxLayout, QPushButton, \
    QListWidget, QComboBox, QStackedWidget, QGroupBox


class SettingsWindow(QWidget):
    def __init__(self, theme="light", parent=None):
        super().__init__(parent, Qt.WindowType.Window)
        self.main_window = parent
        self.theme = theme
        self.initUI()

    def initUI(self):
        self.resize(800, 600)
        self.setWindowTitle('Settings')
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.left_column = QFrame()
        self.left_column.setFixedWidth(200)
        self.settings_list = QListWidget()
        self.settings_list.addItems(["Внешний вид"])
        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(10, 10, 10, 10)
        self.left_layout.addWidget(self.settings_list)
        self.left_column.setLayout(self.left_layout)
        self.right_column = QFrame()
        self.settings_stack = QStackedWidget()
        self.appearance_page = QWidget()
        self.setupAppearancePage()
        self.settings_stack.addWidget(self.appearance_page)
        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(10, 10, 10, 10)
        self.right_layout.addWidget(self.settings_stack)
        self.right_column.setLayout(self.right_layout)
        self.main_layout.addWidget(self.left_column)
        self.main_layout.addWidget(self.right_column)

    def setupAppearancePage(self):
        layout = QVBoxLayout(self.appearance_page)
        theme_group = QGroupBox("Тема приложения")
        theme_layout = QVBoxLayout()
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Светлая тема", "Темная тема"])
        if self.theme == "light":
            self.theme_combo.setCurrentIndex(0)
        else:
            self.theme_combo.setCurrentIndex(1)
        self.apply_theme_button = QPushButton("Применить тему")
        theme_layout.addWidget(QLabel("Выберите тему:"))
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addWidget(self.apply_theme_button)
        self.apply_theme_button.clicked.connect(self.apply_theme)
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        layout.addStretch()

    def apply_theme(self):
        if self.theme_combo.currentIndex() == 0:
            self.theme = 'light'
            self.main_window.theme = 'light'
        else:
            self.theme = 'dark'
            self.main_window.theme = 'dark'
        self.main_window.apply_theme()
        self.main_window.highlihting()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SettingsWindow()
    ex.show()
    sys.exit(app.exec())
