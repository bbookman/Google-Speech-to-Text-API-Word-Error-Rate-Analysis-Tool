class NLPOptions(object):

    contractions = None

    def __init__(self):
        from utilities.contractions import contractions_dictionary
        self.contractions = contractions_dictionary


    def expand_contractions(self, text):
        import re
        contractions = self.contractions
        contractions_pattern = re.compile('({})'.format('|'.join(contractions.keys())),
                                          flags=re.IGNORECASE | re.DOTALL)

        def expand_match(contraction):
            match = contraction.group(0)
            first_char = match[0]
            expanded_contraction = contractions.get(match) \
                if contractions.get(match) \
                else contractions.get(match.lower())
            expanded_contraction = first_char + expanded_contraction[1:]
            # Hack for this bug: https://github.com/dipanjanS/practical-machine-learning-with-python/issues/24
            if expanded_contraction == "as not":
                return "is not"
            return expanded_contraction

        expanded_text = contractions_pattern.sub(expand_match, text)
        expanded_text = re.sub("'", "", expanded_text)
        return expanded_text

    def convert_numbers_to_words(self, text):
        # does not handle things like 21st, 4th
        from nltk.tokenize import word_tokenize
        import inflect

        result = ''
        i = inflect.engine()
        word_tokens = word_tokenize(text)
        for w in word_tokens:
            if w.isdigit():
                numword = i.number_to_words(w)
                result += f' {numword}'
            else:
                result += f' {w}'
        return result

    def remove_stop_words(self, text):
        from nltk.corpus import stopwords
        import string
        result = str()
        stop_words = set(stopwords.words('english'))
        words = text.split()
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in words]
        filtered = [w for w in stripped if not w in stop_words]
        for w in filtered:
            result += " " + w
        return result

    def apply_stemming(self, text):
        from nltk.stem import PorterStemmer
        from nltk.tokenize import word_tokenize

        results = ""
        ps = PorterStemmer()
        words = word_tokenize(text)

        for w in words:
            results += (ps.stem(w) + " ")
        return results