import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
from df_api import DataframeHandler
from model_api import ModelHandler

def old_bill_search():
    df = DataframeHandler()

    congress = st.sidebar.selectbox('Congress?', df.get_unique_values('congress', df.df))
    cong_subset = df.congress_subset(congress)

    st.write('**Congress**: ', congress)

    bill_num = st.sidebar.selectbox('Bill number?', 
                                      df.get_unique_values(col_name='bill_number', 
                                                           subset_df=cong_subset))


    bill_subset = df.bill_subset(bill_num, cong_subset)

    st.write('**Bill Number**: ', bill_num)

    #set button to send to model
    start = st.button('Bill Look Up')
    stop = st.button('Reset')

    if start:
        def pass_or_not(df):
            if sum(bill_subset['predict_cast'] == 1) > 50:
                return "Pass"
            elif sum(bill_subset['predict_cast'] == 0) > 50:
                return "Fail"
            else:
                return "Uncertain"

        st.write('Pass or Fail: ', pass_or_not(bill_subset))
        st.write('Yea votes: ', str(sum(bill_subset['predict_cast'] == 1)))
        st.write('Nay votes: ', str(sum(bill_subset['predict_cast'] == 0)))

        st.markdown('### Distribution of predicted votes and dw_nominate score.')


                                 # category_orders={'party':['D', 'R', 'I']},

        fig = px.scatter(bill_subset, x ='nominate_dim1', y='predict_proba', color='party', 
                         hover_name='bioname',
                         color_discrete_map={'D':'blue', 'R':'red', 'I':'lightgreen'},
                         labels={'nominate_dim1': 'DW Nominate Score',
                                 'predict_proba': 'Probability of Yea Vote'})

        st.plotly_chart(fig)

        st.markdown('### The full breakdown of votes')

        st.write(df.get_vote_breakdown(bill_subset).sort_values(['party', 'predict_proba'], ascending=False))

