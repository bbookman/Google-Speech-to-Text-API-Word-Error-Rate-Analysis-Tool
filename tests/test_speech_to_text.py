import pytest

def test_get_hypothesis():
    from model.configuration import Configuration
    from utilities.speech_to_text import SpeechToText
    uri = 'gs://brb/test_audio_n_truth/1.wav'
    configuration_object = Configuration()
    configuration_object.set_language_code('en-US')
    configuration_object.set_encoding('LINEAR16')
    configuration_object.set_sample_rate_hertz(44100)
    configuration_object.set_model('default')
    speech = SpeechToText()
    result = speech.get_hypothesis(uri, configuration_object)
