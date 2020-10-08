class Data(object):

    def __init__(self, file_path):
        self.results_file_path = file_path

    def read_csv(self):
        import pandas as pd
        try:
            df = pd.read_csv(self.results_file_path, engine='python')
        except FileNotFoundError:
            raise
        return df

    def stats(self):
        df = self.read_csv()
        df.drop(['WER', 'AUDIO_FILE','INSERTIONS','DELETIONS','SUBSTITUTIONS','DELETED_WORDS','INSERTED_WORDS','SUBSTITUTE_WORDS'], axis=1, inplace=True)
        df['WER_BY_GROUP'] = 0
        group_list = ['MODEL', 'ENHANCED', 'BOOST']
        if 'DIGITS' in df.columns:
            group_list.append('DIGITS')
        grouped = df.groupby(group_list)
        averaged = grouped.apply(
            #lambda x: x.assign(WER_BY_GROUP = round((x.REF_ERROR_COUNT / x.REF_WORD_COUNT * 100), 3))).reset_index([group_list], drop = True)
            lambda x: x.assign(WER_BY_GROUP=round((x.REF_ERROR_COUNT / x.REF_WORD_COUNT * 100), 3)))
        averaged.drop(columns=['LANGUAGE', 'HINTS', 'REF_WORD_COUNT', 'REF_ERROR_COUNT'], inplace=True)
        averaged['WER_BY_GROUP'].idxmin
        return averaged
       # averaged.to_html('summary.html')



