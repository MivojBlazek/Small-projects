# Translator App

This is a simple translator application that translates text from English to Czech. It also provides the ability to remove newline characters from copied text to create sentences that are more likely to translate correctly.

This project was primarily designed for reading English literature as part of an Bachelor's final thesis. When text is copied from most pdfs, it is deformed, including adding newline characters after each line in the pdf. This project processes the source text to remove these newlines so that the text can be translated correctly.

## Features

### Main features

- Translate text from English to Czech using Google Translator.
- Highlight sentences in the source text and their corresponding translations.
- Copy source and translated text to the clipboard.
- Automatically remove newline characters from the source text.
- Clear source and translated text.

### Other features

- Removes 1 newline character in text but if there are 2 of them after each other, it stays as a new paragraph.
- If word is wrapped, it will remove `-` character and connect it back together.
- Doesn't translate text in parentheses but only copy it.
- When copying parentheses, some may be missing. This will fill them back in.

## Usage

1. Run the application:
    ```
    python main.py
    ```
    
2. Enter the English text in the left text area.

3. Click the "Translate" button to translate the text to Czech.

4. Use the "Copy" buttons to copy the source or translated text to the clipboard.

5. Use the "Fix source text" button to automatically remove newline characters from the source text (new line characters are removed from translated text for better translations even if it is disabled).

6. Use the "Delete" button to clear the source and translated text.
