import argparse
import os
import warnings
from utilities.utilities import Utilities
from utilities.cloud_storage import GCS
from utilities.io_handler import IOHandler
from model.configuration import Configuration
from utilities.speech_to_text import SpeechToText

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-cs', '--cloud_store_uri',
                        help="Cloud storage uri where audio and ground truth expected reference transcriptions are stored",
                        type=str, required=True)
    parser.add_argument('-lr', '--local_results_path', required=True, help="Path to store generated results")
    parser.add_argument('-to', '--transcriptions_only', default=False, required=False,
                        help="If specified the only output will be transcripts, no results will be output",
                        action='store_true')
    parser.add_argument('-nw', '--numbers_to_words', default=False, required=False,
                        help="Expands all numerals found in text to words.  Example 101 = one hundered one",
                        action='store_true')
    parser.add_argument('-stem', '--stem', default=False, required=False, action='store_true',
                        help="Apply NLP stemming to all text")
    parser.add_argument('-stop', '--remove_stop_words', default=False, action='store_true',
                        help="Remove stop words from all text")
    parser.add_argument('-ex', '--expand', default=False, action='store_true',
                        help="Expand all contractions.  Example aren't = are not")
    parser.add_argument('-m', '--models', nargs='+', default=['default'],
                        help='Space seperated list of models to evaluate.  Example video phone.  Defaults to "default" model')
    parser.add_argument('-e', '--enhanced', default=False, required=False, action='store_true',
                        help="Use the enhanced phone_call model.  Must specify phone_call model in command line")
    parser.add_argument('-n', '--encoding', required=True,
                        help="Specifies audio encoding type.  See https://cloud.google.com/speech-to-text/docs/encoding#audio-encodings")
    parser.add_argument('-hz', '--sample_rate_hertz', default=48000, type=int, required=False,
                        help="Specifies the sample rate.  Example: 48000")
    parser.add_argument('-l', '--langs', default=['en-US'], nargs='+', required=False,
                        help="Space separated list of language codes.  Each processed seperately.  Example en-AU en-GB")
    parser.add_argument('-alts', '--alternative_languages', default=None, nargs='+', required=False,
                        help="Space separated list of language codes for auto language detection. Example en-IN en-US en-GB")
    parser.add_argument('-p', '--phrase_file', required=False, type=str,
                        help='Path to file containing comma separated phrases')
    parser.add_argument('-b', '--boosts', default=list(), nargs='+', required=False,
                        help=('Space separated list of boost values to evaluate for speech adaptation'))
    parser.add_argument('-ch', '--multi', required=False, type=int,
                        help='Integer indicating the number of channels if more than one')
    args = parser.parse_args()
    cloud_store_uri = args.cloud_store_uri
    local_results_path = args.local_results_path
    only_transcribe = args.transcriptions_only
    numbers_to_words = args.numbers_to_words
    stem = args.stem
    stop = args.remove_stop_words
    expand = args.expand
    models = args.models
    enhance = args.enhanced
    enc = args.encoding
    sample_rate_hertz = args.sample_rate_hertz
    language_codes = args.langs
    phrase_file_path = args.phrase_file
    boosts = [int(i) for i in args.boosts]
    boosts.append(0)
    alternative_language_codes = args.alternative_languages
    encoding = args.encoding

    phrases = list()

    #
    #   Audit phrase file
    #
    if phrase_file_path:
        # validate phrase file exists
        try:
            os.path.isfile(phrase_file_path)
        except FileNotFoundError as e:
            print(f'Phrase file not found at {phrase_file_path}')
            print(e)
        # If phrase file exists, read phrases
        try:
            with open(phrase_file_path, 'r') as file:
                contents = file.read()
                phrases = contents.split()
                if not phrases:
                    raise EOFError(f"No data found in {phrase_file_path} ")
        except IOError as e:
            print(f'Could not open phrases file {phrase_file_path}')
            print(e)

    # if boosts exist, there should be phrases
    if boosts !=[0] and not phrase_file_path:
        raise FileNotFoundError(f'Boosts {boosts} specified, but no phrase file specified.')

    #
    #   Audit enhanced option
    #

    # create enhance run list
    run_enhanced = [False]
    if enhance:
        run_enhanced.append(True)
        models_contain_phone_call_model = [model for model in models if model=='phone_call']
        if not models_contain_phone_call_model:
            warning_string = f'Command line option -e, --enhanced specified but phone_call model not specified in models: {models}. Run will include phone_call model'
            warnings.warn(warning_string)
            models.append('phone_call')

    #
    #   Correctly set multi channel audio_channel_count
    #

    if args.multi:
        audio_channel_count = args.multi
    else:
        audio_channel_count = 1

    # Get list of all files in google cloud storage (gcs) bucket
    gcs = GCS()
    raw_file_list = gcs.get_file_list(cloud_store_uri)

    # Filter file list
    utilities = Utilities()
    filtered_file_list = utilities.filter_files(raw_file_list)
    final_file_list = [utilities.append_uri(cloud_store_uri, file) for file in filtered_file_list]


    # Write queue file if it does not exist
    io_handler = IOHandler()

    if not os.path.isfile('queue.txt'):
        audio_set = utilities.get_audio_set(final_file_list)
        io_handler.write_queue_file(audio_set)

    # Read queue
    queue_string = io_handler.read_queue_file()
    queue = queue_string.split(',')
    queue.remove('')
    # Process Audio
    for audio in queue:
        for model in models:
            for boost in boosts:
                for language_code in language_codes:
                    # Run enhanced option only for phone call model
                    if enhance and model == 'phone_call':
                        enhanced_runs = [True, False]
                    else:
                        enhanced_runs = [False]

                    # Each enhancement option
                    for use_enhanced in enhanced_runs:
                        configuration = Configuration()
                        configuration.set_use_enhanced(use_enhanced)
                        configuration.set_speech_context(phrases, boost)
                        configuration.set_alternative_language_codes(alternative_language_codes)
                        configuration.set_model(model)
                        configuration.set_sample_rate_hertz(sample_rate_hertz)
                        configuration.set_language_code(language_code)
                        configuration.set_encoding(encoding)
                        if audio_channel_count > 1:
                            configuration.set_audio_channel_count(audio_channel_count)
                            configuration.set_enable_separate_recognition_per_channel(True)

                        print('STARTING . . .')
                        print(f'audio: {audio}, {configuration}')
                        speech_to_text = SpeechToText()



                        hyp = speech_to_text.get_hypothesis(audio, configuration)

                        #hyp = speech_to_text.get_hypothesis(audio, configuration)
                        print(hyp)





