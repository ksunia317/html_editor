from PyQt6.QtWidgets import QWidget, QVBoxLayout, \
    QTextEdit, QTabWidget


class DocsPage(QWidget):
    def __init__(self, settings_window):
        super().__init__()
        self.settings_window = settings_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        docs_tabs = QTabWidget()
        html_docs = QWidget()
        html_layout = QVBoxLayout(html_docs)
        html_text = QTextEdit()
        html_text.setReadOnly(True)
        with open("docs/html.txt", "r", encoding="utf-8") as f:
            html_text.setHtml(f.read())
        html_layout.addWidget(html_text)
        docs_tabs.addTab(html_docs, "HTML")
        css_docs = QWidget()
        css_layout = QVBoxLayout(css_docs)
        css_text = QTextEdit()
        css_text.setReadOnly(True)
        with open("docs/css.txt", "r", encoding="utf-8") as f:
            css_text.setHtml(f.read())
        css_layout.addWidget(css_text)
        docs_tabs.addTab(css_docs, "CSS")
        hot_keys_docs = QWidget()
        hot_keys_layout = QVBoxLayout(hot_keys_docs)
        hot_keys_text = QTextEdit()
        hot_keys_text.setReadOnly(True)
        with open("docs/hot_keys.txt", "r", encoding="utf-8") as f:
            hot_keys_text.setHtml(f.read())
        hot_keys_layout.addWidget(hot_keys_text)
        docs_tabs.addTab(hot_keys_docs, "Горячие клавиши")
        layout.addWidget(docs_tabs)
