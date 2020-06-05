import pandas as pd
import numpy as np
import pickle as pkl

class DataframeHandler:
    def __init__(self):
        self.path = '../main_df.pkl'
        self.df = pd.read_pickle(self.path)


    def congress_subset(self, congress):
        cong_df = self.df[self.df.congress.isin(congress)]

        return cong_df


    def bill_subset(self, bill_num, subset_df):
        bill_df = subset_df[subset_df.bill_number.isin(bill_num)]

        return bill_df


    def get_unique_values(self, col_name, subset_df):
        return subset_df[col_name].unique()

