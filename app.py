import streamlit as st

import os
from PIL import Image

from page_generale import page_generale
from page_candidat import page_candidat

from data import vspace 

st.set_page_config(page_title="Data élections",layout='wide')

def main():
    #---------------------------------------------------------PAGES-------------------------------------------------------------------------------
    pages = {
        "Données générales": page_generale,
        "Suivi d'un candidat": page_candidat,
    }

    #--------------------------------------------------------SIDE BAR----------------------------------------------------------------------------- 
    path = os.path.dirname(__file__)
    my_file = path+'/Static/logo.jpg'
    st.sidebar.image(Image.open(my_file))
    st.sidebar.markdown(vspace,unsafe_allow_html=True)

    page = st.sidebar.radio("Choix de la page", tuple(pages.keys()))
    
    #---------------------------------------------------------------Page------------------------------------------------------------------------
    st.markdown("""<h1 style='text-align: center; font-weight:bold;padding-bottom:15px; margin-bottom:10px;color:rgba(20,10,80,1); text-decoration: underline rgba(20,10,80,1) 3px;'>
                    DES CHIFFRES POUR LA PRESIDENTIELLE</h1>""", unsafe_allow_html=True)
    st.markdown(vspace, unsafe_allow_html=True)
    
    
    
    pages[page]()


#!!!!!!!!!!!!!!!!!!!!!!!!!!!
if __name__ == "__main__":
    main()
#ne pas toucher, cela permet de conserver l'affichage même lorsqu'aucune page n'est sélectionnée