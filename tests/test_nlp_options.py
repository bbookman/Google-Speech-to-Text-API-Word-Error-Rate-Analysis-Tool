import pytest

def test_nlp_options_init():
    from utilities.nlp_options import NLPOptions
    options = NLPOptions()
    result = options.contractions
    assert isinstance(result, dict)
    for value in result.values():
        assert isinstance(value, str)

def test_expand_contractions_yall():
    from utilities.nlp_options import NLPOptions
    options = NLPOptions()
    expected = "you all"
    data = "y'all"
    result = options.expand_contractions(data)
    assert result == expected

def test_expand_contractions_yall():
    from utilities.nlp_options import NLPOptions
    options = NLPOptions()
    expected = "you all"
    data = "y'all"
    result = options.expand_contractions(data)
    assert result == expected

def test_expand_contractions_isnt():
    from utilities.nlp_options import NLPOptions
    options = NLPOptions()
    expected = "is not"
    data = "isn't"
    result = options.expand_contractions(data)
    assert result == expected

def test_convert_numbers_to_words():
    from utilities.nlp_options import NLPOptions
    options = NLPOptions()
    data = '10'
    expected = ' ten'
    result = options.convert_numbers_to_words(data)
    assert result == expected

def test_remove_stop_words():
    from utilities.nlp_options import NLPOptions
    options = NLPOptions()
    data = "This is the way the world ends, not with a bang but with a whimper"
    expected = " This way world ends bang whimper"
    results = options.remove_stop_words(data)
    assert results == expected

def test_apply_stemming():
    from utilities.nlp_options import NLPOptions
    options = NLPOptions()
    data = 'the quick brown fox jumped over the lazy dog'
    expected = 'the quick brown fox jump over the lazi dog '
    result = options.apply_stemming(data)
    assert result == expected