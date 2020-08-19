#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 08:54:19 2020

@author: nesdav
"""






import os
import soundfile as sf
import pandas as pd
import math
import numpy as np
from scipy import signal, stats
from scipy.fft import fftshift
import matplotlib.pyplot as plt
import statistics 
import time
import pickle
from tqdm import tqdm
import json


##---Carga de datos procesados para juntarlos en un nuevo diccionario llamado totaldict

with open('dataspectrum0.txt') as json_file:
                b0 = json.load(json_file)
                

with open('dataspectrum.txt') as json_file:
                b = json.load(json_file)
                
with open('dataspectrum1.txt') as json_file:
                b1 = json.load(json_file)               
                
                b0.update(b)
                
                
                
ini_dict=b0.copy()
                
for i in range(len(b)):

    ini_dict[str(i+2000)] = b[str(i)] 
    
for i in range(len(b1)):

    ini_dict[str(i+10000)] = b1[str(i)] 
    
    
with open('dataspectrumcomplete.txt', 'w') as outfile:                
                json.dump(ini_dict, outfile)
                
with open('dataspectrumcomplete.txt') as json_file:
                totaldict = json.load(json_file)
             
                
 ###----- Ahora se debe de hacer un promedio por cada hora de meanspect


listhour=[]
dictionarymeanspectall={}
for i in totaldict:
    
    listhour.append(totaldict[str(i)]['hour'])

listhour=np.array(listhour)
uniquehours=np.unique(listhour)





arraymeanspect = np.zeros(shape=(238,129))

for ind, i in enumerate(uniquehours):
    
    hlist=[]
    for j in totaldict:      #Recorre todos los espectros de grabaciones
        if str(i)==totaldict[str(j)]['hour']:
            hlist.append(np.power(10, np.array(totaldict[str(j)]['meanspectrum'])/10))
    
    dictmeanspect = {
                   str(i): 10*np.log(np.mean(hlist, axis=0)),
                }
    dictionarymeanspectall.update(dictmeanspect)
    
    from sklearn.preprocessing import MinMaxScaler
    
    withoutstandari=10*np.log(np.mean(hlist, axis=0))
    scaler = MinMaxScaler()
    ss=scaler.fit_transform(withoutstandari.reshape(-1, 1))
    #scaler.transform(withoutstandari)
    arraymeanspect[ind]= ss.reshape(129)

    
#---Graficar dictionary mean spect


f=np.linspace(0, 24, num=129)
h=np.linspace(0, 23.5, num=238)
    
plt.pcolormesh(h, f, arraymeanspect.T, cmap="inferno")
#plt.pcolor(t, f, s)
plt.ylabel('Frequency [kHz]')
plt.xlabel('Hour')
plt.xticks(np.arange(min(h), max(h), 1.0))
plt.yticks(np.arange(min(f), max(f), 1.0))
plt.savefig('meanspectday.png', dpi=300)

plt.show()    


##--- Ahora con la media 

listhour=[]
dictionarymeanspectall={}
for i in totaldict:
    
    listhour.append(totaldict[str(i)]['hour'])

listhour=np.array(listhour)
uniquehours=np.unique(listhour)

arraymeanspect = np.zeros(shape=(238,129))
for ind, i in enumerate(uniquehours):
    
    hlist=[]
    for j in totaldict:
        if str(i)==totaldict[str(j)]['hour']:
            hlist.append(np.power(10, np.array(totaldict[str(j)]['meanspectrum'])/10))
    
    dictmeanspect = {
                   str(i): 10*np.log(np.median(hlist, axis=0)),
                }
    dictionarymeanspectall.update(dictmeanspect)
    arraymeanspect[ind]= 10*np.log(np.median(hlist, axis=0))
    
    
f=np.linspace(0, 24, num=129)
h=np.linspace(0, 23.5, num=238)
    
plt.pcolormesh(h, f, arraymeanspect.T, cmap="plasma")
#plt.pcolor(t, f, s)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Hour')
plt.xticks(np.arange(min(h), max(h), 1.0))
#plt.savefig('medianspect.png', dpi=300)

plt.show()    


#----Usar etiquetas Kmeans
datakmeans=pd.read_csv('datakmeanszones (1).csv')

listhour=[]
meanspect=[]
name=[]
for i in totaldict:
    meanspect.append(totaldict[str(i)]['meanspectrum'])
    listhour.append(totaldict[str(i)]['hour'])
    name.append(totaldict[str(i)]['name'])

listhour0=np.array(listhour)
meanspect=np.array(meanspect)
name=np.array(name)



listofmachesmean1=[]
listofhours1=[]
for i,j in  enumerate(datakmeans[datakmeans.kmeans==2].nameubi):
    for k in name:
        if k==j:
            listofmachesmean1.append(meanspect[i])
            listofhours1.append(listhour0[i])
            
listofmachesmean1=np.array(listofmachesmean1)
    

listhour=np.array(listofhours1)
uniquehours=np.unique(listofhours1)




arraymeanspect = np.zeros(shape=(238,129))

dictionarymeanspectall={}
for ind, i in enumerate(uniquehours):
    
    hlist=[]
    for jnd,j in enumerate(listhour):      #Recorre todos los espectros de grabaciones
        if str(i)==j:
            hlist.append(np.power(10, np.array(listofmachesmean1[jnd])/10))
    
    dictmeanspect = {
                   str(i): 10*np.log(np.mean(hlist, axis=0)),
                }
    dictionarymeanspectall.update(dictmeanspect)
    
    from sklearn.preprocessing import MinMaxScaler
    
    withoutstandari=10*np.log(np.mean(hlist, axis=0))
    scaler = MinMaxScaler()
    ss=scaler.fit_transform(withoutstandari.reshape(-1, 1))
    #scaler.transform(withoutstandari)
    arraymeanspect[ind]= ss.reshape(129)
    
f=np.linspace(0, 24, num=129)
h=np.linspace(0, 23.5, num=238)
    
plt.pcolormesh(h, f, arraymeanspect.T, cmap="inferno")
#plt.pcolor(t, f, s)
plt.ylabel('Frequency [kHz]')
plt.xlabel('Hour')
plt.xticks(np.arange(min(h), max(h), 1.0))
plt.yticks(np.arange(min(f), max(f), 1.0))
plt.savefig('meanspectday.png', dpi=300)

plt.show()    


##---graficar kmeans ---

with open('dataspectrumallre.txt') as json_file:
                totaldict = json.load(json_file)  
listhour=[]
dictionarymeanspectall={}
for i in totaldict:
    
    listhour.append(i['hour'])

listhour=np.array(listhour)
uniquehours=np.unique(listhour)





from sklearn.preprocessing import MinMaxScaler
for z in range(0,6):    
    arraymeanspect = np.zeros(shape=(238,129))
    for ind, i in enumerate(uniquehours):
        
        hlist=[]
        for jnd,j in enumerate(totaldict):      #Recorre todos los espectros de grabaciones
            #print(jnd)
            if i==j['hour'] and j['Kmeans']==str(z) :
                print('aaaa')
                hlist.append(np.power(10, j['meanspectrum'])/10)
        
        dictmeanspect = {
                       str(i): 10*np.log(np.mean(hlist, axis=0))}
        dictionarymeanspectall.update(dictmeanspect)
        
        
        
        withoutstandari=10*np.log(np.mean(hlist, axis=0))
        scaler = MinMaxScaler()
        ss=scaler.fit_transform(withoutstandari.reshape(-1, 1))
        #scaler.transform(withoutstandari)
        arraymeanspect[ind]= ss.reshape(129)
    
    f=np.linspace(0, 24, num=129)
    h=np.linspace(0, 23.5, num=238)
    
    plt.pcolormesh(h, f, arraymeanspect.T, cmap="inferno")
    #plt.pcolor(t, f, s)
    plt.ylabel('Frequency [kHz]')
    plt.xlabel('Hour')
    plt.xticks(np.arange(min(h), max(h), 1.0))
    plt.yticks(np.arange(min(f), max(f), 1.0))
    plt.savefig('meanspectday.png', dpi=300)
    
    plt.show()    
#---Graficar dictionary mean spect



