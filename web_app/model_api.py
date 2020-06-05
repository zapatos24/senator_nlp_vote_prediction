import pandas as pd
import numpy as np
import joblib
import xgboost as xgb
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import roc_auc_score
# from sklearn.metrics import roc_curve
# from sklearn.metrics import classification_report, 
# from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
# from sklearn.metrics import f1_score

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


    def make_predictions_df(self, main_df, predictions_list):
        main_df_features = ['bioname', 'party', 'cast_code']
        subset_df = main_df[main_df_features].copy()

        pred_df = pd.DataFrame(predictions_list, index=subset_df.index, columns=['predict_proba'])

        pred_df['predict_cast'] = pred_df['predict_proba'].apply(lambda x: 'yea' if round(x)==1 else 'nay')

        return subset_df.join(pred_df)


    def predict(self, df):
        X = df[self.features]
        y = df['cast_code']

        text_cols = ['summary']

        X_non_text = X[[x for x in self.features if x not in text_cols]]

        X_sc_df = self.scale_data(X_non_text)
        
        for col in text_cols:
            X_vec = self.vectorize_text(X[col], col)
            X_sc_df = X_sc_df.join(X_vec)


        predictions_xgb = self.model.predict_proba(X_sc_df)
        predictions_xgb = [item[1] for item in predictions_xgb]

        predictions_df = self.make_predictions_df(df, predictions_xgb)

        return predictions_df

