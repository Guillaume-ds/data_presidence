import streamlit as st
from data import vspace
import datetime as dt

def page_generale():
    st.markdown(vspace, unsafe_allow_html=True)
    
    date_election = dt.date(2022,4,24)
    delta_election = (date_election-dt.date.today()).days
    
    st.markdown(f"""<h1 style='text-align: center; font-weight:bold;padding-bottom:15px; margin-bottom:10px;'>
                    J-{delta_election} </h1>""",unsafe_allow_html=True)
    