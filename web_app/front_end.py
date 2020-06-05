import streamlit as st
from old_bill_app import old_bill_search

'''
# HOW WILL THEY VOTE?
'''
new = st.button('New Bills')
old = st.button('Old Bills')

if new:
    new_bill_search()
if old:
    old_bill_search()
