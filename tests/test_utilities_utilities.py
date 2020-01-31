import pytest

def test_string_to_enum_unspecified():
    from utilities.utilities import Utilities
    from google.cloud.speech_v1p1beta1 import enums
    u = Utilities()
    expected = enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED
    txt = ''
    result = u.string_to_enum(txt)
    assert result == expected

def test_string_to_enum_mulaw():
    from utilities.utilities import Utilities
    from google.cloud.speech_v1p1beta1 import enums
    u = Utilities()
    expected = enums.RecognitionConfig.AudioEncoding.MULAW
    txt = 'MULAW'
    result = u.string_to_enum(txt)
    assert result == expected

def test_string_to_enum_mp3():
    from utilities.utilities import Utilities
    from google.cloud.speech_v1p1beta1 import enums
    u = Utilities()
    expected = enums.RecognitionConfig.AudioEncoding.MP3
    txt = 'mp3'
    result = u.string_to_enum(txt)
    assert result == expected

def test_string_to_enum_flac():
    from utilities.utilities import Utilities
    from google.cloud.speech_v1p1beta1 import enums
    u = Utilities()
    expected = enums.RecognitionConfig.AudioEncoding.FLAC
    txt = 'FLAC'
    result = u.string_to_enum(txt)
    assert result == expected

def test_string_to_enum_amr():
    from utilities.utilities import Utilities
    from google.cloud.speech_v1p1beta1 import enums
    u = Utilities()
    expected = enums.RecognitionConfig.AudioEncoding.AMR
    txt = 'amr'
    result = u.string_to_enum(txt)
    assert result == expected

def test_string_to_enum_amr_wb():
    from utilities.utilities import Utilities
    from google.cloud.speech_v1p1beta1 import enums
    u = Utilities()
    expected = enums.RecognitionConfig.AudioEncoding.AMR_WB
    txt = 'amr_WB'
    result = u.string_to_enum(txt)
    assert result == expected

def test_string_to_enum_ogg_opus():
    from utilities.utilities import Utilities
    from google.cloud.speech_v1p1beta1 import enums
    u = Utilities()
    expected = enums.RecognitionConfig.AudioEncoding.OGG_OPUS
    txt = 'OGG_opus'
    result = u.string_to_enum(txt)
    assert result == expected

def test_string_to_enum_speex_with_header_byte():
    from utilities.utilities import Utilities
    from google.cloud.speech_v1p1beta1 import enums
    u = Utilities()
    expected = enums.RecognitionConfig.AudioEncoding.SPEEX_WITH_HEADER_BYTE
    txt = 'SPEEX_WITH_HEADER_BYTE'
    result = u.string_to_enum(txt)
    assert result == expected
