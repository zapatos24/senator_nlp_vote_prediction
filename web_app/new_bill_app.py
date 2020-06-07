import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
from df_api import DataframeHandler
from model_api import ModelHandler

def new_bill_search():
    df = DataframeHandler()

    congress = 116
    cong_subset = df.congress_subset(congress)

    bill_summary = st.sidebar.text_area('Bill summary:', "")
    sponsor_party = st.sidebar.selectbox('Sponsor Party', ['D', 'R', 'I'])
    num_cospon_D = st.sidebar.slider("Democrat Cosponsors", 0, sum(cong_subset.party == 'D'))
    num_cospon_R = st.sidebar.slider("Republican Cosponsors", 0, sum(cong_subset.party == 'R'))
    num_cospon_I = st.sidebar.slider("Independent Cosponsors", 0, sum(cong_subset.party == 'I'))

    num_cospon_tot = num_cospon_D + num_cospon_R + num_cospon_I

    st.write('**Congress**: ', congress)
    st.write('**Bill Number**: Test Bill')
    st.write('**Bill Summary**: ', bill_summary)
    st.write('**Democrat Cosponsors**: ', num_cospon_D)
    st.write('**Republican Cosponsors**: ', num_cospon_R)
    st.write('**Independent Cosponsors**: ', num_cospon_I)
    st.write('**Total Cosponsors**: ', num_cospon_tot)


    #set button to send to model
    start = st.button('Bill Look Up')
    stop = st.button('Reset')

    if start:
        model = ModelHandler()

        predict_df = model.predict(bill_subset)

        def pass_or_not(df):
            if sum([round(x) for x in df.predict_proba.values]) > 50:
                return "Pass"
            else:
                return "Fail"

        st.write('Pass or Fail: ', pass_or_not(predict_df))
        st.write('Yea votes: ', str(sum(predict_df['predict_cast'] == 'yea')))
        st.write('Nay votes: ', str(sum(predict_df['predict_cast'] == 'nay')))

        nominate_df = bill_subset.join(predict_df[['predict_proba', 'predict_cast']])

        '''
        ### Distribution of predicted votes and dw_nominate score.
        '''

        fig = px.scatter(nominate_df, x ='nominate_dim1', y='predict_proba', color='party')

        st.plotly_chart(fig)

        '''
        ### The full breakdown of votes
        '''

        st.write(predict_df.sort_values(['party', 'predict_proba'], ascending=False))