import streamlit as st
from streamlit_agraph import agraph,Node,Edge,Config

import datetime as dt
from dateutil.relativedelta import relativedelta
import altair as alt

from math import floor
from data import hr,vspace,tweets,candidats

def page_generale():
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
        
    selection = alt.selection_multi(fields=['Candidat'], bind='legend')
        
    line_tweets = alt.Chart(tweets).mark_line().encode(
            alt.X("yearmonthdate(Date):T"),
            alt.Y("Tweets:Q"),
            alt.Color('Candidat:N'),
            opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
            ).add_selection(
            selection
            )
            
    st.altair_chart(line_tweets.interactive()
                    .properties(title = 'Nombre de tweets mentionnant chaque candidats'),
                    use_container_width = True)

    st.markdown(vspace, unsafe_allow_html=True)
    st.markdown(vspace, unsafe_allow_html=True)
    st.markdown(f"""<h4 style='text-align: center; font-weight:bold; margin-bottom:10px;'>
                    Les chiffres du jours </h4>""",unsafe_allow_html=True)
    
    col1,col2,col3,col4 = st.columns(4)
    today_tweets = tweets[tweets.Date==dt.date.today()] 
    yesterday_tweets = tweets[tweets.Date==dt.date.today()-relativedelta(days=1)] 
    max_tweet = max(today_tweets['Tweets'])
    candidat_max_tweet = today_tweets.loc[today_tweets.Tweets == max_tweet,'Candidat'].item()      
    col1.metric(label = f"Max tweet : {candidat_max_tweet}",
                value = max(today_tweets['Tweets']),
                delta = max_tweet - yesterday_tweets.loc[yesterday_tweets.Candidat == candidat_max_tweet]['Tweets'].item())
    col2.metric(label = "Nombre total de tweets",
                value = sum(today_tweets['Tweets']),
                delta = sum(today_tweets['Tweets']) 
                        - sum(yesterday_tweets['Tweets']))
    col3.metric(label = "Nombre moyen de tweets par candidat",
                value = floor(today_tweets['Tweets'].mean()),
                delta = floor(today_tweets['Tweets'].mean() - yesterday_tweets['Tweets'].mean()))
    col4.metric(label = "Indicateur d'intérêt pour la campagne",
                value = "Elevé")
    
    def groupe_politique(x):
        if x in ['Mélanchon']:
            return "Extrème gauche"
        elif x in ['Hidalgo']:
            return "Gauche"
        elif x in ["Macron"]:
            return "Centre"
        elif x in ["Pécresse"]:
            return "Droite"
        elif x in ['Le Pen',"Zemmour"]:
            return "Extreme droite"
    
    def couleur_politique(x):
        if x in ['Mélanchon']:
            return "rgba(250,10,15,1)"
        elif x in ['Hidalgo']:
            return "rgba(245,40,150,1)"
        elif x in ["Macron"]:
            return "rgba(250,175,11,1)"
        elif x in ["Pécresse"]:
            return "rgba(10,110,250,1)"
        elif x in ['Le Pen',"Zemmour"]:
            return "rgba(5,10,165,1)"
    
    tweets['Bord politique'] = list(map(groupe_politique,tweets['Candidat']))
    tweets['Couleur politique'] = list(map(couleur_politique,tweets['Candidat']))
    bords_politique = ["Extrème gauche","Gauche","Centre","Droite","Extreme droite"]
    tweets['Ordre'] = tweets['Bord politique'].apply(lambda x: bords_politique.index(x))
    
    st.markdown(vspace, unsafe_allow_html=True)
    st.markdown(vspace, unsafe_allow_html=True)
    st.markdown(f"""<h4 style='text-align: center; font-weight:bold; margin-bottom:10px;'>
                    Répartition des tweets par bord politique </h4>""",unsafe_allow_html=True)
    
    repartition_parti = alt.Chart(tweets).mark_bar().encode(
        alt.X('Tweets',stack="normalize"),
        alt.Y("yearmonthdate(Date):T"),
        color = alt.Color('Couleur politique:N',scale=None),
        tooltip = ['Bord politique','Tweets'],
        order = "Ordre:N"
    )
    st.altair_chart(repartition_parti,use_container_width = True)
    
    