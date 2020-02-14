class IOHandler(object):
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
                try:
                    file.write(self._csv_header)
                except IOError as i:
                    print(f'Can not write csv header: {i}')
                except FileNotFoundError as x:
                    print(f'Can not find csv file: {x}')
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
            try:
                file.write(string)
            except IOError as i:
                print(f'Can not update csv file: {i}')
        print(f'UPDATED: {full_path}')


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
            try:
                f.write(aligned_html)
            except IOError as i:
                print(f'Can not write html diagnostic {write_path}: {i}')

    def write_queue_file(self, data):
        try:
            with open('queue.txt', 'a+') as f:
                if isinstance(data, str):
                    info = data.split()
                else:
                    info = data
                for item in info:
                    f.write(item + ',')
        except IOError as e:
            print(f'Can not write queue file: {e}')
        print('Writing audio queue')


    def read_queue_file(self):
        result = None
        try:
            with open('queue.txt', 'r') as f:
                result = f.read()
        except IOError as e:
            print(f'Can not read queue file: {e}')
        except FileNotFoundError as x:
            print(f'Queue file not found: {f}')
        if not result:
            raise IOError('No contents found in queue')
        print('Reading audio queue')
        return result

    def write_hyp(self, file_name, text):
        import os.path

        if not os.path.exists(self.get_result_path()):
            os.makedirs(self.get_result_path())

        p = f'{self.get_result_path()}/{file_name}'

        with open(p, 'w+') as f:
            f.write(text)
