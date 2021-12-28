import pandas as pd
import datetime as dt
from numpy import random

import datetime as dt


hr = "<hr style=' text-align : center; border-color : grey; margin-top: 15px; margin-bottom: 15px;'>"
vspace = "<hr style=' text-align : center; border-color : rgba(0,0,0,0); margin-top: 15px; margin-bottom: 15px;'>"

candidats = pd.read_csv("Static/candidats.csv")

def color_candidat(courant):
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
      
#candidats['Couleur']=list(map(color_candidat,candidats['Courant']))






     
                      
tweets = pd.DataFrame({'Date': [dt.date(2021,11,28), dt.date(2021,11,28), dt.date(2021,11,28),dt.date(2021,11,28),dt.date(2021,11,28),
                                dt.date(2021,11,29), dt.date(2021,11,29), dt.date(2021,11,29),dt.date(2021,11,29),dt.date(2021,11,29),
                                dt.date(2021,11,30), dt.date(2021,11,30), dt.date(2021,11,30),dt.date(2021,11,30),dt.date(2021,11,30),
                                dt.date(2021,12,1),dt.date(2021,12,1),dt.date(2021,12,1),dt.date(2021,12,1),dt.date(2021,12,1),
                                dt.date(2021,12,2),dt.date(2021,12,2),dt.date(2021,12,2),dt.date(2021,12,2),dt.date(2021,12,2),
                                dt.date(2021,12,3),dt.date(2021,12,3),dt.date(2021,12,3),dt.date(2021,12,3),dt.date(2021,12,3),
                                dt.date(2021,12,4),dt.date(2021,12,4),dt.date(2021,12,4),dt.date(2021,12,4),dt.date(2021,12,4),
                                dt.date(2021,12,5),dt.date(2021,12,5),dt.date(2021,12,5),dt.date(2021,12,5),dt.date(2021,12,5),
                                dt.date(2021,12,6),dt.date(2021,12,6),dt.date(2021,12,6),dt.date(2021,12,6),dt.date(2021,12,6),],
                          'Candidat': ['Macron', 'Zemmour', 'Pécresse','Hidalgo','Mélanchon',
                                      'Macron', 'Zemmour', 'Pécresse','Hidalgo','Mélanchon',
                                      'Macron', 'Zemmour', 'Pécresse','Hidalgo','Mélanchon',
                                      'Macron', 'Zemmour', 'Pécresse','Hidalgo','Mélanchon',
                                      'Macron', 'Zemmour', 'Pécresse','Hidalgo','Mélanchon',
                                      'Macron', 'Zemmour', 'Pécresse','Hidalgo','Mélanchon',
                                      'Macron', 'Zemmour', 'Pécresse','Hidalgo','Mélanchon',
                                      'Macron', 'Zemmour', 'Pécresse','Hidalgo','Mélanchon',
                                      'Macron', 'Zemmour', 'Pécresse','Hidalgo','Mélanchon',],
                          'Tweets': [189, 90, 80, 65, 98,
                                    201, 190,  92, 78, 85,
                                    127, 150, 91, 86, 102,
                                    147, 157, 95, 98, 107, 
                                    125, 130, 96, 105, 98,
                                    128, 135, 76, 147, 102,
                                    135, 147, 106, 105, 79,
                                    142, 139, 125, 84, 106,
                                    112, 123, 102, 153, 128]})