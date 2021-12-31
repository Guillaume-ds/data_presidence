import streamlit as st
import snscrape.modules.twitter as sntwitter

from scraping_journal import article_lemonde_sentiment
from scraping_twitter import scraptweets_candidat
from data import vspace,hr,comptes_twitter
import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd


def page_candidat():
    #------------------------------------------------Sidebar---------------------------------------------------------
    st.sidebar.markdown(hr,unsafe_allow_html = True)
    st.sidebar.markdown("<h2>Paramètres de l'analyse</h2>",unsafe_allow_html = True)
    choix_candidat = st.sidebar.selectbox("Candidat à analyser",
                                        comptes_twitter['Candidats'])
    
    st.sidebar.markdown(vspace,unsafe_allow_html = True)
    date_deb = st.sidebar.date_input("Choisir une date de début",max_value=dt.date.today()-relativedelta(days=3),value=dt.date.today()-relativedelta(days=30))   
    date_fin = st.sidebar.date_input("Choisir une date de fin",min_value=date_deb+relativedelta(days=1))
    st.sidebar.markdown(vspace,unsafe_allow_html = True)
    nombre_pages = st.sidebar.slider("Choix du nombre de pages à scrapper", min_value = 2, max_value=15)
    st.sidebar.markdown(vspace,unsafe_allow_html = True)   
    lancement_analyse = st.sidebar.button("Lancer l'analyse") 
    candidats = pd.read_csv("Static/candidats.csv")
    
    #------------------------------------------------Photo---------------------------------------------------------
    st.markdown(vspace,unsafe_allow_html = True)
    st.markdown(vspace,unsafe_allow_html = True)
    col1,col2,col3 = st.columns([2,1,2])
    col1.image(f"Static/img_candidats/{choix_candidat}.jpg",use_column_width=True)
    col3.markdown(f"""<h2 style='text-align: left; font-weight:bold; margin-bottom:50px;'>
                    {choix_candidat} </h2>""",unsafe_allow_html=True)
    
    parti = candidats.loc[candidats['Nom']==choix_candidat]['Parti'].item()
    courant = candidats.loc[candidats['Nom']==choix_candidat]['Courant'].item()
    nb_candidatures = int(candidats.loc[candidats['Nom']==choix_candidat]['Nb candidatures'].item()) 
    compte_twitter = comptes_twitter.loc[comptes_twitter['Candidats']==choix_candidat]['Compte Twitter'].item()
    
    col3.markdown(f"""<h4 style='text-align: left; font-weight:bold; margin-bottom:10px;'>
                    Parti : {parti} </h4>""",unsafe_allow_html=True)
    col3.markdown(f"""<h4 style='text-align: left; font-weight:bold; margin-bottom:10px;'>
                    Courant politique : {courant} </h4>""",unsafe_allow_html=True)
    
    col3.markdown(f"""<h4 style='text-align: left; font-weight:bold; margin-bottom:40px;'>
                    Candidat pour la {nb_candidatures} fois</h4>""",unsafe_allow_html=True)
    
    
    col3.markdown(f"""
                    <h4 style='text-align: left; font-weight:bold; margin-bottom:10px;'>
                    Twitter : <a href = 'https://twitter.com/{compte_twitter}'> {compte_twitter}</a>
                    </h4>
                    """,unsafe_allow_html=True)
    
    st.markdown(vspace,unsafe_allow_html = True)
    st.markdown(vspace,unsafe_allow_html = True)
    
    #------------------------------------------------Analyse sentiment---------------------------------------------------------
    if lancement_analyse:
        try:
            mean = article_lemonde_sentiment(date_deb,date_fin,nombre_pages,choix_candidat,choix_candidat)
            st.write(mean)
        except:
            st.error("Impossible d'effectuer la recherche avec ces paramètres")
    
    #------------------------------------------------Analyse twitter---------------------------------------------------------
    # Creating list to append tweet data to
    
    
    
    
    
    st.write(compte_twitter)
    
    
    analyse_tweet = st.button('analyser les tweets')
    if analyse_tweet:
        # Using TwitterSearchScraper to scrape data and append tweets to list
        test = scraptweets_candidat(date_deb,date_fin,compte_twitter)
        st.write(test)
        
    
    

