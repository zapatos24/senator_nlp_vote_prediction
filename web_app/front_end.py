import streamlit as st
from old_bill_app import old_bill_search
import SessionState

'''
# HOW WILL THEY VOTE?
'''

st.sidebar.title("Bill Type")
radio = st.sidebar.radio(label="", options=["New Bills", "Old Bills"])

session_state = SessionState.get(a=0, b=0)  # Pick some initial values.

if radio == "New Bills":
    session_state.a = float(st.text_input(label="What is a?", value=session_state.a))
    st.write(f"You set a to {session_state.a}")
elif radio == "Old Bills":
    ''' 
    # Old Bill Voting

    Comparing model against reality

    Congress guide:

    **116**: 2018 - 2020

    **115**: 2016 - 2018

    **114**: 2014 - 2016

    **113**: 2012 - 2014
    '''
    session_state.b = old_bill_search()
    st.write(f"You set b to {session_state.b}")

new = st.button('New Bills')
old = st.button('Old Bills')

if new:
    new_bill_search()
if old:
    old_bill_search()
