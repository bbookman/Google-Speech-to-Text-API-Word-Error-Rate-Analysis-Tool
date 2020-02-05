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



