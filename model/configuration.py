class Configuration(object):
    sampleRateHertz = int()
    audioChannelCount = int()
    enableSeparateRecognitionPerChannel = False
    languageCode = str()
    alternative_language_codes = list()
    model = str()
    useEnhanced = False
    encoding = str()
    boost = 0
    phrases = []
    speech_context_element = {"phrases": phrases, "boost": boost}
    speech_context = [speech_context_element]

    def _set_boost(self, boost):
        self.boost = boost

    def get_boost(self):
        return self.boost

    def _set_phrases(self, phrases):
        self.phrases = phrases

    def _get_phrases(self):
        return self.phrases

    def set_speech_context(self, phrases, boost):
        self._set_phrases(phrases)
        self._set_boost(boost)
        self.speech_context_element['phrases'] = self.phrases
        self.speech_context_element['boost'] = self.boost

    def get_speech_context(self):
        return self.speech_context

    def set_encoding(self, encoding):
        self.encoding = encoding

    def get_encoding(self):
        return self.encoding

    def get_sample_rate_hertz(self):
        return self.sampleRateHertz

    def set_sample_rate_hertz(self, data):
        self.sampleRateHertz = data

    def set_audio_channel_count(self, data):
        self.audioChannelCount = data

    def get_audio_channel_count(self):
        return self.audioChannelCount

    def set_alternative_language_codes(self, data):
        self.alternative_language_codes = data

    def get_alternative_language_codes(self):
        return self.alternative_language_codes

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

    def __str__(self):
        string = f'model: {self.model}, ' \
                f'language_code: {self.languageCode}, ' \
                f'use_enhanced: {self.useEnhanced}, ' \
                f'sample_rate: {self.sampleRateHertz}, ' \
                f'encoding: {self.encoding}, ' \
                f'phrases: {bool(self._get_phrases())}, boost: {self.get_boost()}'

        audio_channel_count = self.get_audio_channel_count()
        if audio_channel_count > 1:
            string += f'enable_sep_channel_rec: {self.enableSeparateRecognitionPerChannel}, ' \
                      f'audio_channels: {self.audioChannelCount}, '
        return string

