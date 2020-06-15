import pandas as pd
import os
import joblib

class DataframeHandler:
    path = os.path.join(os.path.abspath(os.getenv('XGB_MODEL_PATH')), 'pred_xgb_df.sav')
    # path = '../model_artifacts/pred_xgb_df.sav'
    df = joblib.load(path)


    @classmethod
    def congress_subset(cls, congress):
        return cls.df[cls.df['congress'] == congress]


    @classmethod
    def bill_subset(cls, bill_num, subset_df=[]):
        if type(subset_df) == 'list':
            bill_df = subset_df
        else:
            bill_df = cls.df.copy()

        return bill_df[bill_df.bill_number == bill_num]


    @classmethod
    def get_senator_info(cls, congress, df_size='small'):
        cong_df = cls.congress_subset(congress)
        senator_df = cong_df.drop_duplicates(subset='bioname', keep='last')
        if df_size == 'small':
            short_cols = ['bioname', 'party', 'lead_party', 'nominate_dim1', 
                          'nominate_dim2', 'age', 'tenure', 
                          'percent_campaign_vote', 'party_R']
            return senator_df[short_cols]

        else:
            return senator_df


    @classmethod
    def get_unique_values(cls, col_names=[], col_values=[], unique_col=''):
        if len(col_names) != len(col_values):
            print('Need values for all columns passed')
            return

        if len(col_names) > 2:
            print("Please no more than 2 columns")
            return


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


    @classmethod
    def get_vote_breakdown(cls, congress, bill_num):
        bill_df = cls.bill_subset(bill_num, cls.congress_subset(congress))

        app_cols = ['bioname', 'party', 'nominate_dim1', 'cast_code', 
                    'predict_proba', 'predict_cast']

        return bill_df[app_cols]

