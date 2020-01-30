class SpeechContext():
    phrases = []
    boost = int()

    def set_phrases(self, data):
        self.phrases = data
        return self.phrases

    def get_phrases(self):
        return self.phrases

    def set_boost(self, data):
        self.boost = data

    def get_boost(self):
        return self.boost