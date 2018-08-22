# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 17:35:28 2018

@author: F-888USER
"""
import numpy as np
import numpy.random as random
import scipy as sp
import pandas as pd
from pandas import Series, DataFrame
from PIL import Image
import matplotlib.pyplot as plt
import subprocess

def jtalk(words,e_voice): #possible e_voice are 'happy','quiet','sad','surprise','angry','fear','disgust'
    open_jtalk=['open_jtalk']
    mech=['-x','./dic/naist-jdic']

    if (e_voice == 'happy') or (e_voice == 'quiet') or (e_voice =='sad')or (e_voice == 'angry'):  #there is no proper .htsvoice file to express the status of "disgust" "fear" "surprise"
        htsvoice=['-m','./voice/mei/'+e_voice+'.htsvoice']
        speed=['-r','1.0']
    elif e_voice =='surprise':                         # adjust the speed or intonation to approch the emotional voice
        htsvoice=['-m','./voice/mei/quiet.htsvoice']
        speed=['-r','1.0']
    elif e_voice =='fear':
        htsvoice=['-m','./voice/mei/quiet.htsvoice']
        speed=['-r','1.0']
    elif e_voice =='disgust':
        htsvoice=['-m','./voice/mei/quiet.htsvoice']
        speed=['-r','1.0']
    else:
        htsvoice=['-m','./voice/mei/quiet.htsvoice']
        speed=['-r','1.0']
    

    outwav=['-ow','open_jtalk.wav']
    cmd=open_jtalk+mech+htsvoice+speed+outwav
    c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    c.stdin.write(words.encode('utf-8'))
    c.stdin.close()
    c.wait()
    aplay = ['aplay','-q','open_jtalk.wav']
    wr = subprocess.Popen(aplay)


def routeCheck(route_raw):
    a=[]
    if route_raw==None:
        return np.array([])
    route=int(route_raw)
    while route>10:
        a.append(route%10)
        route=route//10
    a.append(route%10)
    route=route//10
    route_array=np.array(a)
    return route_array
    
## transition initiation

transition_route = {'mood_index':['happy','quiet','sad','surprise','angry','fear','disgust']   # possible transition and route of transition
        ,'happy':['12','12','2','12','2','2','2']
        ,'quiet':['35','0','0','0','13','13','13']
        ,'sad':['4','345','345','345','4','4','4']
        ,'surprise':['9','9','9','9','9','9','9']
        ,'angry':['7','7','7','7','57','7','7']
        ,'fear':['8','8','8','8','8','58','8']
        ,'disgust':['6','6','6','6','6','6','56']}

transition_route_frame=DataFrame(transition_route)
transition_route_frame=transition_route_frame[['mood_index','happy','quiet','sad','surprise','angry','fear','disgust']]
#print(transition_route_frame)

transition_cost = {'mood_index':['happy','quiet','sad','surprise','angry','fear','disgust']
        ,'happy':[0.42,0.21,0.08,0.19,0.06,0.05,0.05]
        ,'quiet':[0.36,1,1,1,0.3,0.2,0.3]
        ,'sad':[0.06,0.09,0.32,0.09,0.12,0.13,0.09]
        ,'surprise':[0.06,0.05,0.06,0.24,0.08,0.10,0.06]
        ,'angry':[0.03,0.04,0.10,0.09,0.29,0.10,0.16]
        ,'fear':[0.03,0.05,0.06,0.08,0.07,0.28,0.08]
        ,'disgust':[0.03,0.04,0.07,0.05,0.12,0.09,0.31]}
transition_cost_frame=DataFrame(transition_cost)
transition_cost_frame=transition_cost_frame[['mood_index','happy','quiet','sad','surprise','angry','fear','disgust']]
#print(transition_cost_frame)

'''
 input as actuator=[0.3,0.4,0.5,0.2,0,0,0,0.8,0.5]  # a input that can influent the mental status. It could be a word, a TV scene, a picture .etc
 current status as status='quiet'
'''
status=['happy','quiet','sad','surprise','angry','fear','disgust']

status_current='quiet'
status_image=Image.open("./emoji/"+status_current+".jpeg")
status_image.thumbnail((128,128))
status_image.show()
text="こんにちは、あなたは誰ですか"
jtalk(text,status_current)

status_next=''

while True:
    print("Please input 9 parameters as the emotional actuator in the order of ")
    str_input=input(" 1  2  3  4  5  6  7  8  9  with space between them:\n")
    e_input=[float(n) for n in str_input.split()]
    #print(e_input)
    actuator=np.array(e_input)
    check=[]
   
    route_code=transition_route_frame[transition_route_frame.mood_index==status_current].index.tolist()
    cost_code=transition_cost_frame[transition_cost_frame.mood_index==status_current].index.tolist()
    for j in range(len(status)):
        route_raw=transition_route_frame.iloc[route_code[0],j+1]
        cost=transition_cost_frame.iloc[route_code[0],j+1]
        #print(cost)
        act_detect=routeCheck(route_raw)          #divide the raw route data into several single route number
        for k in range(len(act_detect)):
            temp=[]
            emok=actuator[act_detect[k]-1]/(cost)
            temp.append(status[j])
            temp.append(cost)
            temp.append(emok)
            #print(temp)
            check.append(temp)
    #print(check)
    aaa=DataFrame(check)
    aaa.columns = ['status_next', 'cost', 'result']
    print(aaa)
    bbb=aaa.sort_values(by=['result'],ascending=False) # sort by the value of result descendly



    ##status_next
    if bbb.iloc[0,2]<1.0:
        status_next=status_current
    else:
        status_next=bbb.iloc[0,0]  #the status with most posibility . the first element in the first line
    print(status_next)
    status_current=status_next
    status_image=Image.open("./emoji/"+status_current+".jpeg")
    status_image.thumbnail((128,128))
    status_image.show()
    jtalk(text,status_current)


