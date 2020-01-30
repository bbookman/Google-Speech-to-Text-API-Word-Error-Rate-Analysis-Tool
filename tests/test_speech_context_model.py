import pytest

def test_speech_context_exists():
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
    assert result == expected

def test_set_boost():
    from model.speech_context import SpeechContext
    context = SpeechContext()
    context.set_boost(1)

def test_get_boost():
    from model.speech_context import SpeechContext
    context = SpeechContext()
    context.get_boost()

def test_set_then_get_boost():
    from model.speech_context import SpeechContext
    expected = 5
    context = SpeechContext()
    context.set_boost(expected)
    result = context.get_boost()
    assert result == expected

def test_str():
    from model.speech_context import SpeechContext
    expected_phrases = ["hello", "hi"]
    expected_boost = 13
    context = SpeechContext()
    context.boost = expected_boost
    context.phrases = expected_phrases
    result = context.__str__()
    assert isinstance(result, str)
    for item in expected_phrases:
        assert item in result
    assert str(expected_boost) in result