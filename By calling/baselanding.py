from turtle import width
#from types import NoneType
import cv2
from cv2 import VideoCapture
import mediapipe as mp
import time
import math
import numpy as np
import os
import ffmpeg

NoneType = type(None)

def slopee(x1,y1,x2,y2):
    try:
        return ((y2 - y1) / (x2 - x1))
    except:
        return

def angle3(a,b,c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang


def findlanding(img,ox,oy,slope,count,ang,prev_ground_assumption,flag,c,facing_left,frame_width,font_size,partdict):
    ground_assump=max(partdict["left_toe_y"],partdict["right_toe_y"],partdict["right_heel_y"],partdict["left_heel_y"])
     
    #print(f"right toe height:{partdict["right_toe_y"]} left toe height:{partdict["left_toe_y"]}")                 #greater than statement added as test 
    
    if(int(ground_assump/10)==int(prev_ground_assumption/10) and not prev_ground_assumption>ground_assump):  #checks if bottomost leg stays at the same place for 3 frames
        if(count==3): #3 frames found to be ideal               ^#upto the 10s digit as units place my vary no matter what
            flag=1                                              
            count=0
        else:
            print("ground")
            count+=1
            
    elif not flag==1:
        prev_ground_assumption=ground_assump
        if (ground_assump==partdict["left_heel_y"] or ground_assump==partdict["left_toe_y"]) and ((not facing_left and partdict["left_toe_x"]==max(partdict["left_toe_x"],partdict["right_toe_x"])) or (facing_left and partdict["left_toe_x"]==min(partdict["left_toe_x"],partdict["right_toe_x"]))): #to check left is on the ground or right

            print("ox is the left toe")
            ox=partdict["left_toe_x"]
            oy=partdict["left_toe_y"]
            
            slope=slopee(partdict["left_heel_x"],partdict["left_heel_y"],partdict["left_toe_x"],partdict["left_toe_y"])
            ang=angle3((partdict["left_knee_x"],partdict["left_knee_y"]),(partdict["left_heel_x"],partdict["left_heel_y"]),(partdict["left_toe_x"],partdict["left_toe_y"]))
        elif (ground_assump==partdict["right_heel_y"] or ground_assump==partdict["right_toe_y"]):
            print("ox is the right toe")
            ox=partdict["right_toe_x"] # as we dont know if the left side or the right side touches the ground while displaying slope instead we send the values as ox and oy as 
            oy=partdict["right_toe_y"]
            slope=slopee(partdict["right_heel_x"],partdict["right_heel_y"],partdict["right_toe_x"],partdict["right_toe_y"])
            ang=angle3((partdict["right_knee_x"],partdict["right_knee_y"]),(partdict["right_heel_x"],partdict["right_heel_y"]),(partdict["right_toe_x"],partdict["right_toe_y"]))
        else:
            pass
        
        if((partdict["right_heel_x"]>partdict["right_toe_x"])) and min(partdict["left_toe_y"],partdict["right_toe_y"],partdict["right_heel_y"],partdict["left_heel_y"])!=partdict["right_heel_y"]: #check left or right and ruling out heel in air condition
            print(f"angbefore{slope}")
            if(ang>250):  #impossible movement
                ang=360-ang
            try:
                slope*=-1
            except:
                slope=15 #to show Unknown
            print(f"slafter{slope}")
            print("left")
            facing_left=1
        elif partdict["left_heel_x"]<partdict["left_toe_x"] : #checking the other leg to rule out the heel in air condition
            facing_left=0
        else:
            print(f"sangbefore{slope}")
            if(ang>250):  #impossible movement
                ang=360-ang
            try:
                slope*=-1
            except:
                slope=15 #to show Unknown
            print(f"slafter{slope}")
            print("left")
    a=0
    #input(a)  #halt
    print(f"angle {ang}")
    #print(f"slope {slope}")
    #print(f"rheel {partdict["right_heel_x"]}")
    #print(f"toe {partdict["right_toe_x"]}")
    print(ground_assump)
    if ground_assump:
        cv2.line(img,(0,int(ground_assump)),(int(frame_width),int(ground_assump)),(255,0,0),3)
    if flag==1 or c<4 and c>=0:
        if slope is NoneType:
            a=1 #garbage for not crashing
            landingtxt=''
        elif((not facing_left and 0<slope) or ang>100):          
            landingtxt='FrontFoot land '    #check landing type with slope
        elif(0>slope and ang<90):
            landingtxt='Heel land'               
        elif(-1.25<slope<1.25):
            landingtxt='MidFoot land'
        else:
            landingtxt='Unknown'
        print(f"angle in if{ang}")
        print(f"slope in if{slope}")
        print(f"facing left={facing_left}")
        #print(f"hips{partdict["left_hip_x"],partdict["right_hip_x"]}")
        print(f"ox ={ox}")
        print(f"going for a {landingtxt}")
        if ((ox<(min(partdict["left_hip_x"],partdict["right_hip_x"]))) and facing_left): #not displaying when the leg is behind the hip 
            cv2.putText(img,landingtxt,(ox,oy),cv2.FONT_HERSHEY_COMPLEX,font_size,(255,255,255),2, lineType=cv2.LINE_AA)
        elif (not facing_left and ox>(max(partdict["left_hip_x"],partdict["right_hip_x"]))):
            cv2.putText(img,landingtxt,(ox,oy),cv2.FONT_HERSHEY_COMPLEX,font_size,(255,255,255),2, lineType=cv2.LINE_AA)
        else :
            cv2.putText(img,landingtxt+'?',(ox,oy),cv2.FONT_HERSHEY_COMPLEX,font_size,(255,0,0),2, lineType=cv2.LINE_AA)
        c-=1
        if(c==0):
            c=5
            flag=0
    return img,ox,oy,slope,count,ang,prev_ground_assumption,flag,c