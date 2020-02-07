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

def test_get_extension_flac():
    from utilities.utilities import Utilities
    u = Utilities()
    expected = 'flac'
    result = u._get_extension('woooooo.flac')
    assert result == expected

def test_is_valid_file_extension_false():
    from utilities.utilities import Utilities
    u = Utilities()
    expected = False
    extension = 'doc'
    result = u._is_valid_file_extension(extension)
    assert result == expected

def test_is_valid_file_extension_true1():
    from utilities.utilities import Utilities
    u = Utilities()
    expected = True
    extension = 'flac'
    result = u._is_valid_file_extension(extension)
    assert result == expected

def test_is_valid_file_extension_true2():
    from utilities.utilities import Utilities
    u = Utilities()
    expected = True
    extension = 'MP3'
    result = u._is_valid_file_extension(extension)
    assert result == expected


def test_get_root_filename_from_uri():
    from utilities.utilities import Utilities
    u = Utilities()
    expected = 'file'
    data = 'gs://foo/bar/baz/file.wav'
    result = u.get_root_filename(data)
    assert result == expected

def test_get_root_filename_from_file_name():
    from utilities.utilities import Utilities
    u = Utilities()
    expected = 'file'
    data = 'file.doc'
    result = u.get_root_filename(data)
    assert result == expected

def test_get_audio_set():
    from utilities.utilities import Utilities
    u = Utilities()
    expected = {'a.wav', 'b.wav', 'c.wav'}
    data = ['a.wav', 'foo.txt', 'c.txt', 'b.wav', 'c.wav', 'a.txt', 'b.txt']
    result = u.get_audio_set(data)
    assert result == expected

def test_get_ref_set():
    from utilities.utilities import Utilities
    u = Utilities()
    expected = {'2.txt', '3.txt'}
    data = ['hello.wav', 'foo.doc', 'bar.flac', '2.txt', '3.txt']
    result = u._get_ref_set(data)
    assert result == expected

def test_filter_files_doc():
    from utilities.utilities import Utilities
    u = Utilities()
    data = ['file.txt', 'hello.doc']
    expected = ['file.txt']
    result = u.filter_files(data)
    assert result == expected

def test_filter_files_homogeneous_audio():
    from utilities.utilities import Utilities
    u = Utilities()
    expected = ['this.flac', 'that.flac', 'other.flac']
    result = u.filter_files(expected)
    assert result == expected

def test_filter_files_orphan_audio():
    from utilities.utilities import Utilities
    u = Utilities()
    data = ['audio.ogg', 'blah.txt', 'blah.ogg']
    expected = ['blah.txt', 'blah.ogg']
    result = u.filter_files(data)
    assert result == expected

def test_filter_files_orphan_ref():
    from utilities.utilities import Utilities
    u = Utilities()
    data = ['blah.txt', 'blah.ogg', 'orphan.txt']
    expected = ['blah.txt', 'blah.ogg']
    result = u.filter_files(data)
    assert result == expected

def test_parse_uri_1():
    from utilities.utilities import Utilities
    u = Utilities()
    uri = 'gs://foo/bar/baz'
    expected_bucket = 'foo'
    expected_folder = 'bar/baz'
    expected_file = None
    result_unused_scheme, result_bucket, result_unused_path, result_folder, result_file  = u.parse_uri(uri)
    assert result_bucket == expected_bucket
    assert result_folder == expected_folder
    assert result_file == expected_file


def test_parse_uri_2():
    from utilities.utilities import Utilities
    u = Utilities()
    uri = 'gs://foo/bar/baz/test.flac'
    expected_bucket = 'foo'
    expected_folder = 'bar/baz'
    expected_file = 'test.flac'
    result_unused_scheme, result_bucket, result_unused_path, result_folder, result_file  = u.parse_uri(uri)
    assert result_bucket == expected_bucket
    assert result_folder == expected_folder
    assert result_file == expected_file
