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

    def _is_audio_homogeneous(self, file_list):
        extension_set = set()
        for item in file_list:
            # ignore text files
            if 'txt' in item:
                continue
            #get just the file ext
            loc = item.rfind('.')
            candidate = item[loc+1:]
            #create a set of unique file ext
            extension_set.add(candidate)
        # if more than one audio file ext, have a hetero bucket
        if len(extension_set) > 1:
            return False
        return True

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

    def _get_audio_set(self, file_list):
        result = set()
        for file_name in file_list:
            for ext in self.supported_audio_extensions:
                if ext in file_name:
                    result.add(self.get_root_filename(file_name))
        return result

    def _get_ref_set(self, file_list):
        result = set()
        for file_name in file_list:
            if '.txt' in file_name:
                result.add(self.get_root_filename(file_name))
        return result

    def _is_paired(self, text_file_name, file_list):
        # get audio list
        audio_files = self._get_audio_set(file_list)
        txt_root = self.get_root_filename(text_file_name)
        for audio in audio_files:
            if txt_root in audio:
                return True
        return False

    def _get_extension(self, file_name):
        dot_loc = file_name.rfind('.')
        return file_name[dot_loc+1:]

    def are_valid_files(self, file_list):
        # check for valid file extensions
        for file in file_list:
            ext = self._get_extension(file)
            if not self._is_valid_file_extension(ext):
                return False, f'{ext} is not a supported file extension'

        # check all audio same file type
        if not self._is_audio_homogeneous(file_list):
            return False, f'Storage endpoint contains heterogeneous audio, must be homogeneous.  Must contain only one audio file type'

        # check that each audio file has a reference text pair
        audio_set = self._get_audio_set(file_list)
        ref_set = self._get_ref_set(file_list)
        mismatch = audio_set.difference(ref_set)
        if mismatch:
            return False, f'Audio files exist with no paired reference human transcription text files'

        return True, None

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

