
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from geopy.geocoders import Nominatim 

#And then import the database
df = pd.read_csv('CLIWOC15.csv', low_memory=False)
#we remove Nan entries for the columns we are interested in studying
df1=df.dropna(subset = ['Lon3', 'Lat3', 'UTC', 'VoyageIni'])
df2=df.dropna(subset = ['VoyageFrom', 'VoyageTo', 'VoyageIni'])
ships = df1[df1['Nationality']=='Spanish']['ShipName'].unique()
m=ships
m2 = df1[df1['Nationality']=='British']['ShipName'].unique()
m3=df1[df1['Nationality']=='Dutch']['ShipName'].unique()
m4=df1[df1['Nationality']=='French']['ShipName'].unique()
m=list(m)

for j in m[:]:
    path_spanish=(df1[df1['ShipName']==j][['Lon3', 'Lat3', 'UTC', 'VoyageIni']])
    groupedPath=path_spanish.groupby('VoyageIni')
    for name, group in groupedPath:
        if group.size<2:
            continue
        group.sort_values(by='UTC', inplace=True)
        #draw path on the background
        x,y=group['Lon3'].tolist(),group['Lat3'].tolist()
    #print(j)

s=pd.DataFrame(groupedPath)
s2=pd.DataFrame(groupedPath2)
s3=pd.DataFrame(groupedPath3)
s4=pd.DataFrame(groupedPath4)
for j in m2[:]:
    path_British=(df1[df1['ShipName']==j][['Lon3', 'Lat3', 'UTC', 'VoyageIni']])
    groupedPath2=path_British.groupby('VoyageIni')
    for name2, group2 in groupedPath2:
        if group2.size<2:
            continue
        group2.sort_values(by='UTC', inplace=True)
        #draw path on the background
        x2,y2=group2['Lon3'].tolist(),group2['Lat3'].tolist()
for j in m3[:]:
    path_Dutch=(df1[df1['ShipName']==j][['Lon3', 'Lat3', 'UTC', 'VoyageIni']])
    groupedPath3=path_Dutch.groupby('VoyageIni')
    for name3, group3 in groupedPath3:
        if group3.size<2:
            continue
        group3.sort_values(by='UTC', inplace=True)
        #draw path on the background
        x3,y3=group3['Lon3'].tolist(),group3['Lat3'].tolist()
for j in m4[:]:
    path_French=(df1[df1['ShipName']==j][['Lon3', 'Lat3', 'UTC', 'VoyageIni']])
    groupedPath4=path_French.groupby('VoyageIni')
    for name4, group4 in groupedPath4:
        if group4.size<2:
            continue
        group4.sort_values(by='UTC', inplace=True)
        #draw path on the background
        x4,y4=group4['Lon3'].tolist(),group4['Lat3'].tolist()
df5=df.dropna(subset = ['Lon3', 'Lat3', 'UTC', 'VoyageIni','WindForce','StateSea','Weather','VoyageFrom', 'VoyageTo', 'VoyageIni'])
m5=df5[df5['Nationality']=='British']

    path_Brit=m5[['ShipName','Lon3', 'Lat3', 'UTC', 'VoyageIni','WindForce','StateSea','Weather','VoyageFrom', 'VoyageTo', 'VoyageIni']]
    path_Brit1=m5[['ShipName','Lon3', 'Lat3', 'UTC', 'VoyageIni','WindForce','StateSea','Weather','VoyageFrom', 'VoyageTo', 'VoyageIni']]
    groupedPath_Brit=path_spanish.groupby('VoyageIni')
    for name, group in groupedPath:
        if group.size<2:
            continue
        group.sort_values(by='UTC', inplace=True)
        group.sort_values(by='VoyageFrom', inplace=True)
        group.sort_values(by='VoyageTo', inplace=True)
        
sm=pd.DataFrame(groupedPath_Brit) 
m6=m5  
m6=path_Brit     
m7=m6.groupby(['VoyageFrom'])
for na1,grp in m7:
    print(na1)
    #print(na2)
    #print(na3)
    print(grp)



       

