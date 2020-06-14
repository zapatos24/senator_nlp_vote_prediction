import streamlit as st
import plotly_express as px
import pandas as pd
from df_api import DataframeHandler
from model_api import ModelHandler

def new_bill_search():
    df = DataframeHandler()

    congress = 116
    cong_senators = df.get_senator_info(congress)

    bill_summary = st.sidebar.text_area('Bill summary:', "")
    sponsor_party = st.sidebar.selectbox('Sponsor Party', ['D', 'R', 'I'])
    num_cospon_D = st.sidebar.slider("Democrat Cosponsors", 0, sum(cong_senators.party == 'D'))
    num_cospon_R = st.sidebar.slider("Republican Cosponsors", 0, sum(cong_senators.party == 'R'))
    num_cospon_I = st.sidebar.slider("Independent Cosponsors", 0, sum(cong_senators.party == 'I'))

    num_cospon_tot = num_cospon_D + num_cospon_R + num_cospon_I

    st.write('**Congress**: ', congress)
    st.write('**Bill Number**: Test Bill')
    st.write('**Bill Summary**: ', bill_summary)
    st.write('**Sponsor Party**: ', sponsor_party)
    st.write('**Democrat Cosponsors**: ', num_cospon_D)
    st.write('**Republican Cosponsors**: ', num_cospon_R)
    st.write('**Independent Cosponsors**: ', num_cospon_I)
    st.write('**Total Cosponsors**: ', num_cospon_tot)


    #set button to send to model
    start = st.sidebar.button('Bill Look Up')
    stop = st.sidebar.button('Reset')

    if start:
        # cong_senators = df.get_senator_info(116)

        import sys
        print(sys.getsizeof(cong_senators))

        # req = {
        #     "dataframe": cong_senators.to_json(),
        #     "summary": "This bill allows a crowdfunding issuer to sell shares through a crowdfunding vehicle. (Crowdfunding is a method of capital formation in which groups of people pool money to invest in a company or to support an effort to accomplish a specific goal.)",
        #     "sponsor_party": "R",
        #     "num_co_D": 1,
        #     "num_co_R": 0,
        #     "num_co_ID": 0,
        # }

        # pred_df = ModelHandler.predict(req['summary'],
        #                                req['sponsor_party'],
        #                                int(req['num_co_D']),
        #                                int(req['num_co_R']),
        #                                int(req['num_co_ID']),
        #                                pd.read_json(req['dataframe']))

        pred_df = ModelHandler.predict(bill_summary,
                                       sponsor_party,
                                       num_co_D,
                                       num_co_R,
                                       num_co_ID,
                                       cong_senators)


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

