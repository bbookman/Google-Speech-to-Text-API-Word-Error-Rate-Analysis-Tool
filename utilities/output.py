class Writer(object):
    _result_path = ''
    _result_file_name = 'results.csv'
    _csv_header = 'AUDIO_FILE, MODEL, ENHANCED, LANGUAGE, ALTERNATIVE_LANGS, PHRASE_HINTS_APPLIED, BOOST, REF_WORD_COUNT, REF_ERROR_COUNT , WER,STEMMING_APPLIED , STOP_WORDS_REMOVED, NUMBER_TO_WORD_CONVERSION, CONTRACTIONS_EXPANDED\n'

    _csv_header_written = False

    def set_result_path(self, result_path):
        self._result_path = result_path

    def get_result_path(self):
        return self._result_path

    def write_csv_header(self):
        import os
        if not self._csv_header_written:
            full_path = f'{self.get_result_path()}/{self._result_file_name}'
            # if path does not exists, make it
            if not os.path.exists(self.get_result_path()):
                os.makedirs(self.get_result_path())

            with open(full_path, 'w') as file:
                file.write(self._csv_header)
            self._csv_header_written = True

    def update_csv(self,
                   uri = '',
                   model = 'default',
                   use_enhanced=False,
                   apply_stemming = False,
                   remove_stop_words = False,
                   expand_contractions = False,
                   convert_numbers_to_words = False,
                   language_code= 'en-US',
                   alternative_language_codes = None,
                   boost = 0,
                   phrase_hints_in_use = False,
                   ref_total_word_count = 0,
                   ref_error_count = 0,
                   word_error_rate =0,
                   ):
        full_path = f'{self.get_result_path()}/{self._result_file_name}'
        string = f'{uri}, {model}, {use_enhanced}, {language_code}, {bool(alternative_language_codes)}, {phrase_hints_in_use},' \
                 f'{boost}, {ref_total_word_count}, {ref_error_count}, {word_error_rate}, {apply_stemming},' \
                 f'{remove_stop_words}, {convert_numbers_to_words}, {expand_contractions}\n'
        with open(full_path, 'a+',) as file:
            file.write(string)

    def write_html_diagnostic(self, hypothesis, reference, audio_file, result_path):
        from utilities.utilities import Utilities
        from utilities.wer import SimpleWER
        wer_obj = SimpleWER()
        wer_obj.AddHypRef(hypothesis, reference)
        aligned_html = '<br>'.join(wer_obj.aligned_htmls)
        u = Utilities()
        root = u.get_root_filename(audio_file)
        result_file = root + '.html'
        write_path = f'{result_path}/{result_file}'
        with open(write_path, 'w') as f:
            f.write(aligned_html)
