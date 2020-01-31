class Utilities():
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
