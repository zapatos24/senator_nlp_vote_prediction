import pandas as pd
import numpy as np
import joblib
import xgboost as xgb
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

from helperfunc import find_cosponsor_of_my_party, calc_cosponsor_party_percent

class ModelHandler:
    def __init__(self):
        self.model_path = '../final_xgb_model.sav'
        self.scaler_path = '../final_xgb_scaler.sav'
        self.feature_path = '../final_xgb_features.sav'
        self.embed_path = '../universal-sentence-encoder_4'
        self.model = joblib.load(self.model_path)
        self.scaler = joblib.load(self.scaler_path)
        self.features = joblib.load(self.feature_path)
        self.embed = hub.load(self.embed_path)


    def scale_data(self, df_X):
        data_sc = self.scaler.transform(df_X)

        X_scaled = pd.DataFrame(data_sc, index=df_X.index, columns=df_X.columns)

        return X_scaled


    def vectorize_text(self, text_df, column_name):
        X_embeddings = self.embed(text_df.values)

        short_col = column_name[:3]

        cols = [short_col+'_'+str(i) for i in range(np.shape(X_embeddings)[1])]

        X_embed = pd.DataFrame(np.asarray(X_embeddings), index=text_df.index, columns=cols)

        return X_embed


    def make_predictions_df(self, bill_df, predictions_list, bill_type='new'):
        bill_df_features = ['bioname', 'party']
        if bill_type == 'old':
            bill_df_features.append('cast_code')
        subset_df = bill_df[bill_df_features].copy()

        pred_df = pd.DataFrame(predictions_list, index=subset_df.index, columns=['predict_proba'])

        pred_df['predict_cast'] = pred_df['predict_proba'].apply(lambda x: 'yea' if round(x)==1 else 'nay')

        return subset_df.join(pred_df)


    def make_new_bill_df(self, bill_sum, sponsor_party, num_co_D, num_co_R, num_co_I, senator_df):
        new_df = senator_df.copy()
        new_df['summary'] = bill_sum
        new_df['sponsor_party'] == sponsor_party
        new_df['cosponsors'] = num_co_D + num_co_R + num_co_I
        new_df['cosponsors_D'] = num_co_D
        new_df['cosponsors_R'] = num_co_R
        new_df['cosponsors_ID'] = num_co_I

        new_df['cosponsors^2'] = new_df['cosponsors']**2

        for party in ['D', 'R', 'ID']:
            title = 'cosponsors_'+party+'^2'
            new_df[title] = new_df['cosponsors_'+party]**2

        new_df['sponsor_is_same_party'] = new_df.apply(lambda x: 1 if x['party'] == x['sponsor_party'] else 0, axis=1)

        new_df['cosponsor_my_party'] = new_df.apply(lambda x: find_cosponsor_of_my_party(x), axis=1)
        new_df['cosponsor_my_party^2'] = new_df['cosponsor_my_party']**2

        for party in ['D', 'R']:
            new_df['cosponsor_party_{}_%'.format(party)] = new_df.apply(lambda x: calc_cosponsor_party_percent(x, party), 
                                                                        axis=1)

        new_df['percent_cosponsors_lead_party'] = new_df.apply(lambda x: x['cosponsor_party_D_%'] 
                                                               if x['lead_party'] == 'D'
                                                               else x['cosponsor_party_R_%'], axis=1)

        return new_df


    def predict(self, df, bill_type='new'):
        X = df[self.features]

        text_cols = ['summary']

        X_non_text = X[[x for x in self.features if x not in text_cols]]

        X_sc_df = self.scale_data(X_non_text)
        
        for col in text_cols:
            X_vec = self.vectorize_text(X[col], col)
            X_sc_df = X_sc_df.join(X_vec)


        predictions_xgb = self.model.predict_proba(X_sc_df)
        predictions_xgb = [item[1] for item in predictions_xgb]

        predictions_df = self.make_predictions_df(df, predictions_xgb, bill_type)

        return predictions_df

