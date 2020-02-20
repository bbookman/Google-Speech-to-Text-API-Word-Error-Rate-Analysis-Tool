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

def test_update_csv():
    from utilities.io_handler import IOHandler
    from model.configuration import Configuration
    from model.nlp import NLPModel
    import os
    configuration = Configuration()
    nlp_model = NLPModel()
    io = IOHandler()
    result_file_name = io._result_file_name
    io.set_result_path('test_results_path')
    io.write_csv_header()
    expected_uri = 'gs://foo/bar/baz/test.flac'
    expected_lang = 'fr-FR'
    nlp_model.set_apply_stemming(True)
    configuration.set_language_code(expected_lang)
    io.update_csv(expected_uri, configuration, nlp_model)
    full_path = f'{io.get_result_path()}/{result_file_name}'

    with open(full_path, 'r') as file:
        contents = file.read()
        os.remove(full_path)
        assert expected_uri in contents
        assert expected_lang in contents
        assert 'True' in contents


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


def test_write_read_queue1():
    from utilities.io_handler import IOHandler
    import os
    io = IOHandler()
    file = 'queue.txt'
    io.write_queue_file('')
    expected = True
    result = os.path.isfile(file)
    os.path.isfile(file)
    assert result == expected


def test_write_read_queue2():
    from utilities.io_handler import IOHandler
    import os
    io = IOHandler()
    file = 'queue.txt'
    expected = 'root,roll,rock'
    io.write_queue_file(expected)
    result = io.read_queue_file()
    os.remove(file)
    assert result == expected + ','


def test_write_hyp():
    from utilities.io_handler import IOHandler
    import os
    import shutil
    io = IOHandler()
    result_path = 'test_results_path'
    io.set_result_path(result_path)
    file_name = '1234_en_US_phone_call_enhanced.txt'
    expected_text = 'testing 1 2 3'
    io.write_hyp(file_name, expected_text)
    result = os.path.isfile(f'{result_path}/{file_name}')
    expected = True
    assert result == expected
    with open(f'{result_path}/{file_name}', 'r') as f:
        result_text = f.read()

    try:
        shutil.rmtree('/Users/bookmanb/stt/stt_rewrite/tests/test_results_path')
    except BaseException:
        pass #do nothing
    assert result_text == expected_text
