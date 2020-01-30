class SpeechContext():
    phrases = []

    def set_phrases(self, data):
        self.phrases = data
        return self.phrases

    def get_phrases(self):
        return self.phrases