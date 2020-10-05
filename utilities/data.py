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
        df.groupby(['MODEL','ENHANCED', 'BOOST' ])['WER'].mean()
        import pdb;pdb.set_trace()
        print('')