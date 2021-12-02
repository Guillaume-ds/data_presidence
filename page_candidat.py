import streamlit as st

def page_candidat():
    st.sidebar.selectbox("Candidat à analyser",["Macron","Zemmour","Le Pen","Lassal"])
    st.write("Page Candidat")