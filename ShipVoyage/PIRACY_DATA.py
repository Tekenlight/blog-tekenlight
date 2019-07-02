
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from geopy.geocoders import Nominatim 

#And then import the database
df = pd.read_csv('CLIWOC15.csv', low_memory=False)
#we remove Nan entries for the columns we are interested in studying

df5=df.dropna(subset = ['Lon3', 'Lat3', 'UTC', 'VoyageIni','VoyageFrom', 'VoyageTo', 'WarsAndFights'])
#m5=df5[df5['Nationality']=='British']
#m7=df5[df5['Nationality']=='Spanish']
#m9=df5[df5['Nationality']=='Dutch']
#m11=df5[df5['Nationality']=='French']
ps=pd.DataFrame(X)
War_Data=df5[['Nationality','Lon3', 'Lat3', 'UTC', 'VoyageIni','VoyageFrom', 'VoyageTo', 'WarsAndFights']]

X=War_Data.iloc[:,:-1].values
y=War_Data.iloc[:,7].values

from sklearn.preprocessing import LabelEncoder
lec=LabelEncoder()
X[:,0]=lec.fit_transform(X[:,0])   
X[:,5]=lec.fit_transform(X[:,5])   
X[:,6]=lec.fit_transform(X[:,6])

from sklearn.preprocessing import StandardScaler
sc_x=StandardScaler()
X=sc_x.fit_transform(X)
ps=pd.DataFrame(y)

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.15,random_state=0)


import keras
from keras.models import Sequential
from keras.layers import Dense

Classifier=Sequential()

Classifier.add(Dense(output_dim=4,init='uniform',activation='relu',input_dim=7))
Classifier.add(Dense(output_dim=4,init='uniform',activation='relu'))
Classifier.add(Dense(output_dim=1,init='uniform',activation='sigmoid'))

Classifier.compile(optimizer='adam',loss='binary_crossentropy', metrics=['accuracy'])
Classifier.fit(X_train,y_train,batch_size=20,nb_epoch=10)

y_pred=Classifier.predict(X_test)
y_pred1=[]
from sklearn.metrics import confusion_matrix
for m in y_pred:
    if m<0.5:
        m=0
    else:
        m=1
    y_pred1.append(m)    
cm=confusion_matrix(y_test,y_pred1)


pred_y1=np.array(y_pred1)










   

       

