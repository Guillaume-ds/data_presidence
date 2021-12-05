import streamlit as st
from data import vspace,tweets
import datetime as dt
from dateutil.relativedelta import relativedelta
import altair as alt
from math import floor

def page_generale():
    st.markdown(vspace, unsafe_allow_html=True)
    
    date_election = dt.date(2022,4,24)
    delta_election = (date_election-dt.date.today()).days
    

    st.markdown(f"""<h1 style='text-align: center; font-weight:bold; margin-bottom:2px;'>
                    J-{delta_election} </h1>""",unsafe_allow_html=True)
    st.markdown(f"""<h4 style='text-align: center; font-weight:bold; margin-bottom:10px;'>
                    Avant le résultat des élections </h4>""",unsafe_allow_html=True)

    st.markdown(vspace, unsafe_allow_html=True)
    st.markdown(vspace, unsafe_allow_html=True)
    
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