from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt6.QtGui import QTextDocument


class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Поиск")
        self.setModal(False)
        self.setMinimumWidth(350)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint)
        layout = QVBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите текст для поиска...")
        self.search_input.textChanged.connect(self.search_text_changed)
        layout.addWidget(QLabel("Найти:"))
        layout.addWidget(self.search_input)
        self.result_count_label = QLabel("Найдено: 0")
        self.result_count_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.result_count_label)
        button_layout = QHBoxLayout()
        self.find_next_btn = QPushButton("Найти далее")
        self.find_next_btn.clicked.connect(self.find_next)
        self.find_next_btn.setEnabled(False)
        self.find_prev_btn = QPushButton("Найти предыдущий")
        self.find_prev_btn.clicked.connect(self.find_prev)
        self.find_prev_btn.setEnabled(False)
        self.close_btn = QPushButton("Закрыть")
        self.close_btn.clicked.connect(self.close)
        button_layout.addWidget(self.find_next_btn)
        button_layout.addWidget(self.find_prev_btn)
        button_layout.addWidget(self.close_btn)
        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.search_input.returnPressed.connect(self.find_next)

    def search_text_changed(self, text):
        has_text = bool(text.strip())
        self.find_next_btn.setEnabled(has_text)
        self.find_prev_btn.setEnabled(has_text)
        if has_text:
            self.update_result_count()
        else:
            self.result_count_label.setText("Найдено: 0")
            if self.parent() and self.parent().current_note_id:
                cursor = self.parent().note_input.textCursor()
                cursor.clearSelection()
                self.parent().note_input.setTextCursor(cursor)

    def update_result_count(self):
        if not self.parent() or self.parent().current_note_id is None:
            return
        text = self.search_input.text()
        if not text:
            self.result_count_label.setText("Найдено: 0")
            return
        document = self.parent().note_input.document()
        content = document.toPlainText()
        count = content.count(text)
        self.result_count_label.setText(f"Найдено: {count}")

    def find_next(self):
        if not self.parent() or self.parent().current_note_id is None:
            return
        text = self.search_input.text()
        if not text:
            return
        parent = self.parent()
        cursor = parent.note_input.textCursor()
        document = parent.note_input.document()
        found = document.find(text, cursor)
        if found.isNull():
            cursor.setPosition(0)
            found = document.find(text, cursor)
        if not found.isNull():
            parent.note_input.setTextCursor(found)
            parent.note_input.ensureCursorVisible()
        self.update_result_count()

    def find_prev(self):
        if not self.parent() or self.parent().current_note_id is None:
            return
        text = self.search_input.text()
        if not text:
            return
        parent = self.parent()
        cursor = parent.note_input.textCursor()
        document = parent.note_input.document()
        found = document.find(text, cursor, QTextDocument.FindFlag.FindBackward)
        if found.isNull():
            cursor.setPosition(document.characterCount() - 1)
            found = document.find(text, cursor, QTextDocument.FindFlag.FindBackward)
        if not found.isNull():
            parent.note_input.setTextCursor(found)
            parent.note_input.ensureCursorVisible()
        self.update_result_count()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
            return
        if event.key() == Qt.Key.Key_Return and event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            self.find_prev()
            return
        if event.key() == Qt.Key.Key_Return:
            self.find_next()
            return
        super().keyPressEvent(event)

    def closeEvent(self, event):
        if self.parent() and self.parent().current_note_id:
            cursor = self.parent().note_input.textCursor()
            cursor.clearSelection()
            self.parent().note_input.setTextCursor(cursor)
        event.accept()