import pytest

def test_send_request():
    from model.configuration import Configuration
    from utilities.speech_to_text import SpeechToText
    uri = 'gs://brb/test_audio_n_truth/1.wav'
    configuration_object = Configuration()
    configuration_object.set_language_code('en-US')
    configuration_object.set_encoding('LINEAR16')
    configuration_object.set_sample_rate_hertz(44100)
    configuration_object.set_model('default')
    speech = SpeechToText()
    speech.send_request(uri, configuration_object)
