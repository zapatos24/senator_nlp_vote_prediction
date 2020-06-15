import pandas as pd
import numpy as np
import joblib
import os
import xgboost as xgb
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

from helperfunc import find_cosponsor_of_my_party, calc_cosponsor_party_percent


class ModelHandler:
	model_path = os.path.join(os.path.abspath(os.getenv('XGB_MODEL_PATH')), 'final_xgb_model.sav')
	scaler_path = os.path.join(os.path.abspath(os.getenv('XGB_MODEL_PATH')), 'final_xgb_scaler.sav')
	feature_path = os.path.join(os.path.abspath(os.getenv('XGB_MODEL_PATH')), 'final_xgb_features.sav')
	embed_path = os.path.abspath(os.getenv('TFHUB_CACHE_DIR'))

	model = joblib.load(model_path)
	scaler = joblib.load(scaler_path)
	features = joblib.load(feature_path)
	embed = hub.load(embed_path)


	@classmethod
	def health_check(cls):
		return (cls.model is not None) and (cls.embed is not None)


	@classmethod
	def scale_data(cls, df_X):
		data_sc = cls.scaler.transform(df_X)

		X_scaled = pd.DataFrame(data_sc, index=df_X.index, columns=df_X.columns)

		return X_scaled


	@classmethod
	def vectorize_text(cls, text):
		return cls.embed(text)


	@classmethod
	def make_predictions_df(cls, bill_df, predictions_list):
		app_cols = ['bioname', 'party', 'nominate_dim1',
                    'predict_proba', 'predict_cast']

		pred_df = pd.DataFrame(predictions_list, index=bill_df.index, columns=['predict_proba'])
		pred_df['predict_cast'] = pred_df['predict_proba'].apply(lambda x: 'yea' if x > .9 else 'nay')

		full_pred_df = bill_df.join(pred_df)

		return full_pred_df[app_cols]


	@classmethod
	def make_new_bill_df(cls, bill_sum, sponsor_party, num_co_D, num_co_R, num_co_ID, senator_df):
		new_df = senator_df.copy()
		new_df['summary'] = bill_sum
		new_df['sponsor_party'] = sponsor_party
		new_df['cosponsors'] = num_co_D + num_co_R + num_co_ID
		new_df['cosponsors_D'] = num_co_D
		new_df['cosponsors_R'] = num_co_R
		new_df['cosponsors_ID'] = num_co_ID

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

		new_df.reset_index(drop=True, inplace=True)

		return new_df


	@classmethod
	def predict(cls, bill_sum, sponsor_party, num_co_D, num_co_R, num_co_ID, senator_df):
		df = cls.make_new_bill_df(bill_sum, sponsor_party, num_co_D, 
								  num_co_R, num_co_ID, senator_df)
		X = df[cls.features]

		text_cols = ['summary']

		X_non_text = X[[x for x in cls.features if x not in text_cols]]

		X_sc_df = cls.scale_data(X_non_text)

		for col in text_cols:
			X_embed = cls.vectorize_text(X[col].unique())
			X_embed_array = np.asarray(X_embed)[0]

			short_col = col[:3]

			for i in range(X_embed_array.shape[0]):
				col_name = short_col+'_'+str(i)
				X_sc_df[col_name] = X_embed_array[i]

			# vec_cols = [short_col+'_'+str(i) for i in range(np.shape(X_embed)[1])]

			# X_vec_df = pd.DataFrame(np.asarray(X_embed), index=X.index, columns=cols)

			# X_sc_df = X_sc_df.join(X_vec_df)


		predictions_xgb = cls.model.predict_proba(X_sc_df)
		predictions_xgb = [item[1] for item in predictions_xgb]

		predictions_df = cls.make_predictions_df(df, predictions_xgb)

		return predictions_df

