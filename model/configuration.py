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
    enableAutomaticPunctuation = False
    enableSpeakerDiarization = False
    diarizationSpeakerCount = 0


    def set_enableAutomaticPunctuation(self, setting):
        self.enableAutomaticPunctuation = setting
    def get_enableAutomaticPunctuation(self):
        return self.enableAutomaticPunctuation

    def set_enableSpeakerDiarization(self, setting):
        self.enableSpeakerDiarization == setting

    def get_enableSpeakerDiarization(self):
        return self.enableSpeakerDiarization
    def set_diarizationSpeakerCount(self, count):
        self.diarizationSpeakerCount = count
    def get_diarizationSpeakerCount(self):
        return self.diarizationSpeakerCount

    def _set_boost(self, boost):
        self.boost = boost

    def get_boost(self):
        return self.boost

    def set_phrases(self, phrases):
        self.phrases = phrases

    def get_phrases(self):
        return self.phrases

    def set_speech_context(self, phrases, boost):
        self.set_phrases(phrases)
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
        string = f'model: {self.model}\n' \
                f'language_code: {self.languageCode}\n' \
                f'use_enhanced: {self.useEnhanced}\n' \
                f'sample_rate: {self.sampleRateHertz}\n' \
                f'encoding: {self.encoding}\n' \
                f'channel count: {self.audioChannelCount} \n' \
                f'phrases: {bool(self.get_phrases())}\n' \
                f'boost:{self.get_boost()}'

        audio_channel_count = self.get_audio_channel_count()
        if audio_channel_count > 1:
            string += f'enable_sep_channel_rec: {self.enableSeparateRecognitionPerChannel}, ' \
                      f'audio_channels: {self.audioChannelCount}, '
        return string

