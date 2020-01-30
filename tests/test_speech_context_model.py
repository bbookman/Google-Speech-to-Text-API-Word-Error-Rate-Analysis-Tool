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

"""def test_context_init():
    from model.speech_context import SpeechContext
    expected_phrases = ["hello","hi"]
    expected_boost = 13
    import pdb; pdb.set_trace()
    context = SpeechContext(expected_phrases, expected_boost)
    result_phrases = context.phrases
    result_boost = context.boost
    assert result_boost == expected_boost
    assert result_phrases == expected_phrases
"""

def test_str():
    from model.speech_context import SpeechContext
    expected_phrases = ["hello", "hi"]
    expected_boost = 13
    context = SpeechContext()
    context.boost = expected_boost
    context.phrases = expected_phrases
    assert isinstance(context.__str__(), str)