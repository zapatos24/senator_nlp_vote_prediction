import pandas as pd
import joblib

class DataframeHandler:
    def __init__(self):
        self.path = '../model_artifacts/pred_xgb_df.sav'
        # self.df = joblib.load(self.path)


    def congress_subset(self, congress):
        df = joblib.load(self.path)
        cong_df = df[df.congress == congress]

        return cong_df


    def bill_subset(self, bill_num, subset_df=[]):
        if type(subset_df) == 'list':
            df = subset_df
        else:
            df = joblib.load(self.path)

        bill_df = df[df.bill_number == bill_num]

        return bill_df


    def unique_subset(self, unique_col, subset_df, cols_to_return=[]):
        # unique_vals = subset_df[unique_col].unique()
        new_df = subset_df.drop_duplicates(subset=unique_col, keep='last')

        if cols_to_return:
            try:
                return new_df[cols_to_return]
            except:
                print('One of cols not in dataframe.')
        else:
            return new_df


    def get_unique_values(self, col_names=[], col_values=[], unique_col=''):
        if len(col_names) != len(col_values):
            print('Need values for all columns passed')
            return

        if len(col_names) > 2:
            print("Please no more than 2 columns")
            return

        df = joblib.load(self.path)

        if len(col_names) == 0:
            return df[unique_col].unique()

        if len(col_names) == 1:
            slice_df = df[df[col_names[0]] == col_values[0]]
            return slice_df[unique_col].unique()

        if len(col_names) == 2:
            slice_df = df[(df[col_names[0]] == col_values[0]) & 
                          (df[col_names[1]] == col_values[1])]
            return slice_df[unique_col].unique()

        print('Something went wrong')
        return


    def get_vote_breakdown(self, congress, bill_num):
        cong_df = self.congress_subset(congress)
        bill_df = self.bill_subset(bill_num, cong_df)

        app_cols = ['bioname', 'party', 'nominate_dim1', 'cast_code', 
                    'predict_proba', 'predict_cast']

        return bill_df[app_cols]

