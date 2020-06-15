import boto3
import json
import pandas as pd
import requests
import os
import joblib

# from src.df_api import DataframeHandler

session = boto3.Session(profile_name='jeremy_sagemaker')
client = session.client('sagemaker-runtime')

custom_attributes = ''
endpoint_name = "senator_nlp_vote_prediction"  # Endpoint name.
content_type = "application/json"              # The MIME type of the input data in the request body.
accept = "application/json"                    # The desired MIME type of the inference in the response.
payload = "..."                                # Payload for inference.



def score(text):

    # from model_api import ModelHandler

    return client.invoke_endpoint(
        EndpointName=endpoint_name,
        CustomAttributes=custom_attributes,
        ContentType=content_type,
        Accept=accept,
        Body=text
        )['Body'].read().decode('utf-8')


def score_local(text):

    # from model_api import ModelHandler

    return requests.post('http://localhost:8080/invocations', json=text).content


path = 'model_artifacts/pred_xgb_df.sav'
df = joblib.load(path)


def congress_subset(df, congress):
    return df[df['congress'] == congress]


def get_senator_info(df, congress, df_size='small'):
    cong_df = congress_subset(df, congress)
    senator_df = cong_df.drop_duplicates(subset='bioname', keep='last')
    if df_size == 'small':
        short_cols = ['bioname', 'party', 'lead_party', 'nominate_dim1', 
                      'nominate_dim2', 'age', 'tenure', 
                      'percent_campaign_vote', 'party_R']

        return senator_df[short_cols]

    else:
        return senator_df

cong_senators = get_senator_info(df, 116)

import sys
print(sys.getsizeof(cong_senators))

test_item = {
    "dataframe": cong_senators.to_json(),
    "summary": "This bill allows a crowdfunding issuer to sell shares through a crowdfunding vehicle. (Crowdfunding is a method of capital formation in which groups of people pool money to invest in a company or to support an effort to accomplish a specific goal.)",
    "sponsor_party": "R",
    "num_co_D": 1,
    "num_co_R": 0,
    "num_co_ID": 0,
}
print('Type test_item:', type(test_item))


TEST_SERVER = False #os.getenv('TEST_SERVER', True)

if TEST_SERVER:
    print(score(test_item))
else:
    print(score_local(test_item))

