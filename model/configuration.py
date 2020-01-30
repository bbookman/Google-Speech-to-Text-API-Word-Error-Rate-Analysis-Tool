from model.speech_context import SpeechContext

class Configuration(object):
    sampleRateHertz = int()
    audioChannelCount = int()
    enableSeparateRecognitionPerChannel = bool()
    languageCode = str()
    model = str()
    useEnhanced = bool()
    speechContext = SpeechContext()

    def get_sample_rate_hertz(self):
        return self.sampleRateHertz

    def set_sample_rate_hertz(self, data):
        self.sampleRateHertz = data

    def set_audio_channel_count(self, data):
        self.audioChannelCount = data

    def get_audio_channel_count(self):
        return self.audioChannelCount

    def set_enable_separate_recognition_per_channel(self, data):
        self.enableSeparateRecognitionPerChannel = data

    def get_enable_separate_recognition_per_channel(self):
        return self.enableSeparateRecognitionPerChannel

    def set_language_code(self, data):
        self.languageCode = data

    def get_language_code(self):
        return self.languageCode

    def get_model(self):
        return self.model

    def set_model(self, data):
        self.model = data

    def get_use_enhanced(self):
        return self.useEnhanced

    def set_use_enhanced(self, data):
        self.useEnhanced = data

    def get_speech_context(self):
        return self.speechContext

    def set_speech_context(self, phrases, boost):
        self.speechContext.phrases = phrases
        self.speechContext.boost = boost

    def __str__(self):
        return f'model: {self.model}, ' \
                f'language_code: {self.languageCode}, ' \
                f'use_enhanced: {self.useEnhanced}, ' \
                f'sample_rate: {self.sampleRateHertz}, ' \
                f'audio_channels: {self.audioChannelCount}, ' \
                f'enable_sep_channel_rec: {self.enableSeparateRecognitionPerChannel}, ' \
                f'speech_context: [ ' \
                f'      phrases: {self.speechContext.phrases}' \
                f'      boost: {self.speechContext.boost}'

