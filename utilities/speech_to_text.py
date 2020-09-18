from model.configuration import Configuration
from google.cloud import speech_v1p1beta1 as speech
import google
import logging
from utilities.utilities import Utilities

# logging setup
logging.basicConfig(filename='wer_app.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SpeechToText(object):
    configuration = Configuration()
    def get_hypothesis(self, uri, configuration):
        import time
        """Asynchronously transcribes the audio uri specified by the gcs_uri."""
        client = speech.SpeechClient()
        config = {
            "model" : configuration.get_model(),
            "use_enhanced" : configuration.get_use_enhanced(),
            "encoding" : configuration.get_encoding(),
            "sample_rate_hertz" : configuration.get_sample_rate_hertz(),
            "language_code" : configuration.get_language_code(),
            "alternative_language_codes" : configuration.get_alternative_language_codes(),
            "audio_channel_count" : configuration.get_audio_channel_count(),
            "enable_separate_recognition_per_channel" : configuration.get_enable_separate_recognition_per_channel(),
            "enable_speaker_diarization": configuration.get_enableSpeakerDiarization(),
            "diarization_speaker_count": configuration.get_diarizationSpeakerCount(),
            "enable_automatic_punctuation": configuration.get_enableAutomaticPunctuation(),
            "speech_contexts": configuration.get_speech_context()
        }

        utilities = Utilities()
        audio = {"uri": uri}
        operation = object
        try:
            operation = client.long_running_recognize(config, audio)
        except google.api_core.exceptions.InvalidArgument as e:
            raise e
        count = 0
        sleep_time = 5
        while not operation.done() and count != 30000:
            print(f"{operation.metadata.progress_percent}% complete - updates every {sleep_time} seconds")
            if count == 29999:
                raise TimeoutError("Time out processing audio")
            count += 1
            time.sleep(sleep_time)
        print(f"{operation.metadata.progress_percent}% complete - updates every {sleep_time} seconds")

        response = operation.result(timeout=1200)

        transcript = str()
        for result in response.results:
            # First alternative is the most probable result
            transcript += " " + result.alternatives[0].transcript
        if not transcript:
            logger.debug('No transcript returned')
        t = utilities.strip_puc(text= transcript)
        return t.lower()