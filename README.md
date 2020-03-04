# Google Speech to Text API Word Error Rate Analysis Tool
[Google Cloud Speech to Text API](https://cloud.google.com/speech-to-text/) offers a number of models and options.  This program is designed to help determine the API options that provide the lowest [Word Error Rate](https://en.wikipedia.org/wiki/Word_error_rate) (WER).

## Terms and abbreviations
* Reference, ground truth, expected, gold standard : file containing text transcription produced by humans.  
* Hypothesis: Transcript text derived from Speech to Text
* STT: Speech to Text
* WER: Word Error Rate

## Setup
### Create a developer account
1.  If you do not have a google account, [create one](https://support.google.com/mail/answer/56256?hl=en)
2.  Go to [Cloud Speech to Text](https://cloud.google.com/speech-to-text)
3.  Click **Try it Free** or **Get started for Free**
4.  Sign in
5.  In **Step 1 of 2** select your country, agree to terms, and click **Continue**
6.  In **Step 2 of 2** fill out all the information and supply a payment method (Speech to Text is free unless you hit some really high caps)

### Enable Cloud Speech-to-Text API
See also: [Before you begin](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries#before-you-begin)
1.  In the left menu select **APIs & Services > Library**
2.  In the search bar, type **speech**
3.  Click **Cloud Speech-to-Text API**
4.  Click **Enable**
5.  In the **Billing Required** dialog click **Enable Billing**

### Get credentials
1.  After enabling billing above, the API details are displayed.  In the right upper corner click **Create Credentials**
2.  In the step "Find out what kind of credentials you need" pull down menu, select **Cloud Speech-to-Text API**
3.  Select the "No, I'm not using them" radio button in the question "Are you planning to use this API with App Engine or Compute Engine?"
4.  Click **What credentials do I need**
5.  In the step "Create a service account", enter any name in the **Service account name** field (example: speech)
6.  In the **Role** pull down menu select **Project > Owner**
7.  The radio button for **Key type** should default to **JSON**.  Leave it at this default
8.  Click **Continue**
9.  A dialog will appear stating "Service account and key created" and a JSON file will download

#### Use of credentials JSON file
1.  Store the file anyplace you wish.  (I like to leave it at root level)
2.  Follow the applicable steps in [Set the environment variable GOOGLE_APPLICATION_CREDENTIALS](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries#before-you-begin)

##### Using the JSON with a python program
See also: [Before you begin](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries#before-you-begin)

**Method 1: In JSON path**  
1.  cd to the path where the JSON file resides
2.  Enable the applicable virtual environment
```bash
path_to_json user$ source path_to_virtual_env/bin/activate
```
3.  Run your program
```bash
path_to_json user$ python3 path_to_source/run.py
```

**Method 2: Supply path in command line**
```bash
path_to_source user$ GOOGLE_APPLICATION_CREDENTIALS=~/your_credentials_file.json python3 run.py 
```

### Python Environment
* Create a python environment as described in [Python Setup](https://cloud.google.com/python/setup).  See also:
    * [Installing Python](https://cloud.google.com/python/setup#installing_python)
    * [Installing Client Libraries](https://cloud.google.com/python/setup#installing_the_cloud_client_libraries_for_python)
    * [Installing Cloud SDK](https://cloud.google.com/python/setup#installing_the_cloud_sdk)

### Files
* For best results, follow [Best Practices](https://cloud.google.com/speech-to-text/docs/best-practices)
* Single directory containing **both** audio and reference text files
* Audio files must all be of a single [supported encoding type](https://cloud.google.com/speech-to-text/docs/encoding#audio-encodings)
* Audio files must all have a single [sample rate](https://cloud.google.com/speech-to-text/docs/basics#sample-rates)

#### File naming
Name the reference files with the same root name as the audio.  Reference files must end in .txt

Example:

```
audio_file_1.mp3
audio_file_1.txt
audio_file_2.mp3
audio_file_2.txt
```

#### Reference files
A reference file should contain only text that is a human derived transcription of the audio.  This text can be called reference text, expected results text, or ground truth text.  There is no need to add punctuation, or any kind of markup.  Punctuation will be removed and any other markup might produce anomalous WER results.  Somewhat standard transcription marking such as [cough] or [laugh] will be removed automatically, any other type of transcription markings that do not fall in brackets will cause miscalculated WER

## Usage
There are a number of command line options available

```cmd
python3 run.py -cs "gs://some/bucket" -lr local_result_folder -m video phone call -l es-MX -hz 44200 -p phrase-file.txt -b 10 30 50 -alts es-ES es-DO -n LINEAR16
```

### Required command line parameters
* -cs, --cloud_store_uri: [Cloud storage uri](https://cloud.google.com/speech-to-text/docs/basics#uri-audio) where audio and ground truth expected reference transcriptions are stored
* -lr, --local_results_path: Local path to store generated results
* -n, --encoding: Specifies [audio encoding type](https://cloud.google.com/speech-to-text/docs/encoding#audio-encodings)
### Optional
#### Speech to Text features
* -m, --models: Space separated list of [models](https://cloud.google.com/speech-to-text/docs/transcription-model) to evaluate.  Example "video phone"
* -l, --langs: [Language code](https://cloud.google.com/speech-to-text/docs/languages).  Default is en-US
* -hz, --sample_rate_hertz: Specifies the sample rate.  Example: 48000
* -e, --enhanced: Use the [enhanced model(s)](https://cloud.google.com/speech-to-text/docs/enhanced-models) if specified by -m
* -ch, --multi: Integer indicating the number of channels if more than one
* -p, --phrase_file: Path to file containing comma separated phrases for [speech adaptation](https://cloud.google.com/speech-to-text/docs/context-strength)
* -b, --boosts: Space separated list of integers for [boosts](https://cloud.google.com/speech-to-text/docs/boost) to apply for speech adaptation
* -alts, --alternative_languages: Space separated list of language codes for [auto language detection](https://cloud.google.com/speech-to-text/docs/multiple-languages). Example en-IN en-US en-GB")
#### Natural Language Processing 
Useful for some use cases where accurate transcription of every single word is not critical.  This may include sentiment analysis and labeling applications
* -ex, --expand: Expand all contractions.  Example aren't = are not"
* -stop, --remove_stop_words: Remove [stop words](https://www.geeksforgeeks.org/removing-stop-words-nltk-python/) from all text
* -stem, --stem: Apply [stemming](https://www.datacamp.com/community/tutorials/stemming-lemmatization-python)
* -n2w, --numbers_to_words: Convert numbers to words.  Example "order number 123" = "order number one two three"
#### Other
* -to, --transcriptions_only: If specified the only output will be transcripts, no analysis will be done
* -a, --alts2prime: Use each alternative language as a primary language.  Helpful when audio might be mixed for example en-US en-GB en-AU
* -q, --random_queue: Replace default queue.txt with randomly named queue file ####_queue.txt
* -fake, --fake_hyp: Use a fake hypothesis for testing.  This will allow skipping sending audio to the API
* -limit, --limit: Limits audio processing to int number.  Useful in cases where there is a lot of audio and you want to get some quick results first

## Speech adaptation
If using [phrases or classes](https://cloud.google.com/speech-to-text/docs/speech-adaptation) by specifying the command line argument -p, the file must be a text file.  It should contain a comma seperated list of phrases and/or classes.
```cmd
some_phrase_file.txt:

pizza, burger, fries, pickles
``` 
## Reports and diagnostics
### Detailed report
A results.csv file will be written to the results directory you specified on the command line.  The file contains the results of transcribing audio for each of the API options you specified
### Diagnostic HTML file
An html file will be written for each transcription in a similar naming pattern.  The HTML file highlights differences between the reference texts and the API results. 

## Resources
* [Before you begin](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries#before-you-begin)
* [Authentication Strategies](https://cloud.google.com/docs/authentication/#authentication_strategies)
* [Google Developer Account](https://cloud.google.com/docs/authentication/) 
* [Quickstart](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries#before-you-begin)
* [Getting Started](https://cloud.google.com/apis/docs/getting-started)
* [Enabling and Disabling Services](https://cloud.google.com/service-usage/docs/enable-disable)
* [Access Control](https://cloud.google.com/service-usage/docs/access-control)
* [Installing Python](https://cloud.google.com/python/setup#installing_python)
* [Installing Client Libraries](https://cloud.google.com/python/setup#installing_the_cloud_client_libraries_for_python)
* [Installing Cloud SDK](https://cloud.google.com/python/setup#installing_the_cloud_sdk)
* [Creating a service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts#creating)
* [Creating and managing service account keys](https://cloud.google.com/iam/docs/creating-managing-service-account-keys)
* [Stemming](https://www.datacamp.com/community/tutorials/stemming-lemmatization-python)
* [Stop words](https://pythonspot.com/nltk-stop-words/)
