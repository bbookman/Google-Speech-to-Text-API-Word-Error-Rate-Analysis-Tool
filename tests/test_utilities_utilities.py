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

def test_is_valid_file_extension_false():
    from utilities.utilities import Utilities
    u = Utilities()
    expected = False
    extension = 'doc'
    result = u.is_valid_file_extension(extension)
    assert result == expected


def test_is_valid_file_extension_true1():
    from utilities.utilities import Utilities
    u = Utilities()
    expected = True
    extension = 'flac'
    result = u.is_valid_file_extension(extension)
    assert result == expected


def test_is_valid_file_extension_true2():
    from utilities.utilities import Utilities
    u = Utilities()
    expected = True
    extension = 'MP3'
    result = u.is_valid_file_extension(extension)
    assert result == expected

def test_is_audio_homogeneous_false():
    from utilities.utilities import Utilities
    u = Utilities()
    test_list = ['hello.wav', 'hello.mp3', 'wow.flac', 'wow.wav', 'test.txt']
    expected = False
    result = u.is_audio_homogeneous(test_list)
    assert result == expected


def test_is_audio_homogeneous_true1():
    from utilities.utilities import Utilities
    u = Utilities()
    test_list = ['hello.wav', 'wow.wav', 'test.txt']
    expected = True
    result = u.is_audio_homogeneous(test_list)
    assert result == expected

def test_is_audio_homogeneous_true2():
    from utilities.utilities import Utilities
    u = Utilities()
    test_list = ['hello.ogg_opus', 'hello.txt']
    expected = True
    result = u.is_audio_homogeneous(test_list)
    assert result == expected
