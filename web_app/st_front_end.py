import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
from df_api import DataframeHandler
from model_api import ModelHandler

''' 
# Old Bill Voting

Comparing model against reality
'''

df = DataframeHandler()

congress = st.sidebar.multiselect('Congress?', df.get_unique_values('congress', df.df))

cong_subset = df.congress_subset(congress)

bill_num = st.sidebar.multiselect('Bill number?', 
                                  df.get_unique_values(col_name='bill_number', 
                                                       subset_df=cong_subset))


bill_subset = df.bill_subset(bill_num, cong_subset)

st.write('Congress: ', congress[0])
st.write('Bill Number: ', bill_num[0])

model = ModelHandler()

predict_df = model.predict(bill_subset)

def pass_or_not(df):
    if sum([round(x) for x in df.predict_proba.values]) > 50:
        return "Pass"
    else:
        return "Fail"

# st.write(predict_df['predict_cast'] == 'yea')

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

# create figure using plotly express
# fig = px.scatter(new_df, x ='nominate_dim1',y='predict_proba',color='party')
# Plot!
# st.plotly_chart(fig)
