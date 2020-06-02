class Utilities():
    supported_audio_extensions = ["flac", "wav", "mp3", "ogg", "oga", "mogg", "opus", "mulaw"]

    def string_to_enum(self, encoding):
        from google.cloud.speech_v1p1beta1 import enums
        result = enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED
        if encoding.upper() == "LINEAR16":
            result = enums.RecognitionConfig.AudioEncoding.LINEAR16
        if encoding.upper() == 'MP3':
            result = enums.RecognitionConfig.AudioEncoding.MP3
        if encoding.upper() == "FLAC":
            result = enums.RecognitionConfig.AudioEncoding.FLAC
        if encoding.upper() == "MULAW":
            result = enums.RecognitionConfig.AudioEncoding.MULAW
        if encoding.upper() == "AMR":
            result = enums.RecognitionConfig.AudioEncoding.AMR
        if encoding.upper() == "AMR_WB":
            result = enums.RecognitionConfig.AudioEncoding.AMR_WB
        if encoding.upper() == "OGG_OPUS":
            result = enums.RecognitionConfig.AudioEncoding.OGG_OPUS
        if encoding.upper() == "SPEEX_WITH_HEADER_BYTE":
            result = enums.RecognitionConfig.AudioEncoding.SPEEX_WITH_HEADER_BYTE

        return result

    def _is_valid_file_extension(self, extension):
        candidate = extension.replace('.', '')

        if candidate.lower() == 'txt':
            return True

        for ext in self.supported_audio_extensions:
            if candidate.lower() == ext:
                return True
        return False

    def get_root_filename(self, uri):
        last_slash = uri.rfind('/')
        if last_slash:
            file_name = uri[last_slash+1:]
        dot_loc = file_name.rfind('.')
        if dot_loc:
            result = file_name[:dot_loc]
        else:
            result = file_name
        return result

    def get_audio_set(self, file_list):
        result = set()
        for file_name in file_list:
            for ext in self.supported_audio_extensions:
                if ext in file_name:
                    result.add(file_name)
        return result

    def _get_ref_set(self, file_list):
        result = set()
        for file_name in file_list:
            if '.txt' in file_name:
                result.add(file_name)
        return result

    def _get_extension(self, file_name):
        dot_loc = file_name.rfind('.')
        return file_name[dot_loc+1:]

    def filter_files(self, files, only_transcribe):
        import copy
        valid_types = list()
        # Remove unsupported file types
        for file in files:
            if self._is_valid_file_extension(self._get_extension(file)):
                valid_types.append(file)
            else:
                print(f'{file} is not supported and will be ignored')

        # If audio is hetero, throw error
        audio_set = self.get_audio_set(valid_types)
        ref_set = self._get_ref_set(valid_types)
        audio_extensions = [self._get_extension(audio) for audio in audio_set]
        if len(set(audio_extensions)) > 1:
            raise FileExistsError(f'Audio files must all be the same file type.  File types on storage:{set(audio_extensions)}')

        # Remove any audio that has no corresponding ref
        audio_roots = [self.get_root_filename(file) for file in audio_set]
        a_root_set = set(audio_roots)
        ref_roots = [self.get_root_filename(file) for file in ref_set]
        r_root_set = set(ref_roots)
        orphan_audio_files = a_root_set.difference(r_root_set)
        orphan_audio_removed = copy.deepcopy(valid_types)
        if orphan_audio_files and not only_transcribe:
            for root in orphan_audio_files:
                for file in valid_types:
                    if root in file:
                        orphan_audio_removed.remove(file)
                        print(f'INFO: audio file {file} does not have corresponding reference file and will be ignored')

        # Remove any reference file that has no corresponding audio file
        orphan_reference_files = r_root_set.difference(a_root_set)
        orphan_referance_removed = copy.deepcopy(orphan_audio_removed)
        if orphan_reference_files:
            for root in orphan_reference_files:
                for file in orphan_audio_removed:
                    if root in file:
                        orphan_referance_removed.remove(file)
                        print(f'INFO: Reference file {file} does not have corresponding audio file and will be ignored')
        return orphan_referance_removed


    def parse_uri(self,uri):
        # if uri = http://hello/world.txt
        # data.scheme = http
        # data.netloc = hello
        # data.path = /world.txt
        # folder = None ' '
        # file = world.txt
        #
        # if uri = gs://foo/bar/baz/hello.wav
        # data.scheme = gs
        # data.netloc = foo
        # data.path = /bar/baz/hello.wav'
        # folder = bar/baz/
        # file = hello.wav
        # scheme, netloc, path, folder, file

        from urllib.parse import urlparse
        data = urlparse(uri)
        ext_in_path = False

        # check for file extension
        for ext in self.supported_audio_extensions:
            if ext not in data.path:
                continue
            else:
                ext_in_path = True
        if 'txt' in data.path:
            ext_in_path = True

        # if there is an extension, there is a file name. get the file name and folder name
        if ext_in_path:
            loc = data.path.rfind("/")
            file = data.path[loc + 1:]
            folder = data.path.replace(file, "")
        else:
            # no file extension, therefore no file name to return, just get the folder
            file = None
            folder = data.path
        # remove leading slash from folder
        if folder.find("/") == 0:
            folder = folder[1:]
            # remove trailing slash from folder
        if folder.rfind("/") == len(folder) - 1:
            folder = folder[:-1]
        return data.scheme, data.netloc, data.path, folder, file


    def append_uri(self, uri, file):
        result = file.replace('/', '')
        slash_loc = uri.rfind('/')
        if slash_loc == len(uri) - 1:
            return uri + file
        return uri + '/' + file

    def create_unique_root(self, root, configuration, nlp_model=None):
        result = root
        result += f'_{configuration.get_model()}'
        language_code = configuration.get_language_code().replace('-', '_')
        result += f'_{language_code}'
        if configuration.get_use_enhanced():
            result+= f'_enhanced'
        if configuration.get_alternative_language_codes():
            result+=f'_alts_applied'
        if configuration.get_speech_context() and configuration.get_boost():
            result+=f'_speech_adaptation_applied'
            result+= f'_boost_{configuration.get_boost()}'
        if nlp_model.get_remove_stop_words():
            result+='_stop_words_removed'
        if nlp_model.get_apply_stemming():
            result+='_stemming_applied'
        if nlp_model.get_expand_contractions():
            result+= '_contractions_expanded'
        if nlp_model.get_n2w():
            result+= '_numbers_converted_2_words'

        return result


    def create_unique_queue_file_name(self):
        from random import seed
        from random import randint
        s = randint(0,100)
        seed(s)
        random_number = randint(1000, 9999)
        return f'queue_{random_number}.txt'

    def get_count_of_word_instances(self, word_list):
        word_set = set(word_list)
        result = dict()
        for word in word_set:
            count = word_list.count(word)
            result[word] = count
        return result



