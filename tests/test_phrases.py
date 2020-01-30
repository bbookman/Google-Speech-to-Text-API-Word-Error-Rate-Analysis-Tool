import pytest

def test_speech_context_init():
    from model.speech_context import SpeechContext

def test_set_phrases():
    from model.speech_context import SpeechContext
    context = SpeechContext()
    context.set_phrases("data")


def test_get_phrases():
    from model.speech_context import SpeechContext
    context = SpeechContext()
    context.get_phrases()

def test_set_then_get_phrases():
    from model.speech_context import SpeechContext
    expected = "data"
    context = SpeechContext()
    context.set_phrases(expected)
    result = context.get_phrases()
    assert expected == result

    
