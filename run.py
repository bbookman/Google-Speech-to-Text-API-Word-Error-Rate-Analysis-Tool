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
    parser.add_argument('-lr', '--local_results_path', required=True, help="Local path to store generated results")
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
    parser.add_argument('-q', '--random_queue', required=False, action='store_true', help='Replaces default queue.txt with randomly named queue file')
    parser.add_argument('-fake', '--fake_hyp',  required=False, action='store_true', help='Use a fake hypothesis for testing')
    parser.add_argument('-limit', '--limit', required=False, default=None,type= int,  help = 'Limit to X number of audio files')
    parser.add_argument('-nzb', '--no_zeros_boost', required=False,  action='store_true', help='skip boost of 0' )
    parser.add_argument('-single', '--single_word', required=False, action='store_true', help='process each letter rather than whole words')
    parser.add_argument('-lf','--local_files_path', required=False, type=str, help='process local files',  default=None)

    nlp_model = NLPModel()
    io_handler = IOHandler()
    nlp_options = NLPOptions()
    configuration = Configuration()
    # Turn on punctuation ..  why not.. no bearing on WER
    configuration.set_enableAutomaticPunctuation(True)

    args = parser.parse_args()
    no_zeros_for_boost = args.no_zeros_boost
    process_each_letter = args.single_word
    local_files_path = args.local_files_path
    limit = args.limit
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

    if not no_zeros_for_boost:
        boosts.append(0)
    alternative_language_codes = args.alternative_languages
    encoding = args.encoding

    random_queue = args.random_queue
    use_fake_hyp = args.fake_hyp

    # init utilities
    utilities = Utilities()

    #
    #   Audit phrase file
    #
    phrases = list()
    if phrase_file_path:
        phrases = io_handler.read_file(phrase_file_path)

    if phrases:
        if no_zeros_for_boost:
            speech_context_runs = [True]
        else:
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
        models_contain_valid_enhanced = [model for model in models if model == 'phone_call' or model =='video']
        if not models_contain_valid_enhanced:
            warning_string = f'Command line option -e, --enhanced specified however supported model not specified in models: {models}.  Processing will include phone_call and video models'
            warnings.warn(warning_string)
            logger.debug(warning_string)
            models.append('phone_call')
            models.append('video')

    logger.info(f'ENHANCED OPTIONS: {run_enhanced}')

    #
    #   Correctly set multi channel audio_channel_count
    #

    if args.multi:
        audio_channel_count = args.multi
    else:
        audio_channel_count = 1

    logger.info(f'AUDIO CHANNEL COUNT: {audio_channel_count}')

    raw_file_list = list()
    # Get either local files or cloud storage

    #import pdb;pdb.set_trace()
    if not local_files_path:
        # Get list of all files in google cloud storage (gcs) bucket
        gcs = GCS()
        raw_file_list = gcs.get_file_list(cloud_store_uri)
    else:
        raw_file_list = utilities.local_files(local_files_path)

    logger.info(f'RAW FILE LIST: {raw_file_list}')

    # Filter file list
    filtered_file_list = utilities.filter_files(raw_file_list, only_transcribe)

    if not local_files_path:
        final_file_list = [utilities.append_uri(cloud_store_uri, file) for file in filtered_file_list]
    else:
        final_file_list = filtered_file_list

    logger.info(f'FINAL FILE LIST: {final_file_list}')

    
    # if only doing transcriptions, add diarization and punctuation?
    dia = False
    punct = False
    c = None
    if only_transcribe:
        dia = input('Add Diarization Y/N ')
        if dia.lower() == 'y':
            c = input('How many speakers (int) ')
            configuration.set_diarizationSpeakerCount(int(c))
            configuration.set_enableSpeakerDiarization(bool(dia))
        else:
            print('No diarization')
        punct = input('Add Punctuation Y/N? ')
        if punct.lower() == 'y':
            configuration.set_enableAutomaticPunctuation(True)

    audio_set = utilities.get_audio_set(final_file_list)
    audio_list = list()
    if limit:
        count = 0
        while count < limit:
            audio_list.append(audio_set.pop())
            count+=1
        string = f'Limit to {limit} audio files'
        print(string)
        logger.info(string)
    else:
        audio_list = list(audio_set)

    # Prompt for confirmation
    for item in audio_list:
        print(item)
    confirm = input('\nProcess the above audio files (Y/N)? ')
    if confirm.lower() == 'n':
        sys.exit(0)
    else:
        print()

    # if queue file exists, give user option to continue last run
    queue_file_name = io_handler.get_queue_file_name()
    if not random_queue:
        delete_queue = False
        if os.path.isfile(queue_file_name):
            delete_queue = input(
                'Queue file found, continue aborted run (Y/N).  Choosing N will delete existing queue file: ')
            if delete_queue:
                os.remove(queue_file_name)
                print('DELETED: Existing queue.txt')
    else:
        queue_file_name = utilities.create_unique_queue_file_name()
        io_handler.set_queue_file_name(queue_file_name)
        string = f'Random queue file option selected. Queue file: {queue_file_name}'
        print(string)
        logger.debug(string)
        cont = input("Continue Y/N? ")
        if cont.lower() != "y":
            sys.exit()



    io_handler.write_queue_file(audio_set)
    print(f'WRITE: {queue_file_name}\n')

    confirm = input(f'models: {models} \n'
                    f'enhanced: {enhance}\n'
                    f'language: {language_codes}\n'
                    f'alternative language codes: {alternative_language_codes}\n'
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
    print(f'READ: {queue_file_name}')
    queue_string = io_handler.read_queue_file()
    queue = queue_string.split(',')
    queue.remove('')
    logger.info(f'QUEUE: {queue}')



    for model in models:

        if enhance and model == 'phone_call' or enhance and model == 'video':
            enhanced_runs = [True, False]
        else:
            enhanced_runs = [False]

        for use_enhanced in enhanced_runs:
            configuration.set_use_enhanced(use_enhanced)
            if alternative_language_codes:
                alternative_runs = [True, False]
            else:
                alternative_runs = [False]
            for alt_run in  alternative_runs:

                for audio in audio_list:
                    root = utilities.get_root_filename(audio)

                    #read reference
                    if not only_transcribe:
                        msg = f'READING: Reference file {cloud_store_uri}/{root}.txt'
                        print(msg)
                        logger.info(msg)

                    if not local_files_path:
                        ref = gcs.read_ref(cloud_store_uri, root + '.txt')
                    else:
                        ref = io_handler.read_file(local_files_path + '/' + root + '.txt')


                    #for speech_run in speech_context_runs:
                    for boost in boosts:
                        for language in language_codes:
                            if boost > 0:
                                string = f'Running with phrase hints, boost {boost}'
                            else:
                                string = 'No speech context applied'
                            print(string)
                            logger.debug(string)
                            if phrases:
                                configuration.set_speech_context(phrases, boost)
                            else:
                                configuration.set_speech_context([], 0)
                            if alt_run:
                                configuration.set_alternative_language_codes(alternative_language_codes)
                          

                            configuration.set_model(model)
                            configuration.set_sample_rate_hertz(sample_rate_hertz)
                            configuration.set_language_code(language)
                            configuration.set_encoding(encoding)
                            if audio_channel_count > 1:
                                configuration.set_audio_channel_count(audio_channel_count)
                                configuration.set_enable_separate_recognition_per_channel(True)

                            logger.info(f'CONFIGURATION: {configuration}')
                            print(f'STARTING')
                            msg = f'audio: {audio}, {configuration}'
                            logger.info(msg)
                            print(msg)



                            # Generate hyp
                            speech_to_text = SpeechToText()

                            if use_fake_hyp:
                                hyp = 'this is a fake hyp'
                            elif local_files_path:
                                hyp = speech_to_text.transcribe_streaming(audio, configuration)
                            else:
                                hyp = speech_to_text.get_hypothesis(audio, configuration)


                            unique_root = utilities.create_unique_root(root, configuration, nlp_model)
                            io_handler.write_hyp(file_name=unique_root + '.txt', text=hyp)

                            if not only_transcribe:
                                # Calculate WER
                                wer_obj = SimpleWER()
                                hyp = hyp.replace(' ', '')
                                ref = ref.replace(' ', '')

                                if process_each_letter:
                                    hyp = list(hyp)
                                    hyp = ' '.join(hyp)
                                    ref = list(hyp)
                                    ref = ' '.join(ref)

                                wer_obj.AddHypRef(hyp, ref)

                                wer , ref_word_count, ref_error_count, ins, deletions, subs = wer_obj.GetWER()
                                string = f'STATS: wer = {wer}%, ref words = {ref_word_count}, number of errors = {ref_error_count}'
                                print(string)
                                logger.info(string)

                                #Remove hyp/ref from WER
                                wer_obj.AddHypRef('', '')

                                # Get words producing errors
                                inserted_words, deleted_words, substituted_words = wer_obj.GetMissedWords()

                                delete_word_counts = utilities.get_count_of_word_instances(deleted_words)
                                inserted_word_counts = utilities.get_count_of_word_instances(inserted_words)
                                substituted_word_count = utilities.get_count_of_word_instances(substituted_words)
                                word_count_list = (delete_word_counts, inserted_word_counts,  substituted_word_count  )

                                io_handler.write_csv_header()

                                io_handler.update_csv(audio, configuration, NLPModel(),  word_count_list ,
                                                      ref_word_count, ref_error_count, wer, ins, deletions, subs )

                                io_handler.write_html_diagnostic(wer_obj, unique_root, io_handler.get_result_path())

                                #NLP options
                                if nlp_model.get_apply_stemming() or nlp_model.get_remove_stop_words() or nlp_model.get_n2w() or nlp_model.get_expand_contractions():
                                    string = f'STEMMING: {nlp_model.get_apply_stemming()} \n' \
                                             f'REMOVE STOP WORDS: {nlp_model.get_remove_stop_words()} \n' \
                                            f'NUMBERS TO WORDS: {nlp_model.get_n2w()} \n' \
                                            f'EXPAND CONTRACTIONS: {nlp_model.get_expand_contractions()}'
                                    print(string)
                                    logger.debug(string)
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
                                    io_handler.update_csv(audio, configuration, nlp_model,
                                                      ref_word_count, ref_error_count, wer)

    print('Done')
    print('Deleting queue')
    os.remove(queue_file_name)


