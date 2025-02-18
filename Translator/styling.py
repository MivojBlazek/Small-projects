from PyQt6.QtWidgets import QPushButton, QTextEdit, QLabel

def style_button(button: QPushButton, type: str):
    if type == "main":
        button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
    elif type == "copy":
        button.setStyleSheet("""
            QPushButton {
                background-color: #008CBA;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 8px;
                max-width: 70px;
            }
            QPushButton:hover {
                background-color: #007bb5;
            }
        """)
    elif type == "delete":
        button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
    elif type == "feature":
        button.setStyleSheet("""
            QPushButton {
                background-color: #e7e7e7;
                color: black;
                border: none;
                padding: 10px 20px;
                text-align: center;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #d6d6d6;
            }
        """)

def style_text_edit(text_edit: QTextEdit):
    text_edit.setStyleSheet("""
        QTextEdit {
            border: 1px solid #ccc;
            padding: 10px;
            font-size: 16px;
        }
    """)
    
def style_info_text(label: QLabel):
    label.setStyleSheet("""
        QLabel {
            width: 100%;
            font-size: 16px;
            color: white;
            background-color: #8C8F80;
            padding: 10px;
            border-radius: 5px;
        }
    """)