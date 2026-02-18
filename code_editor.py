from PyQt6.QtGui import QColor, QPainter, QTextFormat, QTextCursor
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtWidgets import QTextEdit, QWidget


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint(event)


class CodeEditor(QTextEdit):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.line_number_area = LineNumberArea(self)
        self.textChanged.connect(self.update_line_number)
        self.cursorPositionChanged.connect(self.highlight_cur_line)
        self.update_line_number()
        self.highlight_cur_line()
        self.is_highlighting = False

    def line_number_area_width(self):
        if not self.main_window or not self.main_window.config_data["editor"]["show_line_numbers"]:
            return 0
        digits = 1
        max_num = max(1, self.document().blockCount())
        while max_num >= 10:
            max_num /= 10
            digits += 1
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number(self):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_area_paint(self, event):
        if not self.main_window or not self.main_window.config_data["editor"]["show_line_numbers"]:
            return
        painter = QPainter(self.line_number_area)
        if self.main_window.theme == "light":
            painter.fillRect(event.rect(), QColor(240, 240, 240))
            painter.setPen(QColor(100, 100, 100))
        else:
            painter.fillRect(event.rect(), QColor(50, 50, 50))
            painter.setPen(QColor(150, 150, 150))
        document = self.document()
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        block = document.begin()
        block_num = 0
        while block.isValid():
            cursor.setPosition(block.position())
            rect = self.cursorRect(cursor)
            if rect.top() >= event.rect().top() - 20 and rect.bottom() <= event.rect().bottom() + 20:
                num = str(block_num + 1)
                painter.drawText(0, rect.top(), self.line_number_area.width() - 2, rect.height(),
                                 Qt.AlignmentFlag.AlignRight, num)
            block = block.next()
            block_num += 1

    def highlight_cur_line(self):
        extra_selections = []
        if self.isReadOnly():
            return
        selection = QTextEdit.ExtraSelection()
        line_color = QColor(230, 230, 230) if self.main_window.theme == "light" else QColor(60, 60, 60)
        selection.format.setBackground(line_color)
        selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()
        extra_selections.append(selection)
        self.setExtraSelections(extra_selections)