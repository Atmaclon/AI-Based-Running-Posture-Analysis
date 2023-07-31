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


def findhipdrop(img,flagg,count_hip,font_size,partdict):
    slopex=slopee(partdict["left_hip_x"],partdict["left_hip_y"],partdict["right_hip_x"],partdict["right_hip_y"])
    slopez=slopee(partdict["left_hip_z"],partdict["left_hip_y"],partdict["right_hip_z"],partdict["right_hip_y"])
    print("lhip z", partdict["left_hip_z"])
    print("rhip z", partdict["right_hip_z"])
    print("slope for x", slopex)
    print("slope for z", slopez)
    
    try:
        if (slopex<0.245 and slopex>-0.245) and (slopez<0.012 and slopez>-0.012):
            print("No hip drop")
            count_hip=0
        elif ((slopex>0.245 or slopex<-0.245) and (slopez>0.012 or slopez<-0.012)) or (slopez<-0.023 or slopez>0.023):
            count_hip+=1
            if(count_hip>4):
                flagg=5
                count_hip=0
            print("hip dropped")
        else:
            count_hip=0
        print(f"count hip {count_hip}")
        cv2.line(img,(partdict["right_hip_x"],partdict["right_hip_y"]),(partdict["left_hip_x"],partdict["left_hip_y"]),(255,0,0),3)
        if flagg>0:
            if partdict["left_hip_y"]>partdict["right_hip_y"]:
                cv2.putText(img,"Left Hip drop",(partdict["left_hip_x"],partdict["left_hip_y"]-40),cv2.FONT_HERSHEY_COMPLEX,font_size,(255,255,255),2, lineType=cv2.LINE_AA)
            else:
                cv2.putText(img,"Right Hip drop",(partdict["right_hip_x"],partdict["right_hip_y"]-40),cv2.FONT_HERSHEY_COMPLEX,font_size,(255,255,255),2, lineType=cv2.LINE_AA)
            flagg-=1
    except:
        pass
    
    return img,count_hip,flagg