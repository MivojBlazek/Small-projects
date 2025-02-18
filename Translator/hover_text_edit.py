from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor, QPalette

class HoverTextEdit(QTextEdit):
    def __init__(self, sentences, is_source, parent=None):
        super().__init__(parent)
        self.sentences = sentences
        self.is_source = is_source
        self.second_text_edit = None
        self.setMouseTracking(True)
        self.highlighted_format = QTextCharFormat()
        
        # Choose highlight color
        palette = self.palette()
        if palette.color(QPalette.ColorRole.Window).value() < 128: # Dark mode
            highlight_color = QColor("darkblue")
        else: # Light mode
            highlight_color = QColor("lightblue")
        self.highlighted_format.setBackground(highlight_color)

    def set_second_text_edit(self, second):
        self.second_text_edit = second

    def mouseMoveEvent(self, event):
        cursor = self.cursorForPosition(event.pos())
        sentence_cursor, sentence_index = self.get_sentence(cursor)
        if sentence_cursor:
            extra_selection = QTextEdit.ExtraSelection()
            extra_selection.cursor = sentence_cursor
            extra_selection.format = self.highlighted_format
            self.setExtraSelections([extra_selection])
            if self.second_text_edit:
                self.second_text_edit.highlight_sentence(sentence_index, not self.is_source)
        else:
            self.setExtraSelections([])
            if self.second_text_edit:
                self.second_text_edit.setExtraSelections([])
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self.setExtraSelections([])
        if self.second_text_edit:
            self.second_text_edit.setExtraSelections([])
        super().leaveEvent(event)
    
    def get_sentence(self, cursor):
        pos = cursor.position()
        start = 0
        document_length = len(self.toPlainText())
        for index, sentence in enumerate(self.sentences):
            if self.is_source:
                end = start + len(sentence.text)
            else:
                end = start + len(sentence.translation)
            if start <= pos < end:
                if end > document_length:
                    return None, None
                sentence_cursor = QTextCursor(self.document())
                sentence_cursor.setPosition(start)
                sentence_cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
                return sentence_cursor, index
            if self.is_source:
                start = end
            else:
                start = end + 1
        return None, None
    
    def update_sentences(self, sentences):
        self.sentences = sentences

    def highlight_sentence(self, index, is_source):
        if index is not None:
            sentence = self.sentences[index]
            if is_source:
                start = sentence.start_position
                end = start + len(sentence.text)
            else:
                start = sentence.translation_start_position
                end = start + len(sentence.translation)
            sentence_cursor = QTextCursor(self.document())
            sentence_cursor.setPosition(start)
            sentence_cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
            extra_selection = QTextEdit.ExtraSelection()
            extra_selection.cursor = sentence_cursor
            extra_selection.format = self.highlighted_format
            self.setExtraSelections([extra_selection])
