import pandas as pd
import numpy as np
import joblib

class DataframeHandler:
    def __init__(self):
        self.path = '../final_xgb_df.sav'
        self.df = joblib.load(self.path)


    def congress_subset(self, congress):
        cong_df = self.df[self.df.congress == congress]

        return cong_df


    def bill_subset(self, bill_num, subset_df):
        bill_df = subset_df[subset_df.bill_number == bill_num]

        return bill_df


    def get_unique_values(self, col_name, subset_df):
        return subset_df[col_name].unique()

