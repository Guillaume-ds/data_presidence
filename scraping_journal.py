import requests as rq
from bs4 import BeautifulSoup as bs
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
import streamlit as st

analyzer = SentimentIntensityAnalyzer()

def article_lemonde_sentiment(date_deb,date_fin, nombre_de_page, mot,sujet):
    listea = []
    listesent = []
    date_deb_link = str(date_deb.day)+'%2F'+str(date_deb.month)+'%2F'+str(date_deb.year)
    date_fin_link = str(date_fin.day)+'%2F'+str(date_fin.month)+'%2F'+str(date_fin.year)
    #on rentre le mois et l'année
    for nb in range(1,nombre_de_page+1):
        req = rq.get(f"""https://www.lemonde.fr/recherche/?search_keywords={sujet}&start_at={date_deb_link}&end_at={date_fin_link}
                     &search_sort=relevance_desc&page={nb}""").text
        bsreq = bs(req,'lxml')
        for a in bsreq.find_all('a',{'class':'teaser__link'}):
            listea.append(a.get('href'))
 
    for url in listea:
        req = rq.get(url).text
        bsreq = bs(req,'lxml')
        string = ''
        for b in bsreq.find_all('p',{'class':'article__paragraph'}):
            for k in b.strings:
                string+= k
        if mot in string:
            st.write(string)
            st.write('\n\n', url, '\n\n')
            listesent.append(float(analyzer.polarity_scores(string)['compound']))
    return(np.mean(listesent))
