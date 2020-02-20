import argparse
import os, sys
import warnings
from utilities.utilities import Utilities
from utilities.cloud_storage import GCS
from utilities.io_handler import IOHandler
from model.configuration import Configuration
from utilities.speech_to_text import SpeechToText
from model.nlp import NLPModel
from utilities.nlp_options import NLPOptions
from utilities.wer import SimpleWER
import logging

if __name__ == "__main__":

    #logger setup
    logging.basicConfig(filename='wer_app.log')
    logger = logging.getLogger(__name__)
    logger.setLevel('DEBUG')

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
    parser.add_argument('-a', '--alts2prime', required=False, action='store_true', help='Use each alternative language as a primary language')


    nlp_model = NLPModel()
    io_handler = IOHandler()
    nlp_options = NLPOptions()
    args = parser.parse_args()
    cloud_store_uri = args.cloud_store_uri
    io_handler.set_result_path(args.local_results_path)
    only_transcribe = args.transcriptions_only
    nlp_model.set_n2w(args.numbers_to_words)
    nlp_model.set_apply_stemming(args.stem)
    nlp_model.set_remove_stop_words(args.remove_stop_words)
    nlp_model.set_expand_contractions(args.expand)
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
    a2p = args.alts2prime

    # if a2p, append the alts to the language list
    if a2p:
        for code in alternative_language_codes:
            if code not in language_codes:
                language_codes.append(code)

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

    if phrases:
        speech_context_runs = [False, True]
        logger.info(f'PHRASES: {phrases}')
    else:
        speech_context_runs = [False]
        logger.info('NO SPEECH CONTEXT IN USE')

    # if boosts exist, there should be phrases
    if boosts !=[0] and not phrase_file_path:
        raise FileNotFoundError(f'Boosts {boosts} specified, but no phrase file specified.')

    logger.info(f'BOOSTS: {boosts}')
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

    logger.info(f'ENHANCED OPTIONS: {run_enhanced}')
    #
    #   Correctly set multi channel audio_channel_count
    #

    if args.multi:
        audio_channel_count = args.multi
    else:
        audio_channel_count = 1

    logger.info(f'AUDIO CHANNEL COUNT: {audio_channel_count}')
    # Get list of all files in google cloud storage (gcs) bucket
    gcs = GCS()
    raw_file_list = gcs.get_file_list(cloud_store_uri)
    logger.info(f'RAW STORAGE FILE LIST: {raw_file_list}')
    # Filter file list
    utilities = Utilities()
    filtered_file_list = utilities.filter_files(raw_file_list)
    final_file_list = [utilities.append_uri(cloud_store_uri, file) for file in filtered_file_list]

    logger.info(f'FILE LIST FOR PROCESSING: {final_file_list}')

    for item in final_file_list:
        print(item)
    confirm = input('\n\nProcess the above files (Y/N)? ')
    if confirm.lower() == 'n':
        if os.path.isfile('queue.txt'):
            print('Removing existing queue file')
            os.remove('queue.txt')
        sys.exit(0)
    else:
        print()
        print()

    # if queue file exists, give user option to continue last run
    delete_queue = False
    if os.path.isfile('queue.txt'):
        delete_queue = input(
            'Queue file found, continue aborted run (Y/N).  Choosing N will delete existing queue file: ')
        if delete_queue:
            os.remove('queue.txt')
            print('DELETED: Existing queue.txt')


    audio_set = utilities.get_audio_set(final_file_list)
    io_handler.write_queue_file(audio_set)
    print('WRITE: queue.txt\n')

    confirm = input(f'models: {models} \n'
                    f'enhanced: {enhance}\n'
                    f'language: {language_codes}\n'
                    f'alternative language codes: {alternative_language_codes}\n'
                    f'use alternative language codes as primary: {a2p}\n'
                    f'encoding: {encoding}\n'
                    f'sample rate: {sample_rate_hertz}\n'
                    f'audio channels: {audio_channel_count}\n'
                    f'speech context: {bool(phrases)}, boosts: {boosts}\n'
                    f'expand numbers to words: {nlp_model.get_n2w()}\n'
                    f'remove stop words: {nlp_model.get_remove_stop_words()}\n'
                    f'expand contractions: {nlp_model.expand_contractions}\n'
                    f'apply stemming: {nlp_model.get_apply_stemming()}\n\n'
                    'All settings correct (Y/N)? ')
    if not confirm.lower() == 'y':
        sys.exit()
    else:
        print()
        print()

    # Read queue
    print('READ: queue.txt')
    queue_string = io_handler.read_queue_file()
    queue = queue_string.split(',')
    queue.remove('')
    logger.info(f'QUEUE: {queue}')
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
                        for run in speech_context_runs:
                            configuration = Configuration()
                            configuration.set_use_enhanced(use_enhanced)
                            if run:
                                configuration.set_speech_context(phrases, boost)
                            configuration.set_alternative_language_codes(alternative_language_codes)
                            configuration.set_model(model)
                            configuration.set_sample_rate_hertz(sample_rate_hertz)
                            configuration.set_language_code(language_code)
                            configuration.set_encoding(encoding)
                            if audio_channel_count > 1:
                                configuration.set_audio_channel_count(audio_channel_count)
                                configuration.set_enable_separate_recognition_per_channel(True)



                            logger.info(f'CONFIGURATION: {configuration}')
                            print(f'STARTING')
                            msg = f'audio: {audio}, {configuration}'
                            logger.info(msg)
                            print(msg)

                            # Read reference
                            root = utilities.get_root_filename(audio)
                            msg = f'READING: Reference file {cloud_store_uri}/{root}.txt'
                            print(msg)
                            logger.info(msg)

                            ref = gcs.read_ref(cloud_store_uri, root + '.txt')

                            # Generate hyp
                            speech_to_text = SpeechToText()

                            hyp = speech_to_text.get_hypothesis(audio, configuration)

                            unique_root = utilities.create_unique_root(root, configuration, nlp_model)
                            io_handler.write_hyp(file_name=unique_root + '.txt', text=hyp)


                            # Calculate WER
                            wer_obj = SimpleWER()
                            wer_obj.AddHypRef(hyp, ref)
                         
                            wer , ref_word_count, ref_error_count, ins, deletions, subs = wer_obj.GetWER()
                            string = f'STATS: wer = {wer}, ref words = {ref_word_count}, number of errors = {ref_error_count}'
                            print(string)
                            logger.info(string)

                            #Remove hyp/ref from WER
                            wer_obj.AddHypRef('', '')

                            # Get words producing errors
                            inserted_words, deleted_words, substituted_words = wer_obj.GetMissedWords()

                            ###
                            #       debug
                            #
                            ###

                            print(f'inserted words: {inserted_words}')
                            print(f'deleted words: {deleted_words}')
                            print(f'sub words: {substituted_words}')

                            ###########

                            # Get counts
                            delete_word_counts = utilities.get_count_of_word_instances(deleted_words)
                            inserted_word_counts = utilities.get_count_of_word_instances(inserted_words)
                            substituted_word_count = utilities.get_count_of_word_instances(substituted_words)


                            # Write results
                            io_handler.write_csv_header()
                            io_handler.update_csv(cloud_store_uri, configuration, nlp_model,
                                                  ref_word_count, ref_error_count, wer, ins, deletions, subs )

                            io_handler.write_html_diagnostic(wer_obj, unique_root, io_handler.get_result_path())

                            #NLP options
                            if nlp_model.get_apply_stemming() or nlp_model.get_remove_stop_words() or nlp_model.get_n2w() or nlp_model.get_expand_contractions():
                                # Get NLP results
                                nlp_result = nlp_options.apply_nlp_options(nlp_model, hyp)

                                # Get WER
                                wer_obj.AddHypRef(nlp_result, ref)
                                # return round(wer, 2), nref, total_error, self.wer_info['ins'], self.wer_info['del'], self.wer_info['sub']
                                wer, ref_word_count, ref_error_count, ins, deletions, subs = wer_obj.GetWER()
                                string = f'stop: {nlp_model.get_remove_stop_words()}, stem: {nlp_model.get_apply_stemming()}, n2w: {nlp_model.get_n2w()}, exp: {nlp_model.get_expand_contractions()}'
                                print(string)
                                logger.info(string)
                                string = f'STATS: wer = {wer}, ref words = {ref_word_count}, number of errors = {ref_error_count}'
                                print(string)
                                logger.info(string)

                                # Write hyp
                                unique_root = utilities.create_unique_root(root, configuration, nlp_model)
                                io_handler.write_hyp(file_name=unique_root + '.txt', text=nlp_result)

                                # Write diagnostic

                                io_handler.write_html_diagnostic(wer_obj, unique_root, io_handler.get_result_path())

                                # Update csv
                                io_handler.update_csv(cloud_store_uri, configuration, nlp_model,
                                                  ref_word_count, ref_error_count, wer)

    print('Done')
    print('Deleting queue')
    os.remove('queue.txt')




