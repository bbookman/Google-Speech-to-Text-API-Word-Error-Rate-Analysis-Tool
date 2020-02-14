import pytest


def test_set_result_path():
    from utilities.io_handler import IOHandler
    io = IOHandler()
    io.set_result_path('/this/path')

def test_get_result_path():
    from utilities.io_handler import IOHandler
    io = IOHandler()
    io.get_result_path()

def test_set_get_result_path():
    from utilities.io_handler import IOHandler
    io = IOHandler()
    expected = '/foo/bar/baz'
    io.set_result_path(expected)
    result = io.get_result_path()
    assert result == expected


def test_write_csv_header():
    from utilities.io_handler import IOHandler
    import os
    io = IOHandler()
    result_path = 'test_results_path'
    file_path = f'{result_path}/{io._result_file_name}'
    io.set_result_path(result_path)
    io.write_csv_header()
    expected_file = True
    result_file = os.path.isfile(file_path)
    assert io._csv_header_written
    assert os.path.isdir(result_path)
    os.remove(file_path)
    assert result_file == expected_file


def test_header_written_once():
    from utilities.io_handler import IOHandler
    import os, csv
    io = IOHandler()
    result_path = 'test_results_path'
    file_path = f'{result_path}/{io._result_file_name}'
    io.set_result_path(result_path)
    count = 0
    expected = 1
    while count < 5:
        io.write_csv_header()
        count+=1
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        result = sum(1 for row in reader)
    os.remove(file_path)
    assert result == expected



def test_write_csv_verify_header():
    from utilities.io_handler import IOHandler
    import os, csv
    io = IOHandler()
    result_file_name = io._result_file_name
    io.set_result_path('test_results_path')
    io.write_csv_header()
    full_path = f'{io.get_result_path()}/{result_file_name}'
    expected_header_words = io._csv_header.split()
    with open(full_path, 'r') as file:
        result_header_words = csv.reader(file)

    os.remove(full_path)

def test_update_csv():
    from utilities.io_handler import IOHandler
    import os
    io = IOHandler()
    result_file_name = io._result_file_name
    io.set_result_path('test_results_path')
    io.write_csv_header()
    expected_uri = 'gs://foo/bar/baz/test.flac'
    expected_lang = 'fr-FR'
    expected_boost = '341'
    io.update_csv(uri = expected_uri,
                      model = 'default',
                      use_enhanced=False,
                      apply_stemming = False,
                      remove_stop_words = False,
                      expand_contractions = False,
                      convert_numbers_to_words = False,
                      language_code= expected_lang,
                      alternative_language_codes = None,
                      boost = expected_boost,
                      phrase_hints_in_use = False,
                      ref_total_word_count = 0,
                      ref_error_count = 0,
                      word_error_rate =0, )
    full_path = f'{io.get_result_path()}/{result_file_name}'

    with open(full_path, 'r') as file:
        contents = file.read()
        os.remove(full_path)
        assert expected_uri in contents
        assert expected_boost in contents
        assert expected_lang in contents



def DO_NOT_TST_html_diagnostic_contents():
    from utilities.io_handler import IOHandler
    from utilities.utilities import Utilities
    import os
    hypothesis = 'this is a hyp'
    reference = 'this is a ref'
    html = 'this is a <span style="background-color: greenyellow"><del>hyp</del></span><span style="background-color: yellow">ref </span>'
    expected = html.split()
    u = Utilities()
    io = IOHandler()
    audio_uri = 'gs://foo/bar/baz/test.flac'
    results_path = 'test_results_path'
    io.set_result_path(results_path)
    expected_file_name = u.get_root_filename(audio_uri) + '.html'

    io.write_html_diagnostic(hypothesis, reference, audio_uri, results_path)
    file_path = f'{results_path}/{expected_file_name}'
    with open(file_path, 'r') as f:
        reader = f.read()
        results = reader.split()
        for result in results:
            passed = False
            for item in expected:
                if result in item:
                    passed = True
                    continue
            assert passed == True
    os.remove(file_path)

def test_write_queue_file():
    from utilities.io_handler import IOHandler
    import os
    io = IOHandler()
    txt = 'this_root_audio_file_name, 122345, foobarbaz'
    queue_path = 'queue.txt'
    io.write_queue_file(txt)
    expected = True
    result = os.path.isfile(queue_path)
    os.remove(queue_path)
    assert result == expected


def test_read_queue_file():
    from utilities.io_handler import IOHandler
    io = IOHandler()
    io.read_queue_file()

def test_write_read_queue():
    from utilities.io_handler import IOHandler
    import os
    io = IOHandler()
    file = 'queue.txt'
    io.write_queue_file('')
    expected = True
    result = os.path.isfile(file)
    os.path.isfile(file)
    assert result == expected


def test_write_read_queue():
    from utilities.io_handler import IOHandler
    import os
    io = IOHandler()
    file = 'queue.txt'
    expected = 'root,roll,rock'
    io.write_queue_file(expected)
    result = io.read_queue_file()
    os.remove(file)
    assert result == expected


def test_write_hyp():
    from utilities.io_handler import IOHandler
    import os
    io = IOHandler()
    result_path = 'test_results_path'
    file_name = '1234_en_US_phone_call_enhanced.txt'
    expected_text = 'testing 1 2 3'
    io.write_hyp(file_name, expected_text)
    result = os.path.isfile(f'{result_path}/{file_name}')
    expected = True
    assert result == expected
    with open(f'{result_path}/{file_name}', 'r') as f:
        result_text = f.read()
    assert result_text == expected_text