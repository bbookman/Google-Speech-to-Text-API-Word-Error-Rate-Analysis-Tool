from model.configuration import Configuration
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types


class SpeechToText(object):
    configuration = Configuration()
    def send_request(self, uri, configuration):
        """Asynchronously transcribes the audio uri specified by the gcs_uri."""
        client = speech.SpeechClient()
        config = types.RecognitionConfig(
            model = configuration.get_model(),
            use_enhanced = configuration.get_use_enhanced(),
            encoding = configuration.get_encoding(),
            sample_rate_hertz = configuration.get_sample_rate_hertz(),
            language_code = configuration.get_language_code(),
            alternative_language_codes = configuration.get_alternative_language_codes(),
            audio_channel_count = configuration.get_audio_channel_count(),
            enable_separate_recognition_per_channel = configuration.get_enable_separate_recognition_per_channel()

        )


        audio = {"uri": uri}
        operation = client.long_running_recognize(config, audio)