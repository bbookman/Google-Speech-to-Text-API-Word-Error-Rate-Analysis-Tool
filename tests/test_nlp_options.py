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

def test_apply_nlp_options_stem():
    from utilities.nlp_options import NLPOptions
    from model.nlp import NLPModel
    hyp = 'thingy dancing'
    options = NLPOptions()
    model = NLPModel()
    model.set_apply_stemming(True)
    result = options.apply_nlp_options(model, hyp)
    expected = 'thingi danc '
    assert result == expected

def test_apply_nlp_options_stop():
    from utilities.nlp_options import NLPOptions
    from model.nlp import NLPModel
    hyp = 'thingy in the dancing'
    options = NLPOptions()
    model = NLPModel()
    model.set_remove_stop_words(True)
    result = options.apply_nlp_options(model, hyp)
    expected = ' thingy dancing'
    assert result == expected

def test_apply_nlp_options_n2w():
    from utilities.nlp_options import NLPOptions
    from model.nlp import NLPModel
    hyp = '34 567'
    options = NLPOptions()
    model = NLPModel()
    model.set_n2w(True)
    result = options.apply_nlp_options(model, hyp)
    expected = ' thirty-four five hundred and sixty-seven'
    assert result == expected

def test_apply_nlp_options_expand_cont():
    from utilities.nlp_options import NLPOptions
    from model.nlp import NLPModel
    hyp = "isn't can't"
    options = NLPOptions()
    model = NLPModel()
    model.set_expand_contractions(True)
    result = options.apply_nlp_options(model, hyp)
    expected = 'is not cannot'
    assert result == expected

def test_apply_nlp_options_stem_stop():
    from utilities.nlp_options import NLPOptions
    from model.nlp import NLPModel
    hyp = 'thingy dancing in the'
    options = NLPOptions()
    model = NLPModel()
    model.set_apply_stemming(True)
    model.set_remove_stop_words(True)
    result = options.apply_nlp_options(model, hyp)
    expected = 'thingi danc '
    assert result == expected

def test_apply_nlp_options_stem_n2w():
    from utilities.nlp_options import NLPOptions
    from model.nlp import NLPModel
    hyp = 'thingy dancing 4'
    options = NLPOptions()
    model = NLPModel()
    model.set_apply_stemming(True)
    model.set_n2w(True)
    result = options.apply_nlp_options(model, hyp)
    expected = 'thingi danc four '
    assert result == expected

def test_apply_nlp_options_stem_exp():
    from utilities.nlp_options import NLPOptions
    from model.nlp import NLPModel
    hyp = "thingy dancing won't"
    options = NLPOptions()
    model = NLPModel()
    model.set_apply_stemming(True)
    model.set_expand_contractions(True)
    result = options.apply_nlp_options(model, hyp)
    expected = 'thingi danc will not '
    assert result == expected

def test_apply_nlp_options_stop_n2w():
    from utilities.nlp_options import NLPOptions
    from model.nlp import NLPModel
    hyp = "in the 666"
    options = NLPOptions()
    model = NLPModel()
    model.set_remove_stop_words(True)
    model.set_n2w(True)
    result = options.apply_nlp_options(model, hyp)
    expected = ' six hundred sixtysix'
    assert result == expected

def test_apply_nlp_options_n2w_exp():
    from utilities.nlp_options import NLPOptions
    from model.nlp import NLPModel
    hyp = "666 don't"
    options = NLPOptions()
    model = NLPModel()
    model.set_n2w(True)
    model.set_expand_contractions(True)
    result = options.apply_nlp_options(model, hyp)
    expected = ' six hundred and sixty-six do not'
    assert result == expected

def test_apply_nlp_options_stop_n2w_exp():
    from utilities.nlp_options import NLPOptions
    from model.nlp import NLPModel
    hyp = "666 don't in the"
    options = NLPOptions()
    model = NLPModel()
    model.set_n2w(True)
    model.set_expand_contractions(True)
    model.set_remove_stop_words(True)
    result = options.apply_nlp_options(model, hyp)
    expected = ' six hundred sixtysix'
    assert result == expected

def test_apply_nlp_options_stem_n2w_exp():
    from utilities.nlp_options import NLPOptions
    from model.nlp import NLPModel
    hyp = "666 don't in the raining"
    options = NLPOptions()
    model = NLPModel()
    model.set_n2w(True)
    model.set_expand_contractions(True)
    model.set_apply_stemming(True)
    result = options.apply_nlp_options(model, hyp)
    expected = 'six hundr and sixty-six do not in the rain '
    assert result == expected


def test_stem_stop_n2w():
    from utilities.nlp_options import NLPOptions
    from model.nlp import NLPModel
    hyp = "666 don't in the raining"
    options = NLPOptions()
    model = NLPModel()
    model.set_n2w(True)
    model.set_remove_stop_words(True)
    model.set_apply_stemming(True)
    result = options.apply_nlp_options(model, hyp)
    expected = 'six hundr sixtysix nt rain '
    assert result == expected


def test_stem_stop_exp():
    from utilities.nlp_options import NLPOptions
    from model.nlp import NLPModel
    hyp = "don't in the won't didn't isn't raining"
    options = NLPOptions()
    model = NLPModel()
    model.set_expand_contractions(True)
    model.set_remove_stop_words(True)
    model.set_apply_stemming(True)
    result = options.apply_nlp_options(model, hyp)
    expected = 'rain '
    assert result == expected

def test_stem_stop_n2w():
    from utilities.nlp_options import NLPOptions
    from model.nlp import NLPModel
    hyp = "don't in the won't didn't isn't raining 3 6 9"
    options = NLPOptions()
    model = NLPModel()
    model.set_n2w(True)
    model.set_remove_stop_words(True)
    model.set_apply_stemming(True)
    result = options.apply_nlp_options(model, hyp)
    expected = 'nt wo nt nt nt rain three six nine '
    assert result == expected

def test_stem_stop_n2w_exp():
    from utilities.nlp_options import NLPOptions
    from model.nlp import NLPModel
    hyp = "don't in the won't didn't isn't raining 3 6 9"
    options = NLPOptions()
    model = NLPModel()
    model.set_n2w(True)
    model.set_remove_stop_words(True)
    model.set_apply_stemming(True)
    model.set_expand_contractions(True)
    result = options.apply_nlp_options(model, hyp)
    expected = 'rain three six nine '
    assert result == expected

