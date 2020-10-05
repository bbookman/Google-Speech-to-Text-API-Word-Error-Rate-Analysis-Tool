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
        df.drop(['INSERTIONS','DELETIONS','SUBSTITUTIONS','DELETED_WORDS','INSERTED_WORDS','SUBSTITUTE_WORDS'], axis=1, inplace=True)
        df.groupby(['MODEL', 'ENHANCED', 'BOOST']).describe().to_html('describe.html')
