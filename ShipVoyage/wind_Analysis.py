
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import nltk
import re
import datetime
import matplotlib.dates as mdates
ship_data=pd.read_csv('CLIWOC15.csv')
df5=ship_data.dropna(subset=['Nationality','Lon3', 'Lat3', 'UTC', 'VoyageIni','VoyageTo','VoyageFrom'])
path_spanish=(df5[df5['Nationality']=='Spanish'][['Lon3', 'Lat3', 'UTC', 'VoyageIni','VoyageTo','VoyageFrom','WindForce']])




gentle={'vacilante','recio','rafagas','poco','pardo','pacifico','no ha habido','moderado','flojo','flojito','escaso','endeble','debil','de 8 y 9 millas','de 6 y 7 millas','calmoso','calmo','calma muerta','calma','brisado','abonanzado','abonanzando','brisa','abonanzo','abrisado','a fugado','apacible','apaciguado','arreciando','aventolinado','benigno','blandura','bonancible','bonanza'}

medium={'vivo','vivito','recio','fuertecito','fuerte','fresquito','fresquecito','frescote','fresco','frescachonazo','frescachon','duro','durito','de toda vela larga','de toda vela','de proa','de alta vela','altivo'}

Strong={'turbonada','tormentoso como especie de huracan','tormentoso','tormenta','temporal','tempestuoso','tempestad','rieguroso','mucho','muchisimo','intolerable','intenso','insufrible','insoportable','incostante','inaguantable','impetuoso','huracanado','huracan','furioso','furia','fugadas huracanadas','fuerza','fortisimo','ferocidad extraordinaria','demasiado','ahuracanado','alterados','amenazante','aturbonado','borrascoso'}

indexes=[]
for index, row in path_spanish.iterrows():
    sentence = row.WindForce 
    sentence=sentence.lower()
    if sentence in Strong:
        indexes.append(index)
        
lon_calm=[]
lat_calm=[]
UTC_calm=[]
wind_force=[]
for j in indexes:
    lat_calm.append(df5['Lat3'].iat[j])
    lon_calm.append(df5['Lon3'].iat[j])
    UTC_calm.append(df5['UTC'].iat[j])

lon_calm1=np.asarray(lon_calm)
lat_calm1=np.asarray(lat_calm)
UTC_calm1=np.asarray(UTC_calm)
    
    
    