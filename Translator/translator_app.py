import re
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QSpacerItem, QGraphicsOpacityEffect
from PyQt6.QtCore import QTimer, Qt, QPropertyAnimation
from deep_translator import GoogleTranslator
from styling import style_button, style_text_edit, style_info_text
from sentence import Sentence
from hover_text_edit import HoverTextEdit

class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.sentences = []
        self.init_ui()

    def init_ui(self):
        self.resize(1600, 900)
        self.main_layout = QVBoxLayout()
        self.text_layout = QHBoxLayout()
        
        # Text input and output widgets
        self.input_label = QLabel("English:", self)
        self.output_label = QLabel("Czech:", self)
        self.input_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.output_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        self.source_text = HoverTextEdit(self.sentences, is_source=True, parent=self)
        self.translated_text = HoverTextEdit(self.sentences, is_source=False, parent=self)
        self.source_text.set_second_text_edit(self.translated_text)
        self.translated_text.set_second_text_edit(self.source_text)
        self.translated_text.setReadOnly(True)
        
        # Synchronize scrolling
        self.source_text.verticalScrollBar().valueChanged.connect(self.sync_scroll)
        self.translated_text.verticalScrollBar().valueChanged.connect(self.sync_scroll)
        
        # Copy text buttons
        self.copy_source_button = QPushButton("Copy", self)
        self.copy_source_button.clicked.connect(self.copy_source_text)
        self.copy_translated_button = QPushButton("Copy", self)
        self.copy_translated_button.clicked.connect(self.copy_translated_text)
        
        # Translate button
        self.translate_button = QPushButton("Translate", self)
        self.translate_button.clicked.connect(self.translate_text)
        
        # Remove newlines button
        self.auto_remove_newlines_button = QPushButton("Remove newlines Enabled", self)
        self.auto_remove_newlines_button.setCheckable(True)
        self.auto_remove_newlines_button.setChecked(True)
        self.auto_remove_newlines_button.clicked.connect(self.toggle_auto_remove_newlines)
        
        # Delete source text button
        self.delete_source_button = QPushButton("Delete", self)
        self.delete_source_button.clicked.connect(self.delete_source_text)
        
        # Info label
        self.info_label = QLabel("", self)
        style_info_text(self.info_label)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setVisible(False)
        
        # Add widgets to layout
        self.input_layout = QVBoxLayout()
        self.output_layout = QVBoxLayout()
        self.input_menu_layout = QHBoxLayout()
        self.output_menu_layout = QHBoxLayout()
        
        self.input_menu_layout.addWidget(self.delete_source_button)
        self.input_menu_layout.addWidget(self.auto_remove_newlines_button)
        self.input_menu_layout.addStretch()
        self.input_menu_layout.addWidget(self.copy_source_button)
        
        self.input_layout.addWidget(self.input_label)
        self.input_layout.addLayout(self.input_menu_layout)
        self.input_layout.addWidget(self.source_text)
        self.output_layout.addWidget(self.output_label)
        
        self.output_menu_layout.addWidget(self.translate_button)
        self.output_menu_layout.addStretch()
        self.output_menu_layout.addWidget(self.copy_translated_button)
        
        self.output_layout.addLayout(self.output_menu_layout)
        self.output_layout.addWidget(self.translated_text)
        
        self.text_layout.addLayout(self.input_layout)
        self.text_layout.addSpacerItem(QSpacerItem(30, 30))
        self.text_layout.addLayout(self.output_layout)
        
        self.main_layout.addLayout(self.text_layout)
        self.main_layout.addWidget(self.info_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(self.main_layout)
        
        # Style widgets
        style_text_edit(self.source_text)
        style_text_edit(self.translated_text)
        style_button(self.copy_source_button, "copy")
        style_button(self.copy_translated_button, "copy")
        style_button(self.translate_button, "main")
        style_button(self.auto_remove_newlines_button, "feature")
        style_button(self.delete_source_button, "delete")
    
    def sync_scroll(self):
        sender = self.sender()
        if sender == self.source_text.verticalScrollBar():
            self.translated_text.verticalScrollBar().setValue(sender.value())
        elif sender == self.translated_text.verticalScrollBar():
            self.source_text.verticalScrollBar().setValue(sender.value())
    
    def translate_text(self):
        self.show_message("Translating...", 0)
        source_text = self.source_text.toPlainText()
        if self.auto_remove_newlines_button.isChecked():
            source_text = source_text.replace("-\n", '')
            source_text = source_text.replace('\n', ' ')
            source_text = source_text.replace('\r', '')
            self.source_text.setPlainText(source_text)
        translator = GoogleTranslator(source='en', target='cs')
        
        # Split text into sentences
        self.sentences = self.split_into_sentences(source_text)
        translated_start_pos = 0
        for sentence in self.sentences:
            if len(sentence.text) > 4000:
                max_chunk_size = 4000
                chunks = [sentence.text[i:i+max_chunk_size] for i in range(0, len(sentence.text), max_chunk_size)]
                translated_chunks = [translator.translate(chunk) for chunk in chunks]
                sentence.translation = ' '.join(translated_chunks)
            sentence.translation = translator.translate(sentence.text)
            sentence.add_translation_start_pos(translated_start_pos)
            translated_start_pos += len(sentence.translation) + 1
        translated_text = ' '.join([sentence.translation for sentence in self.sentences])
        self.translated_text.setPlainText(translated_text)
        self.show_message("Translation complete.", 1000)
        
        self.source_text.update_sentences(self.sentences)
        self.translated_text.update_sentences(self.sentences)
    
    def split_into_sentences(self, text):
        sentence_endings = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)(?=\s|$)')
        sentences = sentence_endings.split(text)
        start_pos = 0
        sentence_objects = []
        for sentence in sentences:
            sentence_objects.append(Sentence(sentence, start_pos))
            start_pos += len(sentence)
        return sentence_objects

    def toggle_auto_remove_newlines(self):
        if self.auto_remove_newlines_button.isChecked():
            self.auto_remove_newlines_button.setText("Remove newlines Enabled")
        else:
            self.auto_remove_newlines_button.setText("Remove newlines Disabled")

    def delete_source_text(self):
        self.source_text.clear()
        self.source_text.setFocus()
        self.sentences = []

    def copy_source_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.source_text.toPlainText())
        self.show_message("Source text copied to clipboard.", 1000)

    def copy_translated_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.translated_text.toPlainText())
        self.show_message("Translated text copied to clipboard.", 1000)
    
    def show_message(self, message, time):
        self.info_label.setText(message)
        self.info_label.setVisible(True)

        # Set up opacity effect
        self.opacity_effect = QGraphicsOpacityEffect()
        self.info_label.setGraphicsEffect(self.opacity_effect)
        
        # Fade in animation
        self.fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in.setDuration(500)
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(1)
        self.fade_in.start()
        
        if time > 0:
            QTimer.singleShot(time, self.hide_message)
    
    def hide_message(self):
        # Fade out animation
        self.fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out.setDuration(500)
        self.fade_out.setStartValue(1)
        self.fade_out.setEndValue(0)
        self.fade_out.finished.connect(self.info_label.hide)
        self.fade_out.start()
