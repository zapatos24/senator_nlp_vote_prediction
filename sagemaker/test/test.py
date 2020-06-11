import boto3
import json
import pandas as pd

from df_api import DataframeHandler


client = boto3.client('sagemaker-runtime')

custom_attributes = ''
endpoint_name = "senator_nlp_vote_prediction"               # Endpoint name.
content_type = "application/json"                           # The MIME type of the input data in the request body.
accept = "application/json"                                 # The desired MIME type of the inference in the response.
payload = "..."                                             # Payload for inference.


def score(text):

    # from model_api import ModelHandler

    return client.invoke_endpoint(
        EndpointName=endpoint_name,
        CustomAttributes=custom_attributes,
        ContentType=content_type,
        Accept=accept,
        Body=text
        )['Body'].read().decode('utf-8')



df = DataframeHandler()
cong_senators = df.unique_subset('bioname',
                                     df.congress_subset(116))

test_item = {
    "dataframe": cong_senators.to_json(),
    "summary": "This bill allows a crowdfunding issuer to sell shares through a crowdfunding vehicle. (Crowdfunding is a method of capital formation in which groups of people pool money to invest in a company or to support an effort to accomplish a specific goal.)",
    "sponsor_party": "R",
    "d_cosponsors": 1,
    "r_cosponsors": 0,
    "i_cosponsors": 0,
}

print(score(json.dumps(test_item)))

# print(json.loads(json.dumps(test_item))[0])

