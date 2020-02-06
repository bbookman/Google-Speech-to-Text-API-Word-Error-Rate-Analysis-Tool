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

def test_get_extension():
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

def test_is_audio_homogeneous_false():
    from utilities.utilities import Utilities
    u = Utilities()
    test_list = ['gs://hello.wav', 'gs://foo/bar/baz/hello.mp3', 'wow.flac', 'wow.wav', 'test.txt']
    expected = False
    result = u._is_audio_homogeneous(test_list)
    assert result == expected

def test_is_audio_homogeneous_true1():
    from utilities.utilities import Utilities
    u = Utilities()
    test_list = ['gs://foo/hello.wav', 'gs://foo/bar/wow.wav', 'test.txt']
    expected = True
    result = u._is_audio_homogeneous(test_list)
    assert result == expected

def test_is_audio_homogeneous_true2():
    from utilities.utilities import Utilities
    u = Utilities()
    test_list = ['hello.ogg_opus', 'hello.txt']
    expected = True
    result = u._is_audio_homogeneous(test_list)
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
    expected = {'a', 'b', 'c'}
    data = ['a.wav', 'foo.txt', 'c.txt', 'b.wav', 'c.wav', 'a.txt', 'b.txt']
    result = u._get_audio_set(data)
    assert result == expected

def test_get_ref_set():
    from utilities.utilities import Utilities
    u = Utilities()
    expected = {'1', '2', '3'}
    data = ['hello.wav', 'gs://blah/1.txt', 'foo.doc', 'bar.flac', '3.txt', '2.txt']
    result = u._get_ref_set(data)
    assert result == expected

def test_is_paired_false():
    from utilities.utilities import Utilities
    u = Utilities()
    expected = False
    txt_file = 'gs://baz/fred.txt'
    all_files = ['bar.wav', 'gs://baz/fred.txt', 'baz.txt', 'zed.ogg', 'foo.raw']
    result = u._is_paired(txt_file, all_files)
    assert result == expected

def test_is_paired_true():
    from utilities.utilities import Utilities
    u = Utilities()
    expected = True
    txt_file = 'fred.txt'
    all_files = ['bar.wav', 'fred.txt', 'baz.txt', 'fred.flac', 'zed.ogg', 'foo.raw']
    result = u._is_paired(txt_file, all_files)
    assert result == expected

def test_validate_files_false1():
    from utilities.utilities import Utilities
    u = Utilities()
    expected_bool = False
    file_list = ['bar.wav', 'fred.txt', 'baz.txt', 'gs://fooo/baaar/fred.flac', 'zed.ogg', 'foo.raw']
    result_bool, result_string = u.are_valid_files(file_list)
    assert result_bool == expected_bool
    assert isinstance(result_string, str)

def test_validate_files_false2_invalid_extension():
    from utilities.utilities import Utilities
    u = Utilities()
    expected_bool = False
    expected_string = 'extension'
    file_list = ['bar.wav', 'fred.txt', 'baz.txt', 'fred.flac', 'zed.ogg', 'foo.raw']
    result_bool, result_string = u.are_valid_files(file_list)
    assert result_bool == expected_bool
    assert expected_string in result_string

def test_validate_files_false3_hetero():
    from utilities.utilities import Utilities
    u = Utilities()
    expected_bool = False
    expected_string = 'heterogeneous'
    file_list = ['bar.wav', 'fred.txt', 'baz.txt', 'fred.flac', 'gs://sponge_bob/zed.ogg', ]
    result_bool, result_string = u.are_valid_files(file_list)
    assert result_bool == expected_bool
    assert expected_string in result_string

def test_validate_files_false4_no_pair():
    from utilities.utilities import Utilities
    u = Utilities()
    expected_bool = False
    expected_string = 'paired'
    file_list = ['gs://flintstone/fred.txt', 'fred.wav', 'wilma.wav', 'betty.wav', 'betty.txt']
    result_bool, result_string = u.are_valid_files(file_list)
    assert result_bool == expected_bool
    assert expected_string in result_string

def test_validate_files_true():
    from utilities.utilities import Utilities
    u = Utilities()
    expected_bool = True
    expected_string = None
    file_list = ['a.txt', 'a.wav', 'zxy.wav', 'zxy.txt']
    result_bool, result_string = u.are_valid_files(file_list)
    assert result_string == expected_string

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

