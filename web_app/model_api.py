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

class ModelFunctions:
    def __init__(self):
        self.model_path = '../final_xgb_model.sav'
        self.scaler_path = '../final_xgb_scaler.sav'
        self.feature_path = '../final_xgb_features.sav'
        self.embed_path = '../universal-sentence-encoder_4'
        self.model = joblib.load(self.model_path)
        self.scaler = joblib.load(self.scaler_path)
        self.features = joblib.load(self.feature_path)
        self.embed = hub.load(embed_path)


    def scale_data(self, df_X):
        data_sc = scalar.transform(df_X)

        X_scaled = pd.DataFrame(data_sc, index=df_X.index, columns=df_X.columns)

        return X_scaled


    def vectorize_text(self, text_df):
        X_embeddings = self.embed(text_df.values)

        return X_embeddings


    def predict(self, df):
        X = df[self.features]
        y = df['cast_code']

        text_cols = ['summary']

        X_non_text = X[[x for x in self.features if x not in text_cols]]

        X_sc = scale_data(X_non_text)
        
        for col in text_cols:
            X_vec = vectorize_text(X[col])


        predictions_xgb = self.model.predict_proba(X_sc)
        predictions_xgb = [item[1] for item in predictions_xgb]

        return predictions_xgb

