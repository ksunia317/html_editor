from PyQt6.QtGui import QPalette, QColor


def apply_light_theme(app):
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(248, 248, 248))  # Светлый фон
    palette.setColor(QPalette.ColorRole.WindowText, QColor(29, 29, 29))  # #1D1D1D
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))  # Белый для контента
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
    palette.setColor(QPalette.ColorRole.Text, QColor(29, 29, 29))  # #1D1D1D
    palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(29, 29, 29))  # #1D1D1D
    palette.setColor(QPalette.ColorRole.Highlight, QColor(138, 92, 245))  # #8A5CF5
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Light, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.Midlight, QColor(200, 200, 200))
    palette.setColor(QPalette.ColorRole.Dark, QColor(150, 150, 150))
    palette.setColor(QPalette.ColorRole.Mid, QColor(180, 180, 180))
    palette.setColor(QPalette.ColorRole.Shadow, QColor(120, 120, 120))
    palette.setColor(QPalette.ColorRole.Link, QColor(138, 92, 245))  # #8A5CF5
    palette.setColor(QPalette.ColorRole.LinkVisited, QColor(110, 74, 196))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(29, 29, 29))  # #1D1D1D
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(97, 97, 97))  # #616161
    app.setPalette(palette)
    app.setStyleSheet("""
        QMainWindow, QWidget {
            background-color: #F8F8F8;
            color: #1D1D1D;
            font-family: 'Segoe UI', system-ui;
        }

        QFrame {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
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
            background-color: #C9C9C9;
            color: #616161;
        }

        QLineEdit, QTextEdit, QTextBrowser {
            background-color: #FFFFFF;
            color: #1D1D1D;
            border: 1px solid #E0E0E0;
            border-radius: 6px;
            padding: 10px 14px;
            font-size: 13px;
            selection-background-color: #8A5CF5;
            selection-color: #FFFFFF;
        }

        QLineEdit:focus, QTextEdit:focus {
            border-color: #8A5CF5;
            background-color: #FFFFFF;
        }

        QLineEdit::placeholder, QTextEdit::placeholder {
            color: #616161;
            font-style: italic;
        }

        QListWidget {
            background-color: #FFFFFF;
            color: #1D1D1D;
            border: 1px solid #E0E0E0;
            border-radius: 6px;
            outline: none;
            font-size: 13px;
        }

        QListWidget::item {
            padding: 12px 16px;
            border-bottom: 1px solid #F0F0F0;
            background-color: #FFFFFF;
        }

        QListWidget::item:selected {
            background-color: #8A5CF5;
            color: #FFFFFF;
            border-radius: 4px;
        }

        QListWidget::item:hover {
            background-color: #F8F8F8;
            border-radius: 4px;
        }

        QTabWidget::pane {
            border: 1px solid #E0E0E0;
            background-color: #FFFFFF;
            border-radius: 8px;
            margin-top: 4px;
        }

        QTabWidget::tab-bar {
            alignment: left;
        }

        QTabBar::tab {
            background-color: #F0F0F0;
            color: #616161;
            padding: 12px 24px;
            margin-right: 2px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            border: 1px solid #E0E0E0;
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
            background-color: #E8E8E8;
            color: #1D1D1D;
        }

        QComboBox {
            background-color: #FFFFFF;
            color: #1D1D1D;
            border: 1px solid #E0E0E0;
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
            border-left: 1px solid #E0E0E0;
            width: 10px;
            a: 10px;
        }

        QComboBox QAbstractItemView {
            background-color: #FFFFFF;
            color: #1D1D1D;
            border: 1px solid #E0E0E0;
            selection-background-color: #8A5CF5;
            selection-color: #FFFFFF;
            outline: none;
        }

        QComboBox QAbstractItemView::item {
            padding: 10px 14px;
            border-bottom: 1px solid #F0F0F0;
        }

        QComboBox QAbstractItemView::item:selected {
            background-color: #8A5CF5;
            color: #FFFFFF;
        }

        QScrollBar:vertical {
            background-color: #F0F0F0;
            width: 12px;
            margin: 0px;
            border-radius: 6px;
        }

        QScrollBar::handle:vertical {
            background-color: #C9C9C9;
            border-radius: 6px;
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
            background-color: #F0F0F0;
            a: 12px;
            margin: 0px;
            border-radius: 6px;
        }

        QScrollBar::handle:horizontal {
            background-color: #C9C9C9;
            border-radius: 6px;
            min-width: 30px;
        }

        QScrollBar::handle:horizontal:hover {
            background-color: #8A5CF5;
        }

        QGroupBox {
            color: #1D1D1D;
            font-weight: bold;
            font-size: 14px;
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
            background-color: #FFFFFF;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 8px;
            background-color: #FFFFFF;
        }

        QLabel {
            color: #1D1D1D;
            font-size: 13px;
        }

        QCheckBox, QRadioButton {
            color: #1D1D1D;
            font-size: 13px;
            spacing: 8px;
        }

        QCheckBox::indicator, QRadioButton::indicator {
            width: 16px;
            a: 16px;
            border: 1px solid #C9C9C9;
            border-radius: 3px;
            background-color: #FFFFFF;
        }

        QCheckBox::indicator:checked, QRadioButton::indicator:checked {
            background-color: #8A5CF5;
            border-color: #8A5CF5;
        }

        QCheckBox::indicator:hover, QRadioButton::indicator:hover {
            border-color: #8A5CF5;
        }
    """)