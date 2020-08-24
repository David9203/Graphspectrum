

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 15:22:16 2020

@author: davidrendon
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
os.chdir('/home/davidrendon/Documents/Spectrogramskmeans/19agosto')    ##Put here the directory with to save 
da= pd.read_csv("datakmeanszones.csv") #Read the csv with the names of the recordings in the directory
os.chdir('/media/davidrendon/Seagate Expansion Drive/Bioacustica/Caribe') #Put directory with the files 
allrecord={}   #saves the dictionary
errorrecordigns=[] # saves the recordings with error
canal=1             #Channel in the case of stereo recordings
tipo_ventana = "hann"  
sobreposicion = 0
tamano_ventana = int(512)
fmin = int(0)
fmax = int(1)

count=0
#os.remove("dataspectrum.txt")

for j,i in enumerate(da.nameubi):
#        start = time.time()
     print('recordingno',j)
     try:
        x1, Fs1 = sf.read(i[1:])
        f, t, s = signal.spectrogram(x1, Fs1, window=tipo_ventana, 
                                         mode="magnitude", 
                                         )    
        meanspect=s.mean(axis=1)
        
        
        thisdict = {
                  "name": i,
                  "hour":i[-10:-4],
                  "Kmeans":str(da.kmeans[j]),
                  #"frequency": f.tolist(),
                  #"time": t.tolist(),
                  #"spectrum":s.flatten().tolist(),
                  "meanspectrum":meanspect.tolist() 
                }
        allrecord[j]=thisdict
        count=count+1
        if count==500:
            
            try:
                start = time.time()
                with open('dataspectrum0.txt') as json_file:
                    b = json.load(json_file)
                    b.update(allrecord)
                with open('dataspectrum0.txt', 'w') as outfile:
                    json.dump(b, outfile)
                
                end = time.time()
                print(end - start)
            except:
                with open('dataspectrum0.txt', 'w') as outfile:
                    json.dump(allrecord, outfile)
            allrecord={}     
            b={}
            count=0    
            
            
     except:
        print('erroren grabacion:  ',i)
        errorrecordigns.append(i)
#        end = time.time()
#       print(end - start)

with open('dataspectrum0.txt') as json_file:
                b = json.load(json_file)
                b.update(allrecord)
                

with open('dataspectrum0.txt', 'w') as outfile:                
                json.dump(b, outfile)

newallrecord=[]
for i in allrecord:
    print(i)
    thisdict = {
                  "name": allrecord[i]['name'],
                  "hour": allrecord[i]['hour'],
                  "Kmeans": str(allrecord[i]['Kmeans']),
                  #"frequency": f.tolist(),
                  #"time": t.tolist(),
                  #"spectrum":s.flatten().tolist(),
                  "meanspectrum": allrecord[i]['meanspectrum'] 
                }
    newallrecord.append(thisdict)
    
with open('dataspectrum0.txt', 'w') as outfile:                
                json.dump(newallrecord, outfile)
    