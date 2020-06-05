import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
from df_api import DataframeFunctions
# import model_api

''' 
# Old Bill Voting

Comparing model against reality
'''

df = DataframeFunctions()

congress = st.sidebar.multiselect('Congress?', df.get_unique_values('congress', df.df))

cong_subset = df.congress_subset(congress)

bill_num = st.sidebar.multiselect('Bill number?', 
                                  df.get_unique_values(col_name='bill_number', 
                                                       subset_df=cong_subset))


bill_subset = df.bill_subset(bill_num, cong_subset)
# new_df = cong_subset[(cong_subset['congress'].isin(congress)) & 
#                      (cong_subset['bill_number'].isin(bill_num))]

st.write(bill_subset)

'''
### And here is a chart.
'''

# create figure using plotly express
fig = px.scatter(new_df, x ='nominate_dim1',y='percent_campaign_vote',color='party_D')
# Plot!
st.plotly_chart(fig)
