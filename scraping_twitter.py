from dateutil.relativedelta import relativedelta
import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime as dt
import streamlit as st
import time



def queryTweet(date_deb = None,date_fin=dt.date.today()):
    """
    Scrap l'ensemble des tweets des candidats 
    """
    comptes_twitter = pd.read_csv("Static/comptes_twitter.csv") #liste des comptes à scrapper 
    tweets_candidats = pd.read_csv("Static/tweets_candidats.csv") #liste actuelle des tweets (pour avoir la date max)
    if date_deb == None:    
        date_deb = dt.datetime.strptime(max(tweets_candidats['Jour']),"%Y-%m-%d").date()+relativedelta(days=1)
    for i in range(len(comptes_twitter)):
        compte_twitter = comptes_twitter.loc[i,"Compte Twitter"]            
        for tweet in sntwitter.TwitterSearchScraper(f'since:{date_deb} until:{date_fin} from:{compte_twitter}').get_items():
            candidat = comptes_twitter.loc[comptes_twitter['Compte Twitter']==tweet.user.username]['Candidat'].item()
            tweets_candidats = tweets_candidats.append({                
                "Candidat":candidat,
                "Date":tweet.date,
                "Tweet":tweet.content,
                "Nb de likes":tweet.likeCount,
                "Jour": tweet.date.date(),
                "Compte Twitter":tweet.user.username,},ignore_index=True)
        comptes_twitter.loc[i,'Followers'] = tweet.user.followersCount
    tweets_candidats.to_csv('Static/tweets_candidats.csv',index=False)
    comptes_twitter.to_csv("Static/comptes_twitter.csv",index=False)
    time.sleep(60*60*24)
    
queryTweet()
    
    
def getfollowers():
    comptes_twitter = pd.read_csv("Static/comptes_twitter.csv")
    comptes_twitter['Followers'] = comptes_twitter["Compte Twitter"]
    for i in range(len(comptes_twitter)):
        compte_twitter = comptes_twitter.loc[i,"Compte Twitter"] 
        st.write(compte_twitter)       
        for j,tweet in enumerate(sntwitter.TwitterSearchScraper(f'since:2021-12-15 from:{compte_twitter}').get_items()):
            if j>=1:
                break
            comptes_twitter.loc[i,'Followers'] = tweet.user.followersCount
            
    comptes_twitter.to_csv("Static/comptes_twitter.csv",index=False)


















def scraptweets_candidat(date_deb,date_fin,compte_twitter):
    """
    Scrappe les tweets d'un candidat et les tweets à propos d'un candidat
    """
    deb = date_deb.strftime("%Y-%m-%d") #Passe les dates du format datetime au format str
    fin = date_fin.strftime("%Y-%m-%d")
    tweets_list1 = []
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'since:{deb} until:{fin} from:{compte_twitter}').get_items()):
            if i>100:
                break
            tweets_list1.append([tweet.user.username, tweet.date, tweet.content,tweet.likeCount])
            
        # Creating a dataframe from the tweets list above 
    tweets_df1 = pd.DataFrame(tweets_list1, columns=['Candidat', 'Date', 'Text', 'Likes'])
    return tweets_df1



def changement_nom(x):
    tweets_candidats = tweets_candidats.rename(columns={'Candidat':'Compte Twitter'}).drop("Unnamed: 0",axis=1)
    tweets_candidats['Candidat']= [0]*2003
    a = comptes_twitter[comptes_twitter['Compte Twitter']=='Anne_Hidalgo'].index
    st.write(comptes_twitter.loc[a,'Candidats'].item())
    
    for i in range(len(tweets_candidats)):
        compte = tweets_candidats.loc[i,'Compte Twitter']
        tweets_candidats.loc[i,'Candidat'] = comptes_twitter[comptes_twitter['Compte Twitter']==compte]['Candidats'].item()
    return None