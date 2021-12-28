import streamlit as st
import snscrape.modules.twitter as sntwitter

from scraping_journal import article_lemonde_sentiment
from data import vspace,hr
import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd

def page_candidat():
    #------------------------------------------------Sidebar---------------------------------------------------------
    st.sidebar.markdown(hr,unsafe_allow_html = True)
    st.sidebar.markdown("<h2>Paramètres de l'analyse</h2>",unsafe_allow_html = True)
    choix_candidat = st.sidebar.selectbox("Candidat à analyser",["Macron","Zemmour","Le Pen","Lassal","Pécresse"])
    
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
    tweets_list1 = []

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:EmmanuelMacron').get_items()):
        if i>100:
            break
        tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.lang])
        
    # Creating a dataframe from the tweets list above 
    tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Tweet Id', 'Text', 'Username','lang'])
    st.write(tweets_df1)