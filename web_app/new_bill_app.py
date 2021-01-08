import streamlit as st
import plotly_express as px
import pandas as pd
import boto3
import json
import requests
import os
import joblib

from df_api import DataframeHandler


def new_bill_search():
    df = DataframeHandler()

    congress = 116
    cong_senators = df.get_senator_info(congress)

    bill_summary = st.sidebar.text_area('Bill summary:', "")
    sponsor_party = st.sidebar.selectbox('Sponsor Party', ['D', 'R', 'I'])
    num_co_D = st.sidebar.slider("Democrat Cosponsors", 0, sum(cong_senators.party == 'D'))
    num_co_R = st.sidebar.slider("Republican Cosponsors", 0, sum(cong_senators.party == 'R'))
    num_co_ID = st.sidebar.slider("Independent Cosponsors", 0, sum(cong_senators.party == 'I'))

    num_co_tot = num_co_D + num_co_R + num_co_ID

    st.write('**Congress**: ', congress)
    st.write('**Bill Number**: Test Bill')
    st.write('**Bill Summary**: ', bill_summary)
    st.write('**Sponsor Party**: ', sponsor_party)
    st.write('**Democrat Cosponsors**: ', num_co_D)
    st.write('**Republican Cosponsors**: ', num_co_R)
    st.write('**Independent Cosponsors**: ', num_co_ID)
    st.write('**Total Cosponsors**: ', num_co_tot)

    # set button to send to model
    start = st.sidebar.button('Bill Look Up')
    stop = st.sidebar.button('Reset')

    if start:
        # for session construction when in Docker container
        try:
            session = boto3.Session(aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                                    region_name=os.getenv('AWS_DEFAULT_REGION')
                                    )
        # for local testing
        except:
            session = boto3.Session(profile_name='jeremy_sagemaker')

        client = session.client('sagemaker-runtime')

        custom_attributes = ''
        endpoint_name = "senator-nlp-vote-prediction"  # Endpoint name.
        content_type = "application/json"              # The MIME type of the input data in the request body.
        accept = "application/json"                    # The desired MIME type of the inference in the response.
        payload = "..."                                # Payload for inference.



        def score(text):
            return client.invoke_endpoint(
                EndpointName=endpoint_name,
                CustomAttributes=custom_attributes,
                ContentType=content_type,
                Accept=accept,
                Body=text
                )['Body'].read().decode('utf-8')


        def score_local(text):
            return requests.post('http://localhost:8080/invocations', json=text).content


        pred_item = {"dataframe": cong_senators.to_json(),
                     "summary": bill_summary,
                     "sponsor_party": sponsor_party,
                     "num_co_D": num_co_D,
                     "num_co_R": num_co_R,
                     "num_co_ID": num_co_ID}


        test_item = {"dataframe": cong_senators.to_json(),
                     "summary": "This bill allows a crowdfunding issuer to sell shares through a crowdfunding vehicle. (Crowdfunding is a method of capital formation in which groups of people pool money to invest in a company or to support an effort to accomplish a specific goal.)",
                     "sponsor_party": "R",
                     "num_co_D": 1,
                     "num_co_R": 0,
                     "num_co_ID": 0}


        TEST_SERVER = True #os.getenv('TEST_SERVER', True)
        TEST_ITEM = False

        if TEST_SERVER:
            if TEST_ITEM:
                response = score(json.dumps(test_item))
            else:
                response = score(json.dumps(pred_item))
        else:
            if TEST_ITEM:
                response = score_local(test_item)
            else:
                response = score_local(pred_item)

        pred_df = pd.read_json(json.loads(response)['score_data'])

        def pass_or_not(df, column):
            if sum(df[column] == 'yea') > 50:
                return "Pass"
            elif sum(df[column] == 'nay') > 50:
                return "Fail"
            else:
                return "Uncertain"

        st.write('**Pass or Fail Predicted**: ', pass_or_not(pred_df, 'predict_cast'), '  \n \
                  **Yea votes**: ', str(sum(pred_df['predict_cast'] == 'yea')), '  \n \
                  **Nay votes**: ', str(sum(pred_df['predict_cast'] == 'nay')))


        st.markdown("Below you can see a distribution of senators' DW-NOMINATE score  \
                     against the model's predicted probability that the senator will vote 'yea'  \
                     on the bill.")

        st.markdown("The DW-NOMINATE score is a measure developed in the early  \
                     1980's for scoring congresspeople based on ideology (liberal-conservative)  \
                     and on more issue based politics. What is shown below is the first  \
                     dimension of that score, the liberal-conservative spectrum.")

        st.markdown("For a more detailed explanation on DW-NOMINATE, visit this  \
                     [wikipedia article](https://en.wikipedia.org/wiki/NOMINATE_(scaling_method)) \
                     on the subject.")

        st.markdown('### Distribution of predicted votes and dw_nominate score.')

        fig = px.scatter(pred_df, 
                         x ='nominate_dim1', y='predict_proba', 
                         color='party', 
                         hover_name='bioname',
                         hover_data={'nominate_dim1': False, 
                                     'party': False, 
                                     'predict_proba': ':.3f'},
                         color_discrete_map={'D':'blue', 
                                             'R':'red', 
                                             'I':'lightgreen'}
                        )

        #labels={'nominate_dim1': 'DW Nominate Score','predict_proba': 'Probability of Yea Vote'}

        fig.update_layout(xaxis_title="DW-NOMINATE Score",
                          yaxis_title="Probability of Yea Vote")

        st.plotly_chart(fig)

        st.markdown('### The full breakdown of votes')

        st.write(pred_df.sort_values(['party', 'predict_proba'], ascending=False))

