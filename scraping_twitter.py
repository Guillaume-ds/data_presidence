import snscrape.modules.twitter as sntwitter
import pandas as pd

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