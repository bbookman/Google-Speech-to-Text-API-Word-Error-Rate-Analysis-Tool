from model.configuration import Configuration
from model.nlp import NLPModel

class IOHandler(object):
    _result_path = ''
    _result_file_name = 'results.csv'
    _csv_header_written = False
    configuration = Configuration()
    nlp_model = NLPModel()
    _queue_file_name = 'queue.txt'

    def set_queue_file_name(self, name):
        self._queue_file_name = name

    def get_queue_file_name(self):
        return self._queue_file_name

    def set_result_path(self, result_path):
        self._result_path = result_path

    def get_result_path(self):
        return self._result_path

    def write_csv_header(self, configuration, nlp_model):
        import os

        csv_header = 'WER, AUDIO_FILE, MODEL,'
        if configuration.get_use_enhanced():
            csv_header+= 'ENHANCED,'
        csv_header+= 'LANGUAGE,'
        if configuration.get_alternative_language_codes():
            csv_header+= 'ALTERNATIVE_LANGS,'
        if configuration.get_phrases():
            csv_header+= 'PHRASE_HINTS_APPLIED,'
        if configuration.get_boost():
            csv_header+= 'BOOST,'

        csv_header+= 'REF_WORD_COUNT, REF_ERROR_COUNT ,'
        if nlp_model.get_apply_stemming():
            csv_header+= 'STEMMING_APPLIED ,'
        if nlp_model.get_remove_stop_words():
            csv_header += 'STOP_WORDS_REMOVED,'
        if nlp_model.get_n2w():
            csv_header += 'NUMBER_TO_WORD_CONVERSION,'
        if nlp_model.get_expand_contractions():
            csv_header += 'CONTRACTIONS_EXPANDED,'
        csv_header+= 'INSERTIONS, DELETIONS, SUBSTITUTIONS, DELETED_WORDS, INSERTED_WORDS, SUBSTITUTE_WORDS\n'


        if not self._csv_header_written:
            full_path = f'{self.get_result_path()}/{self._result_file_name}'
            # if path does not exists, make it
            if not os.path.exists(self.get_result_path()):
                os.makedirs(self.get_result_path())

            with open(full_path, 'w') as file:
                try:
                    file.write(csv_header)
                except IOError as i:
                    print(f'Can not write csv header: {i}')
                except FileNotFoundError as x:
                    print(f'Can not find csv file: {x}')
            self._csv_header_written = True

    def update_csv(self, word_error_rate, uri, configuration, nlp_model, word_count_list =None ,ref_total_word_count = 0, ref_error_count = 0,  ins=0, deletions=0, subs=0 ):
        import logging
        logging.basicConfig(filename='wer_app.log')
        logger = logging.getLogger(__name__)
        from collections import OrderedDict
        deleted_words_dict = dict()
        inserted_words_dict = dict()
        substitute_words_dict = dict()

        if word_count_list:
            try:
                deleted_words_dict  = OrderedDict(sorted(word_count_list[0].items(), key=lambda x: x[1]))
                inserted_words_dict  = OrderedDict(sorted(word_count_list[1].items(), key=lambda x: x[1]))
                substitute_words_dict = OrderedDict(sorted(word_count_list[2].items(), key=lambda x: x[1]))
            except TypeError as t:
                string = f'{t}'
                logger.debug(string)
                print(string)
                deleted_words_dict = None
                inserted_words_dict = None
                substitute_words_dict = None
        deleted_words = ''
        inserted_words = ''
        substitute_words = ''
        if deleted_words_dict:
            for k, v in deleted_words_dict.items():
                deleted_words+= f'{k}:{v}, '
        if inserted_words_dict:
            for k, v in inserted_words_dict.items():
                inserted_words+=  f'{k}:{v}, '
        if substitute_words_dict:
            for k, v in substitute_words_dict.items():
                substitute_words+=  f'{k}:{v}, '
        full_path = f'{self.get_result_path()}/{self._result_file_name}'

        string = f'{word_error_rate},{uri}, {configuration.get_model()}, '
        if configuration.get_use_enhanced():
            string += 'ENHANCED,'

        string+= f'{configuration.get_language_code()},'

        if configuration.get_alternative_language_codes():
            alts = ''
            for item in (configuration.get_alternative_language_codes()):
                alts += item + ' '
            string += f'{alts},'
        if bool(configuration.get_phrases()):
            string += f'{bool(configuration.get_phrases())},'
        if configuration.get_boost() is not None:
            string += f'{configuration.get_boost()},'
        string+= f'{ref_total_word_count}, {ref_error_count},'
        if nlp_model.get_apply_stemming():
            string+=  f'{nlp_model.get_apply_stemming()},'
        if nlp_model.get_remove_stop_words():
            string += f'{nlp_model.get_remove_stop_words()},'
        if nlp_model.get_n2w():
            string += f'{nlp_model.get_n2w()},'
        if nlp_model.get_expand_contractions():
            string+=f'{nlp_model.get_expand_contractions()},'
        string+= f'{ins}, {deletions}, {subs}, ' \
                 f'{deleted_words}, {inserted_words}, {substitute_words}\n'
        with open(full_path, 'a+',) as file:
            try:
                file.write(string)
            except IOError as i:
                print(f'Can not update csv file: {i}')
        print(f'UPDATED: {full_path}')


    def write_html_diagnostic(self, wer_obj, unique_root, result_path):
        aligned_html = '<br>'.join(wer_obj.aligned_htmls)
        aligned_html += '<h1>KEY</h1>'
        aligned_html += """<span style="background-color: lightgreen">
                MATCH</span> | """
        aligned_html += """<span style="background-color: aqua">
        INSERTION</span> | """
        aligned_html += """<span style="background-color: red">DELETION</span> | """
        aligned_html += """<span style="background-color: orange">API</span> <span style="background-color: yellow">EXPECTED</span> (SUBSTITUTION)"""

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
            with open(self._queue_file_name, 'a+') as f:
                if isinstance(data, str):
                    info = data.split()
                else:
                    info = data
                for item in info:
                    f.write(item + ',')
        except IOError as e:
            print(f'Can not write diagnostic file: {e}')


    def read_queue_file(self):
        result = None
        try:
            with open(self._queue_file_name, 'r') as f:
                result = f.read()
        except IOError as e:
            print(f'Can not read queue file: {e}')
        except FileNotFoundError as x:
            print(f'Queue file not found: {x}')
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

    def read_file(self, file_path):
        import os
        try:
            os.path.isfile(file_path)
        except FileNotFoundError as e:
            print(f'File not found at {file_path}')
            print(e)
        # If phrase file exists, read phrases
        try:
            with open(file_path, 'r',  encoding='latin-1') as file:
                contents = file.read()
                result = contents.split()
                if not result:
                    raise EOFError(f"No data found in {file_path} ")
        except IOError as e:
            print(f'Could not open file {file_path}')
            raise
        result = ''.join(result)
        return result