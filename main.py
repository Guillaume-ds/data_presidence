import streamlit as st
import datetime as dt 
from dateutil.relativedelta import relativedelta

from page_generale import page_generale
from page_candidat import page_candidat

from donnees import * 

st.set_page_config(page_title="La data présidentielle",layout='wide')

def main():
    #---------------------------------------------------------PAGES-------------------------------------------------------------------------------
    pages = {
        "Données générales": page_generale,
        "Suivi d'un candidat": page_candidat,
    }

    #--------------------------------------------------------SIDE BAR----------------------------------------------------------------------------- 
    st.sidebar.markdown("""<h2 style='text-align: center; font-weight:bold;padding-bottom:15px; margin-bottom:10px;'>
                    Choix de l'analyse</h2>""", unsafe_allow_html=True)
    page = st.sidebar.radio("", tuple(pages.keys()))
    
    #---------------------------------------------------------------Page------------------------------------------------------------------------
    st.markdown("""<h1 style='text-align: center; font-weight:bold;padding-bottom:15px; margin-bottom:10px;'>
                    LES CHIFFRES DE LA PRESIDENTIELLE</h1>""", unsafe_allow_html=True)
        
    
    pages[page]()


#!!!!!!!!!!!!!!!!!!!!!!!!!!!
if __name__ == "__main__":
    main()
#ne pas toucher, cela permet de conserver l'affichage même lorsqu'aucune page n'est sélectionnée