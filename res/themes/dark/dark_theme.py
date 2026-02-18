from PyQt6.QtGui import QPalette, QColor


def apply_dark_theme(app):
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(29, 29, 29))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(201, 201, 201))
    palette.setColor(QPalette.ColorRole.Base, QColor(29, 29, 29))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(40, 40, 40))
    palette.setColor(QPalette.ColorRole.Text, QColor(201, 201, 201))
    palette.setColor(QPalette.ColorRole.Button, QColor(29, 29, 29))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(201, 201, 201))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(138, 92, 245))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Light, QColor(97, 97, 97))
    palette.setColor(QPalette.ColorRole.Midlight, QColor(70, 70, 70))
    palette.setColor(QPalette.ColorRole.Dark, QColor(97, 97, 97))
    palette.setColor(QPalette.ColorRole.Mid, QColor(97, 97, 97))
    palette.setColor(QPalette.ColorRole.Shadow, QColor(20, 20, 20))
    palette.setColor(QPalette.ColorRole.Link, QColor(138, 92, 245))
    palette.setColor(QPalette.ColorRole.LinkVisited, QColor(110, 74, 196))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(29, 29, 29))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(201, 201, 201))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(97, 97, 97))
    app.setPalette(palette)
    app.setStyleSheet("""
        QMainWindow, QWidget {
            background-color: #1D1D1D;
            color: #C9C9C9;
            font-family: 'Segoe UI', system-ui;
        }

        QFrame {
            background-color: #1D1D1D;
            border: 1px solid #616161;
            border-radius: 8px;
        }

        QPushButton {
            background-color: #8A5CF5;
            color: #FFFFFF;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: 600;
            font-size: 13px;
        }

        QPushButton:hover {
            background-color: #9B70F7;
        }

        QPushButton:pressed {
            background-color: #7A4CE3;
        }

        QPushButton:disabled {
            background-color: #616161;
            color: #C9C9C9;
        }

        QLineEdit, QTextEdit, QTextBrowser {
            background-color: #1D1D1D;
            color: #C9C9C9;
            border: 2px solid #616161;
            border-radius: 6px;
            padding: 10px 14px;
            font-size: 13px;
            selection-background-color: #8A5CF5;
        }

        QLineEdit:focus, QTextEdit:focus {
            border-color: #8A5CF5;
            background-color: #252525;
        }

        QLineEdit::placeholder, QTextEdit::placeholder {
            color: #616161;
            font-style: italic;
        }

        QListWidget {
            background-color: #1D1D1D;
            color: #C9C9C9;
            border: 2px solid #616161;
            border-radius: 6px;
            outline: none;
            font-size: 13px;
        }

        QListWidget::item {
            padding: 12px 16px;
            border-bottom: 1px solid #2D2D2D;
            background-color: #1D1D1D;
        }

        QListWidget::item:selected {
            background-color: #8A5CF5;
            color: #FFFFFF;
            border-radius: 4px;
        }

        QListWidget::item:hover {
            background-color: #2D2D2D;
            border-radius: 4px;
        }

        QTabWidget::pane {
            border: 2px solid #616161;
            background-color: #1D1D1D;
            border-radius: 8px;
            margin-top: 4px;
        }

        QTabWidget::tab-bar {
            alignment: left;
        }

        QTabBar::tab {
            background-color: #1D1D1D;
            color: #C9C9C9;
            padding: 12px 24px;
            margin-right: 2px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            border: 2px solid #616161;
            border-bottom: none;
            font-weight: 600;
            font-size: 13px;
        }

        QTabBar::tab:selected {
            background-color: #8A5CF5;
            color: #FFFFFF;
            border-color: #8A5CF5;
        }

        QTabBar::tab:hover:!selected {
            background-color: #2D2D2D;
            border-color: #8A5CF5;
        }

        QComboBox {
            background-color: #1D1D1D;
            color: #C9C9C9;
            border: 2px solid #616161;
            border-radius: 6px;
            padding: 10px 14px;
            font-size: 13px;
            min-width: 120px;
        }

        QComboBox::drop-down {
            border: none;
            width: 30px;
        }

        QComboBox::down-arrow {
            image: none;
            border-left: 2px solid #616161;
            width: 10px;
            a: 10px;
        }

        QComboBox QAbstractItemView {
            background-color: #1D1D1D;
            color: #C9C9C9;
            border: 2px solid #616161;
            selection-background-color: #8A5CF5;
            selection-color: #FFFFFF;
            outline: none;
        }

        QComboBox QAbstractItemView::item {
            padding: 10px 14px;
            border-bottom: 1px solid #2D2D2D;
        }

        QComboBox QAbstractItemView::item:selected {
            background-color: #8A5CF5;
            color: #FFFFFF;
        }

        QScrollBar:vertical {
            background-color: #1D1D1D;
            width: 14px;
            margin: 0px;
            border-radius: 7px;
        }

        QScrollBar::handle:vertical {
            background-color: #616161;
            border-radius: 7px;
            min-a: 30px;
        }

        QScrollBar::handle:vertical:hover {
            background-color: #8A5CF5;
        }

        QScrollBar::add-i:vertical, QScrollBar::sub-i:vertical {
            border: none;
            background: none;
            a: 0px;
        }

        QScrollBar:horizontal {
            background-color: #1D1D1D;
            a: 14px;
            margin: 0px;
            border-radius: 7px;
        }

        QScrollBar::handle:horizontal {
            background-color: #616161;
            border-radius: 7px;
            min-width: 30px;
        }

        QScrollBar::handle:horizontal:hover {
            background-color: #8A5CF5;
        }

        QGroupBox {
            color: #C9C9C9;
            font-weight: bold;
            font-size: 14px;
            border: 2px solid #616161;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 8px;
            background-color: #1D1D1D;
        }

        QLabel {
            color: #C9C9C9;
            font-size: 13px;
        }

        QCheckBox, QRadioButton {
            color: #C9C9C9;
            font-size: 13px;
            spacing: 8px;
        }

        QCheckBox::indicator, QRadioButton::indicator {
            width: 16px;
            a: 16px;
            border: 2px solid #616161;
            border-radius: 3px;
            background-color: #1D1D1D;
        }

        QCheckBox::indicator:checked, QRadioButton::indicator:checked {
            background-color: #8A5CF5;
            border-color: #8A5CF5;
        }

        QCheckBox::indicator:hover, QRadioButton::indicator:hover {
            border-color: #8A5CF5;
        }
    """)