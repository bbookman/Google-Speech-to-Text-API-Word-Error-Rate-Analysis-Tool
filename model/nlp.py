class NLPModel(object):
    remove_stop_words = False
    apply_stemming = False
    expand_contractions = False
    convert_numbers_to_words = False

    def set_remove_stop_words(self, setting):
        if not isinstance(setting, bool):
            raise TypeError(f'Failure setting value for remove_stop_words.  Expected bool, got {type(setting)}')
        self.remove_stop_words = setting

    def get_remove_stop_words(self):
        return self.remove_stop_words

    def set_apply_stemming(self, setting):
        if not isinstance(setting, bool):
            raise TypeError(f'Failure setting value for apply stemming.  Expected bool, got {type(setting)}')
        self.apply_stemming = setting

    def get_apply_stemming(self):
        return self.apply_stemming

    def set_expand_contractions(self, setting):
        if not isinstance(setting, bool):
            raise TypeError(f'Failure setting value for expand contractions.  Expected bool, got {type(setting)}')
        self.expand_contractions = setting

    def get_expand_contractions(self):
        return self.expand_contractions

    def set_n2w(self, setting):
        if not isinstance(setting, bool):
            raise TypeError(f'Failure seting value for convert numbers to words.  Expected bool, got {type(setting)}')
        self.convert_numbers_to_words = setting

    def get_n2w(self):
        return self.convert_numbers_to_words