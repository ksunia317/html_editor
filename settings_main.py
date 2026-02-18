import sys
from PyQt6.QtWidgets import QApplication
from settings_window import SettingsWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SettingsWindow()
    ex.show()
    sys.exit(app.exec())