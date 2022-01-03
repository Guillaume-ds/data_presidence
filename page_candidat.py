import streamlit as st
import altair as alt

from data import vspace,vspace2,hr,comptes_twitter,tweets_candidats
import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd
from millify import prettify
from wordcloud import WordCloud

from data import french_stopwords

from nltk.tokenize import RegexpTokenizer


import re 



def page_candidat():
    #------------------------------------------------Sidebar---------------------------------------------------------
    st.sidebar.markdown(hr,unsafe_allow_html = True)
    st.sidebar.markdown("<h2>Paramètres de l'analyse</h2>",unsafe_allow_html = True)
    choix_candidat = st.sidebar.selectbox("Candidat à analyser",
                                        comptes_twitter['Candidat'])
    
    st.sidebar.markdown(vspace,unsafe_allow_html = True)
    date_deb = st.sidebar.date_input("Choisir une date de début",max_value=dt.date.today()-relativedelta(days=3),value=dt.date.today()-relativedelta(days=30))   
    date_fin = st.sidebar.date_input("Choisir une date de fin",min_value=date_deb+relativedelta(days=1))
    
    st.sidebar.markdown(vspace,unsafe_allow_html = True)   
    
    
    @st.cache(suppress_st_warning=True)
    def get_candidats():
        """
        Le fichier ne bouge pas, pas besoin de le lire à chaque fois 
        """
        candidats = pd.read_csv("Static/candidats.csv")
        return candidats
    
    candidats = get_candidats()
    #------------------------------------------------Photo---------------------------------------------------------
    st.markdown(vspace,unsafe_allow_html = True)
    
    col1,col2,col3 = st.columns([2,1,2])
    col1.image(f"Static/img_candidats/{choix_candidat}.jpg",use_column_width=True)
    col3.markdown(f"""<h2 style='text-align: left; font-weight:bold; margin-bottom:50px; margin-top:0px'>
                    {choix_candidat} </h2>""",unsafe_allow_html=True)
    
    @st.cache 
    def infos_candidat(choix_candidat):
        #utilisation du cache pour éviter le rerun lors du changement de date
        parti = candidats.loc[candidats['Nom']==choix_candidat]['Parti'].item()
        courant = candidats.loc[candidats['Nom']==choix_candidat]['Courant'].item()
        nb_candidatures = int(candidats.loc[candidats['Nom']==choix_candidat]['Nb candidatures'].item()) 
        compte_twitter = comptes_twitter.loc[comptes_twitter['Candidat']==choix_candidat]['Compte Twitter'].item()
        followers = comptes_twitter.loc[comptes_twitter['Candidat']==choix_candidat]['Followers'].item()
        return parti,nb_candidatures,courant,compte_twitter,followers
    
    parti,nb_candidatures,courant,compte_twitter,followers = infos_candidat(choix_candidat)
    
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
    col3.markdown(f"""<h4 style='text-align: left; font-weight:bold; margin-bottom:10px;'>
                    Nombre de followers : {prettify(followers,' ')} </h4>""",unsafe_allow_html=True)

    tweet_count = col3.empty()
   
    st.markdown(vspace2,unsafe_allow_html = True)
    
    #------------------------------------------------Analyse twitter---------------------------------------------------------
    #------------------------------------------------likes twitter-----------------------------
    @st.cache
    def get_max_like(date_deb,date_fin,choix_candidat):
        if type(tweets_candidats.loc[1,'Jour'])==str: 
            tweets_candidats['Jour'] = tweets_candidats['Jour'].apply(lambda x : dt.datetime.strptime(x,"%Y-%m-%d").date())
            tweets_candidats_analyse = tweets_candidats.loc[(tweets_candidats['Candidat']==choix_candidat) 
                                                            & (tweets_candidats['Jour']>=date_deb)
                                                            & (tweets_candidats['Jour']<= date_fin)]
            
        else : 
            tweets_candidats_analyse = tweets_candidats.loc[(tweets_candidats['Candidat']==choix_candidat) 
                                                            & (tweets_candidats['Jour'] >= date_deb)
                                                            & (tweets_candidats['Jour'] <= date_fin)]
            
        tweet_max_like = tweets_candidats_analyse.loc[tweets_candidats_analyse['Nb de likes'] == max(tweets_candidats_analyse['Nb de likes'])]
        return tweets_candidats_analyse,tweet_max_like

    tweets_candidats_analyse,tweet_max_like = get_max_like(date_deb,date_fin,choix_candidat)
    
    with tweet_count.container():
        st.markdown(f"""<h4 style='text-align: left; font-weight:bold; margin-bottom:40px;'>
                    Nombre de tweets sur la période : {len(tweets_candidats_analyse)} </h4>""",unsafe_allow_html=True)
    
    st.markdown(f"""<h4 style='text-align : center; margin-bottom:25px'>
                Tweet le plus liké (le {tweet_max_like['Jour'].item()} avec {prettify(int(tweet_max_like['Nb de likes'].item()),' ')} likes)
                </h4>""", unsafe_allow_html = True)

    st.code(tweet_max_like.Tweet.item())
    st.markdown(vspace2,unsafe_allow_html = True)
    st.markdown(vspace,unsafe_allow_html = True)
    #------------------------------------------------Nb mots twitter-----------------------------
    
    @st.cache
    def wordcount_wordcloud(date_deb,date_fin,choix_candidat):
        
        tokenizer = RegexpTokenizer(r"[\w+]+")
        mots_tweets = pd.DataFrame(tweets_candidats_analyse['Tweet'].apply(lambda x : tokenizer.tokenize(re.sub(r"https\S+", "", x))))    
        mots_tweets['nb_mots_tweet'] = mots_tweets['Tweet'].apply(lambda x : len(x))
        mots_tweets['tweet_sw'] = mots_tweets['Tweet'].apply(lambda x : ' '.join([mot for mot in x if mot.lower() not in french_stopwords]))
        total_tweet = ' '.join(mots_tweets['tweet_sw'])
        word_count = WordCloud().process_text(total_tweet)
        
        return mots_tweets,word_count

    mots_tweets,word_count = wordcount_wordcloud(date_deb,date_fin,choix_candidat)
    
   
    bar = alt.Chart(mots_tweets).mark_bar().encode(
        x=alt.X('nb_mots_tweet:Q', 
                bin=alt.Bin(step=1),
                axis = alt.Axis(title="Nombre de mots par tweet (et moyenne)")),
        y=alt.Y('count()',
                axis = alt.Axis(title="Nombre de tweets")),
        tooltip = [alt.Tooltip('nb_mots_tweet:Q',title='Nombre de mots'),alt.Tooltip('count():Q',title='Nombre de tweets')]
    )

    rule = alt.Chart(mots_tweets).mark_rule(color='red').encode(
        x='mean(nb_mots_tweet):Q',
        size=alt.value(5)
    )

    st.altair_chart((bar+rule)
                    .interactive()
                    .properties(title = f'Distribution du nombre de tweet par nombre de mots'),
                    use_container_width = True)
    
    st.markdown(vspace2,unsafe_allow_html = True)    
    st.markdown(vspace2,unsafe_allow_html = True)
    
    #------------------------------------------------Word cloud twitter-----------------------------
        
    st.markdown(f"""<h4 style='text-align : center; margin-bottom:25px'>
                Mots les plus utilisés par {choix_candidat}
                </h4>""", unsafe_allow_html = True)
    
    nb_mots = st.slider("Nombre de mots à intégrer dans le nuage", min_value=10,max_value=50,value=30)
    st.markdown(vspace2,unsafe_allow_html = True)
    
    st.markdown(vspace,unsafe_allow_html = True)
    wc = WordCloud(background_color="white",max_words=nb_mots,width=800, height=400).fit_words(word_count)
    st.image(wc.to_array(),use_column_width=True) 
      

    
    