import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from geopy.geocoders import Nominatim 

#And then import the database
df = pd.read_csv('CLIWOC15.csv', low_memory=False)
#we remove Nan entries for the columns we are interested in studying

df5=df.dropna(subset = ['Lon3', 'Lat3', 'UTC', 'VoyageIni','WindForce','StateSea','Weather','VoyageFrom', 'VoyageTo', 'VoyageIni'])
m5=df5[df5['Nationality']=='British']
m7=df5[df5['Nationality']=='Spanish']
m9=df5[df5['Nationality']=='Dutch']
m11=df5[df5['Nationality']=='French']

   path_Brit_CLIM=m5[['ShipName','Lon3', 'Lat3', 'UTC', 'VoyageIni','WindForce','StateSea','Weather','VoyageFrom', 'VoyageTo', 'VoyageIni']]
   path_Du_CLIM=m9[['ShipName','Lon3', 'Lat3', 'UTC', 'VoyageIni','WindForce','StateSea','Weather','VoyageFrom', 'VoyageTo', 'VoyageIni']]
   path_Fr_CLIM=m11[['ShipName','Lon3', 'Lat3', 'UTC', 'VoyageIni','WindForce','StateSea','Weather','VoyageFrom', 'VoyageTo', 'VoyageIni']]
   path_Sp_CLIM=m7[['ShipName','Lon3', 'Lat3', 'UTC', 'VoyageIni','WindForce','StateSea','Weather','VoyageFrom', 'VoyageTo', 'VoyageIni']]
    #path_Brit1=m5[['ShipName','Lon3', 'Lat3', 'UTC', 'VoyageIni','WindForce','StateSea','Weather','VoyageFrom', 'VoyageTo', 'VoyageIni']]
    #groupedPath_Brit=path_spanish.groupby('VoyageIni')
    #for name, group in groupedPath:
    #    if group.size<2:
    #        continue
    #    group.sort_values(by='UTC', inplace=True)
    #    group.sort_values(by='VoyageFrom', inplace=True)
    #    group.sort_values(by='VoyageTo', inplace=True)
        
#sm=pd.DataFrame(groupedPath_Brit) 
#m6=m5  
m6=path_Brit_CLIM
m8=path_Sp_CLIM
m10=path_Du_CLIM    
m12=path_Fr_CLIM


       

