class NLPOptions(object):
    should_expand_contractions = bool()
    should_apply_stemming = bool()
    should_convert_numbers_to_words = bool()
    should_remove_stop_words = bool()
    contractions = None

    def __init__(self):
        from utilities.contractions import contractions_dictionary
        self.contractions = contractions_dictionary

    def set_should_expand_contractions(self, option):
        self.should_expand_contractions = option

    def get_should_expand_contractions(self):
        return self.should_expand_contractions

    def set_should_apply_stemming(self, option):
        self.should_apply_stemming = option

    def get_should_apply_stemming(self):
        return self.should_apply_stemming

    def set_should_convert_numbers_to_words(self, option):
        self.should_convert_numbers_to_words = option

    def get_should_convert_numbers_to_words(self):
        return self.should_convert_numbers_to_words

    def set_should_remove_stop_words(self, option):
        self.should_remove_stop_words = option

    def get_should_remove_stop_words(self):
        return self.should_remove_stop_words


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