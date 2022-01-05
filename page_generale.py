import streamlit as st

from streamlit_agraph import agraph,Node,Edge,Config

import datetime as dt
from dateutil.relativedelta import relativedelta
import altair as alt
import pandas as pd 
from millify import prettify

from data import hr,vspace,tweets_candidats


def page_generale():
    #-------------------------------------------------Data Candidats------------------------------------------------------   

    @st.cache
    def donnees_candidats():
        #charge le fichier candidat, une fois par session
        candidats = pd.read_csv("Static/candidats.csv")
        liste_courants = list(candidats['Courant'].unique())
        liste_couleurs = list(candidats['Couleur'].unique())
        return candidats, liste_courants,liste_couleurs
    
    candidats,liste_courants,liste_couleurs = donnees_candidats()
    if type(tweets_candidats['Jour'][0]) == str:
        tweets_candidats['Jour'] = tweets_candidats['Jour'].apply(lambda x : dt.datetime.strptime(x,"%Y-%m-%d").date()) 
        
    #---------------------------------------------------Sidebar-----------------------------------------------------------
    
    st.sidebar.markdown(hr,unsafe_allow_html = True)
    
    courants = st.sidebar.multiselect('Choix des courants politiques',liste_courants,liste_courants)
    statut = st.sidebar.multiselect('Choix du statut',candidats['Statut'].unique(),"En course")  
      
    #---------------------------------------------------Dates------------------------------------------------------------
    
    @st.cache
    def calcul_dates_elections():
        #calcul les ecarts avec les deux tours des elections 
        date_premier_tour = dt.date(2022,4,10)
        delta_premier_tour = (date_premier_tour-dt.date.today()).days  
        date_election = dt.date(2022,4,24)
        delta_election = (date_election-dt.date.today()).days
        return delta_premier_tour,delta_election
    
    delta_premier_tour,delta_election = calcul_dates_elections()
    
    col1,col2,col3 = st.columns([3,1,3])
    col1.markdown(f"""<h2 style='text-align: center; font-weight:bold; margin-bottom:2px;'>
                    J-{delta_premier_tour} </h2>""",unsafe_allow_html=True)
    col1.markdown(f"""<h5 style='text-align: center; font-weight:bold; margin-bottom:10px;'>
                    Avant le premier tour </h5>""",unsafe_allow_html=True)
    

    col3.markdown(f"""<h2 style='text-align: center; font-weight:bold; margin-bottom:2px;'>
                    J-{delta_election} </h2>""",unsafe_allow_html=True)
    col3.markdown(f"""<h5 style='text-align: center; font-weight:bold; margin-bottom:10px;'>
                    Avant le résultat des élections </h5>""",unsafe_allow_html=True)

    st.markdown(vspace, unsafe_allow_html=True)
    st.markdown(vspace, unsafe_allow_html=True)
    st.markdown(vspace, unsafe_allow_html=True)
    #----------------------------------------------------Tweeter----------------------------------------------------
    
    st.markdown(f"""<h2 style='text-align: center; font-weight:bold; margin-bottom:-10px;'>
                    Les chiffres de Tweeter </h2>""",unsafe_allow_html=True)
    
    st.markdown(f"""<p style='text-align: center; margin-bottom:15px; margin-top:-10px'>
                    Données collectées depuis le 01/01/2021 - choix des bornes temporelles ci-dessous
                    </p>""",unsafe_allow_html=True)
    
    st.markdown(vspace, unsafe_allow_html=True)
    st.markdown(vspace, unsafe_allow_html=True)
    
    col1,col2,col3,col4,col5=st.columns([1,1,1,1,1])
    dat_deb = col2.date_input('Date de début de l\'analyse',
                              min_value=dt.date(2021,1,1),
                              max_value=dt.date.today(),
                              value=dt.date.today()-relativedelta(days=30))
    dat_fin = col4.date_input('Date de fin de l\'analyse',
                              min_value=dat_deb,
                              max_value=dt.date.today())
    
    tweets_candidats_analyse = tweets_candidats.loc[(tweets_candidats.Jour>=dat_deb)&(tweets_candidats.Jour<=dat_fin)]
    
    st.markdown(vspace, unsafe_allow_html=True)
    st.markdown(vspace, unsafe_allow_html=True)
    
    selection = alt.selection_multi(fields=['Candidat'], bind='legend')
        
    line_tweets = alt.Chart(tweets_candidats_analyse).mark_line().encode(
            alt.X("yearmonthdate(Date):T"),
            alt.Y("count(Tweets):Q"),
            alt.Color('Candidat:N',legend=alt.Legend(title="Candidats (cliquer)")),
            tooltip = ['Candidat','count(Tweets):Q'],
            opacity=alt.condition(selection, alt.value(1), alt.value(0.1))
            ).add_selection(
            selection
            )

    st.altair_chart(line_tweets.interactive()
                    .properties(title = 'Nombre de tweets par jour par candidat'),
                    use_container_width = True)
    
    st.markdown(vspace, unsafe_allow_html=True)
    st.markdown(vspace, unsafe_allow_html=True)    
    
    bar_tweets = alt.Chart(tweets_candidats_analyse).mark_bar().encode(
        alt.X("Candidat:N",
              axis=alt.Axis(labelAngle=-10),
              sort=alt.EncodingSortField(field="Candidat", op="count", order='descending')),
        alt.Y("count(Tweets):Q"),
        tooltip = ['Candidat',alt.Tooltip('count(Tweets):Q',title='Total de tweets')],
    )
    
    st.altair_chart(bar_tweets.interactive()
                    .properties(title = f'Nombre total de tweets par candidat du {dat_deb} au {dat_fin}'),
                    use_container_width = True)
    
    st.markdown(vspace, unsafe_allow_html=True)
    st.markdown(vspace, unsafe_allow_html=True) 
    
    box_likes = alt.Chart(tweets_candidats_analyse).mark_boxplot(extent='min-max').encode(
                    alt.X('Candidat:O',
                          axis=alt.Axis(labelAngle=-10)),
                    y='Nb de likes:Q',
                    color=alt.Color('Candidat:N',legend=None),)
    
    st.altair_chart(box_likes.interactive()
                    .properties(title = f'Distribution du nombre de likes du {dat_deb} au {dat_fin}')
                    ,use_container_width = True)
    #---------------------------------------------------------Metric---------------------------------------------------------
    st.markdown(vspace, unsafe_allow_html=True)
    st.markdown(vspace, unsafe_allow_html=True)
    
    st.markdown(f"""<p style='text-align: center; margin-bottom:15px; margin-top:-10px'>
                    Les chiffres de la semaine
                    </p>""",unsafe_allow_html=True)
    
    @st.cache
    def chiffres_tweet_semaine():           
        tweets_jour = tweets_candidats[tweets_candidats['Jour']==dt.date.today()-relativedelta(days=1)]
        tweet_hier = tweets_candidats[tweets_candidats['Jour']==dt.date.today()-relativedelta(days=2)]
        tweet_semaine = tweets_candidats[tweets_candidats['Jour']>=dt.date.today()-relativedelta(days=7)]
        tweet_semaine_passee = tweets_candidats[(tweets_candidats['Jour']>=dt.date.today()-relativedelta(days=14)) &
                                        (tweets_candidats['Jour']<dt.date.today()-relativedelta(days=7))]
        return tweets_jour,tweet_hier,tweet_semaine,tweet_semaine_passee
    
    tweets_jour,tweet_hier,tweet_semaine,tweet_semaine_passee =  chiffres_tweet_semaine()
    
    col1,col2,col3,col4 = st.columns(4)
    
    col1.metric(label=f"Nb de tweets du {dt.date.today()}",
                value = len(tweets_jour),
                delta = len(tweets_jour) - len(tweet_hier))
    
    col2.metric(label=f"Nb de likes du {dt.date.today()}",
                value = prettify(int(tweets_jour['Nb de likes'].sum()),' '),
                delta = prettify(int(tweets_jour['Nb de likes'].sum()) - int(tweet_hier['Nb de likes'].sum()),' '))
    
    col3.metric(label="Nb de tweets de la semaine",
                value = len(tweet_semaine),
                delta = len(tweet_semaine) - len(tweet_semaine_passee))
    
    col4.metric(label="Nb de likes total de la semaine",
                value = prettify(int(tweet_semaine['Nb de likes'].sum()),' '),
                delta = prettify(int(tweet_semaine['Nb de likes'].sum()) - int(tweet_semaine_passee['Nb de likes'].sum()),' '))
 
    
    #----------------------------------------------------Agraph graphique----------------------------------------------------
    st.markdown(vspace, unsafe_allow_html=True)
    st.markdown(vspace, unsafe_allow_html=True)
    st.markdown(f"""<h4 style='text-align: center; font-weight:bold; margin-bottom:0px;'>
                    Les candidats et leurs partis </h4>""",unsafe_allow_html=True)
    
    @st.cache 
    def creation_agraph(statut,courants):
        
        candidats_analyse = candidats.loc[(candidats.Statut.isin(statut)) & (candidats.Courant.isin(courants))].reset_index()  
        
        nodes_courants=[] 
        nodes_courants = [Node(id=i,label=str(i),
                            color = liste_couleurs[index],
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
        
        return nodes, edges,config

    nodes, edges,config = creation_agraph(statut,courants)
    with st.expander("Voir les partis et les candidats"):
        
        return_value = agraph(nodes=nodes, 
                    edges=edges, 
                    config=config)
   
