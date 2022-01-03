import pandas as pd

#-------------------------------------------------Mardown---------------------------------------------------
hr = "<hr style=' text-align : center; border-color : grey; margin-top: 15px; margin-bottom: 15px;'>"
vspace = "<hr style=' text-align : center; border-color : rgba(0,0,0,0); margin-top: 15px; margin-bottom: 15px;'>"
vspace2 = "<hr style=' text-align : center; border-color : rgba(0,0,0,0); margin-top: 30px; margin-bottom: 30px;'>"
#--------------------------------------------------Files------------------------------------------------------

tweets_candidats = pd.read_csv('Static/tweets_candidats.csv')
comptes_twitter = pd.read_csv('Static/comptes_twitter.csv')

#-------------------------------------------------Functions---------------------------------------------------
def couleur_candidat():
      candidats = pd.read_csv("Static/candidats.csv")
      def couleur(courant):
            if courant == "Gauche radicale":
                  return "red"
            elif courant == "Gauche socialiste":
                  return "deeppink"
            elif courant == "Gauche écologiste":
                  return "green"
            elif courant == "Centre":
                  return "orange"
            elif courant == "Droite":
                  return "blue"
            elif courant == "Droite souverainiste":
                  return "royalblue"
            elif courant == "Divers":
                  return "wheat"
                 
      candidats['Couleur']=candidats['Courant'].apply(lambda x: couleur(x))   
      candidats.to_csv('Static/candidats.csv',index=False)

#------------------------------------------------------------------Autre------------------------------------------------

french_stopwords = ['d', 'du', 'de', 'la', 'des', 'le', 'et','qu','y', 'est', 'elle', 'une','n', 'en', 'que', 'aux', 'qui', 'ces', 'les', 'dans', 'sur', 'l', 'un', 'pour', 'par', 'il', 'ou', 'à', 'ce', 'a', 'sont', 'cas', 'plus', 'leur', 'se', 's', 'vous', 'au', 'c', 'aussi', 'toutes', 'autre', 'comme']
    
