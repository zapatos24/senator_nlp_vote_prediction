import pandas as pd
import joblib

class DataframeHandler:
    def __init__(self):
        self.path = 'pred_xgb_df.sav'
        self.df = joblib.load(self.path)


    def congress_subset(self, congress):
        cong_df = self.df[self.df.congress == congress]

        return cong_df


    def bill_subset(self, bill_num, subset_df):
        bill_df = subset_df[subset_df.bill_number == bill_num]

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


    def get_unique_values(self, col_name, subset_df):
        return subset_df[col_name].unique()


    def get_vote_breakdown(self, subset_df):
        app_cols = ['bioname', 'party', 'predict_proba', 'cast_code', 'predict_cast']
        return subset_df[app_cols]

