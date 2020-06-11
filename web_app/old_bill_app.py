import streamlit as st
import plotly_express as px

from df_api import DataframeHandler
# from model_api import ModelHandler

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
    start = st.sidebar.button('Bill Look Up')
    stop = st.sidebar.button('Reset')

    if start:
        def pass_or_not(df, column):
            if sum(bill_subset[column] == 1) > 50:
                return "Pass"
            elif sum(bill_subset[column] == 0) > 50:
                return "Fail"
            else:
                return "Uncertain"

        st.write('**Pass or Fail Actual**: ', pass_or_not(bill_subset, 'cast_code'), '  \n \
                  **Yea votes**: ', str(sum(bill_subset['cast_code'] == 1)), '  \n \
                  **Nay votes**: ', str(sum(bill_subset['cast_code'] == 0)))

        st.write('**Pass or Fail Predicted**: ', pass_or_not(bill_subset, 'predict_cast'), '  \n \
                  **Yea votes**: ', str(sum(bill_subset['predict_cast'] == 1)), '  \n \
                  **Nay votes**: ', str(sum(bill_subset['predict_cast'] == 0)))


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

        fig = px.scatter(bill_subset, 
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

        st.write(df.get_vote_breakdown(bill_subset).sort_values(['party', 'predict_proba'], ascending=False))

