import streamlit as st
import snscrape.modules.twitter as sntwitter

from scraping_journal import article_lemonde_sentiment
from scraping_twitter import scraptweets_candidat
from data import vspace,hr
import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd


def page_candidat():
    #------------------------------------------------Sidebar---------------------------------------------------------
    st.sidebar.markdown(hr,unsafe_allow_html = True)
    st.sidebar.markdown("<h2>Paramètres de l'analyse</h2>",unsafe_allow_html = True)
    choix_candidat = st.sidebar.selectbox("Candidat à analyser",
                                          ["Yannick Jadot",
                                           "Emmanuel Macron",
                                           "Eric Zemmour",
                                           "Marine Le Pen",
                                           "Jean Lassal",
                                           "Valérie Pécresse"])
    
    st.sidebar.markdown(vspace,unsafe_allow_html = True)
    date_deb = st.sidebar.date_input("Choisir une date de début",max_value=dt.date.today()-relativedelta(days=3),value=dt.date.today()-relativedelta(days=30))   
    date_fin = st.sidebar.date_input("Choisir une date de fin",min_value=date_deb+relativedelta(days=1))
    st.sidebar.markdown(vspace,unsafe_allow_html = True)
    nombre_pages = st.sidebar.slider("Choix du nombre de pages à scrapper", min_value = 2, max_value=15)
    st.sidebar.markdown(vspace,unsafe_allow_html = True)   
    lancement_analyse = st.sidebar.button("Lancer l'analyse") 
    
    #------------------------------------------------Photo---------------------------------------------------------
    col1,col2,col3 = st.columns(3)
    col2.image(f"Static/{choix_candidat}.jpg",use_column_width=True)
    col2.markdown(f"""<p style='text-align: center; font-weight:bold; margin-bottom:10px;'>
                    {choix_candidat} </p>""",unsafe_allow_html=True)
    
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
    
    comptes_twitter = pd.read_csv('Static\comptes_twitter.csv')
    
    compte_twitter = comptes_twitter[comptes_twitter['Candidats']==choix_candidat]['Compte Twitter'].item()
    
    st.write(compte_twitter)
    
    
    analyse_tweet = st.button('analyser les tweets')
    if analyse_tweet:
        # Using TwitterSearchScraper to scrape data and append tweets to list
        test = scraptweets_candidat(date_deb,date_fin,compte_twitter)
        st.write(test)
        
    
    

