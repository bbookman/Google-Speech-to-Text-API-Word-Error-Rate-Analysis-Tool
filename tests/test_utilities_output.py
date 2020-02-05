import pytest


def test_set_result_path():
    from utilities.output import Writer
    writer = Writer()
    writer.set_result_path('/this/path')

def test_get_result_path():
    from utilities.output import Writer
    writer = Writer()
    writer.get_result_path()

def test_set_get_result_path():
    from utilities.output import Writer
    writer = Writer()
    expected = '/foo/bar/baz'
    writer.set_result_path(expected)
    result = writer.get_result_path()
    assert result == expected


def test_write_csv_header():
    from utilities.output import Writer
    import os
    writer = Writer()
    result_path = 'test_results_path'
    file_path = f'{result_path}/{writer._result_file_name}'
    writer.set_result_path(result_path)
    writer.write_csv_header()
    assert writer._csv_header_written
    assert os.path.isdir(result_path)
    assert os.path.isfile(file_path)
    os.remove(file_path)

def test_header_written_once():
    from utilities.output import Writer
    import os, csv
    writer = Writer()
    result_path = 'test_results_path'
    file_path = f'{result_path}/{writer._result_file_name}'
    writer.set_result_path(result_path)
    count = 0
    expected = 1
    while count < 5:
        writer.write_csv_header()
        count+=1
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        result = sum(1 for row in reader)
    assert result == expected
    os.remove(file_path)


def test_write_csv_verify_header():
    from utilities.output import Writer
    import os, csv
    writer = Writer()
    result_file_name = writer._result_file_name
    writer.set_result_path('test_results_path')
    writer.write_csv_header()
    full_path = f'{writer.get_result_path()}/{result_file_name}'
    expected_header_words = writer._csv_header.split()
    with open(full_path, 'r') as file:
        result_header_words = csv.reader(file)

    os.remove(full_path)

def test_update_csv():
    from utilities.output import Writer
    import os
    writer = Writer()
    result_file_name = writer._result_file_name
    writer.set_result_path('test_results_path')
    writer.write_csv_header()
    expected_uri = 'gs://foo/bar/baz/test.flac'
    expected_lang = 'fr-FR'
    expected_boost = '341'
    writer.update_csv(uri = expected_uri,
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
    full_path = f'{writer.get_result_path()}/{result_file_name}'

    with open(full_path, 'r') as file:
        contents = file.read()
        assert expected_uri in contents
        assert expected_boost in contents
        assert expected_lang in contents
    os.remove(full_path)


def test_html_diagnostic_contents():
    from utilities.output import Writer
    from utilities.utilities import Utilities
    import os
    hypothesis = 'this is a hyp'
    reference = 'this is a ref'
    html = 'this is a <span style="background-color: greenyellow"><del>hyp</del></span><span style="background-color: yellow">ref </span>'
    expected = html.split()
    u = Utilities()
    writer = Writer()
    audio_uri = 'gs://foo/bar/baz/test.flac'
    results_path = 'test_results_path'
    writer.set_result_path(results_path)
    expected_file_name = u.get_root_filename(audio_uri) + '.html'

    writer.write_html_diagnostic(hypothesis, reference, audio_uri, results_path)
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
