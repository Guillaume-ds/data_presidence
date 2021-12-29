import streamlit as st
from streamlit_agraph import agraph,Node,Edge,Config
import snscrape.modules.twitter as sntwitter

import datetime as dt
from dateutil.relativedelta import relativedelta
import altair as alt
import pandas as pd 
from math import floor
from data import hr,vspace,tweets,candidats

def page_generale():
    candidats = pd.read_csv('Static\candidats.csv')
    #------------------------------------------------Sidebar---------------------------------------------------------
    st.sidebar.markdown(hr,unsafe_allow_html = True)
    liste_courants = list(candidats['Courant'].unique())
    liste_couleur = list(candidats['Couleur'].unique())
    courants = st.sidebar.multiselect('Choix des courants politiques',liste_courants,liste_courants)
    statut = st.sidebar.multiselect('Choix du statut',candidats['Statut'].unique(),"En course")
    
    #------------------------------------------------Dates---------------------------------------------------------
       
    date_premier_tour = dt.date(2022,4,10)
    delta_premier_tour = (date_premier_tour-dt.date.today()).days  
    date_election = dt.date(2022,4,24)
    delta_election = (date_election-dt.date.today()).days
    
    col1,col2,col3 = st.columns([3,1,3])
    col1.markdown(f"""<h1 style='text-align: center; font-weight:bold; margin-bottom:2px;'>
                    J-{delta_premier_tour} </h1>""",unsafe_allow_html=True)
    col1.markdown(f"""<h4 style='text-align: center; font-weight:bold; margin-bottom:10px;'>
                    Avant le premier tour </h4>""",unsafe_allow_html=True)
    

    col3.markdown(f"""<h1 style='text-align: center; font-weight:bold; margin-bottom:2px;'>
                    J-{delta_election} </h1>""",unsafe_allow_html=True)
    col3.markdown(f"""<h4 style='text-align: center; font-weight:bold; margin-bottom:10px;'>
                    Avant le résultat des élections </h4>""",unsafe_allow_html=True)

    st.markdown(vspace, unsafe_allow_html=True)
    st.markdown(vspace, unsafe_allow_html=True)
    
    #---------------------------------------------------------Metric---------------------------------------------------------
    
    
    
    
    
    
    #----------------------------------------------------Agraph graphique----------------------------------------------------
    st.markdown(f"""<h4 style='text-align: center; font-weight:bold; margin-bottom:0px;'>
                    Les candidats et leurs partis </h4>""",unsafe_allow_html=True)
    candidats_analyse = candidats.loc[(candidats.Statut.isin(statut)) & (candidats.Courant.isin(courants))].reset_index()  
     
    nodes_courants=[] 
    nodes_courants = [Node(id=i,label=str(i),
                           color = liste_couleur[index],
                           size=800) for index,i in enumerate(liste_courants)]
    
    nodes_candidats=[]
    nodes_candidats = [Node(id=candidats_analyse.loc[i,"Nom"],
                            label=candidats_analyse.loc[i,"Nom"],
                            size=400,
                            color=candidats_analyse.loc[i,"Couleur"]) for i in range(len(candidats_analyse))]
    
    nodes_courants.extend(nodes_candidats)
    nodes=[]
    nodes.extend(nodes_courants)

    edges = [Edge(source=candidats_analyse.loc[i,"Nom"],
                  target=candidats_analyse.loc[i,"Courant"]) for i in range(len(candidats_analyse))]
    
    edges_courants = [Edge(source=liste_courants[i],target=liste_courants[i+1],color="lightgrey",type="CURVE_SMOOTH") for i in range(len(liste_courants)-1)]
    
    edges.extend(edges_courants)
    
    config = Config( 
                width=1000,
                height=800,
                directed=False,
                nodeHighlightBehavior=True, 
                graphviz_config={"rankdir": liste_courants, "ranksep":0, "nodesep": 0},
                highlightColor="#F7A7A6", 
                collapsible=False,
                node={'labelProperty':'label'},
                link={'labelProperty': 'label', 'renderLabel': True},
                initialZoom=1.2,
                staticGraphWithDragAndDrop=False,
                staticGraph=False,
                ) 

    
    col1,col2,col3=st.columns([2,10,1])
    with col2:
        return_value = agraph(nodes=nodes, 
                      edges=edges, 
                      config=config)
   
    #----------------------------------------------------Tweeter----------------------------------------------------
    st.markdown(f"""<h4 style='text-align: center; font-weight:bold; margin-bottom:10px;'>
                    Les chiffres de Tweeter </h4>""",unsafe_allow_html=True)
    
    
    
    comptes_twitter = pd.read_csv("Static\comptes_twitter.csv")
    tweets_candidats = pd.DataFrame({
        "Candidat":[],
        "Date":[],
        "Nb de likes":0})

    for i in range(len(comptes_twitter)):
        compte_twitter = comptes_twitter.loc[i,"Compte Twitter"]            
        for tweet in sntwitter.TwitterSearchScraper(f'since:2021-12-01 from:{compte_twitter}').get_items():
            tweets_candidats = tweets_candidats.append({
                "Candidat":tweet.user.username,
                "Date":tweet.date,
                "Nb de likes":tweet.likeCount,},ignore_index=True)

    st.write(tweets_candidats)
    tweets_candidats.to_csv('Static/tweets_candidats.csv')
    tweets_list=[]

    obtenir_les_tweets = st.button('Scrapper tweeter')
    if obtenir_les_tweets:    
        for nom in candidats['Nom']: 
            for tweet in sntwitter.TwitterSearchScraper(f'{nom} since:2021-12-01 until:2021-12-28 lang:fr').get_items():
                tweets_list.append([nom, tweet.date, tweet.content,tweet.likeCount])
            st.write(nom)
    
    tweets_df = pd.DataFrame(tweets_list, columns=['Candidat', 'Date', 'Text', 'Likes'])
        
    nb_tweets=0
    obtenir_les_tweets2 = st.button('Scrapper tweeter2')
    if obtenir_les_tweets2:    
        for nom in candidats['Nom'][:1]: 
            for tweet in sntwitter.TwitterSearchScraper(f'{nom} since:2021-12-27 until:2021-12-28 lang:fr').get_items():
                tweets_list.append([nom, tweet.date, tweet.content,tweet.likeCount])
            st.write(nom,tweets_list)
    
    #tweets_df = pd.DataFrame(tweets_list, columns=['Candidat', 'Date', 'Text', 'Likes'])
    
    