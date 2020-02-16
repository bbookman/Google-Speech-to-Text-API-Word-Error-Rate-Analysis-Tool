from model.configuration import Configuration
from model.nlp import NLPModel

class IOHandler(object):
    _result_path = ''
    _result_file_name = 'results.csv'
    _csv_header = 'AUDIO_FILE, MODEL, ENHANCED, LANGUAGE, ALTERNATIVE_LANGS, Reading audio queueASE_HINTS_APPLIED, BOOST, REF_WORD_COUNT, REF_ERROR_COUNT , WER,STEMMING_APPLIED , STOP_WORDS_REMOVED, NUMBER_TO_WORD_CONVERSION, CONTRACTIONS_EXPANDED\n'
    _csv_header_written = False
    configuration = Configuration()
    nlp_model = NLPModel()

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
                   uri,
                    configuration,
                    nlp_model,
                    ref_total_word_count = 0,
                    ref_error_count = 0,
                    word_error_rate =0,
                    ):

        full_path = f'{self.get_result_path()}/{self._result_file_name}'
        string = f'{uri}, {configuration.get_model()}, {configuration.get_use_enhanced()}, {configuration.get_language_code()},' \
                 f' {configuration.get_alternative_language_codes()}, {bool(configuration.get_speech_context())},' \
                 f'{configuration.get_boost()}, {ref_total_word_count}, {ref_error_count}, {word_error_rate}, {nlp_model.get_apply_stemming()},' \
                 f'{nlp_model.get_remove_stop_words()}, {nlp_model.get_n2w()}, {nlp_model.get_expand_contractions()}\n'
        with open(full_path, 'a+',) as file:
            try:
                file.write(string)
            except IOError as i:
                print(f'Can not update csv file: {i}')
        print(f'UPDATED: {full_path}')


    def write_html_diagnostic(self, wer_obj, unique_root, result_path):
        aligned_html = '<br>'.join(wer_obj.aligned_htmls)

        result_file = unique_root + '.html'
        write_path = f'{result_path}/{result_file}'
        with open(write_path, 'w') as f:
            try:
                f.write(aligned_html)
            except IOError as i:
                print(f'Can not write html diagnostic {write_path}: {i}')
        print(f'WROTE: diagnostic file: {write_path} ')

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
            print(f'Can not write diagnostic file: {e}')
        print('WROTE: queue file queue.txt')


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
        return result

    def write_hyp(self, file_name, text):
        import os.path

        if not os.path.exists(self.get_result_path()):
            os.makedirs(self.get_result_path())

        p = f'{self.get_result_path()}/{file_name}'

        with open(p, 'w+') as f:
            f.write(text)
