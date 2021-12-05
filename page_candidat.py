import streamlit as st

def page_candidat():
    choix_candidat = st.sidebar.selectbox("Candidat à analyser",["Macron","Zemmour","Le Pen","Lassal","Pécresse"])
    
    col1,col2,col3 = st.columns([2,1,2])
    col2.image(f"Static/{choix_candidat}.jpg",use_column_width=True)
    col2.markdown(f"""<p style='text-align: center; font-weight:bold; margin-bottom:10px;'>
                    {choix_candidat} </p>""",unsafe_allow_html=True)