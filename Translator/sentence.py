class Sentence:
    def __init__(self, text, start_position, translation=None):
        self.text = text
        self.start_position = start_position
        self.translation = translation

    def add_translation_start_pos(self, translation_start_position):
        self.translation_start_position = translation_start_position

    def add_translation(self, translation):
        self.translation = translation
