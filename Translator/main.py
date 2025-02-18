from PyQt6.QtWidgets import QApplication
from translator_app import TranslatorApp

if __name__ == "__main__":
    app = QApplication([])
    window = TranslatorApp()
    window.setWindowTitle("Translator")
    window.show()
    app.exec()
