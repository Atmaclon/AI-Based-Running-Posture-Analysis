from multiprocessing import Process,Queue,Pipe
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

def angle3(a,b,c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang

    
def findlean(img,facing_left,font_size,partdict,facing_dir_prev):
    head_middle_x=((partdict["left_ear_x"]+partdict["right_ear_x"])/2)
    head_middle_y=((partdict["left_ear_y"]+partdict["right_ear_y"])/2)
    
    hip_middle_x=(partdict["left_hip_x"]+ partdict["right_hip_x"])/2
    hip_middle_y=(partdict["left_hip_y"]+ partdict["right_hip_y"])/2

    should_middle_x=(partdict["left_should_x"]+ partdict["right_should_x"])/2
    should_middle_y=(partdict["left_should_y"]+ partdict["right_should_y"])/2
    
    cv2.line(img,(int(hip_middle_x),0),(int(hip_middle_x),int(hip_middle_y)),(255,255,0),3)
    cv2.line(img,(int(head_middle_x),int(head_middle_y)),(int(hip_middle_x),int(hip_middle_y)),(255,0,0),3)
    
    angle=angle3(( partdict["left_knee_x"], partdict["left_knee_y"]),( partdict["left_heel_x"], partdict["left_heel_y"]),( partdict["left_toe_x"], partdict["left_toe_y"]))  #lean angle
    ang=angle3((int(hip_middle_x),0),(int(hip_middle_x),int(hip_middle_y)),(int(head_middle_x),int(head_middle_y)))  #foot angle to check foot in air condition
    
    headAngle=angle3((int(hip_middle_x),0), (int(should_middle_x),int(should_middle_y)),(int(head_middle_x),int(head_middle_y)))
    shouldAngle=angle3((int(hip_middle_x),0),(int(hip_middle_x),int(hip_middle_y)), (int(should_middle_x),int(should_middle_y)))
    print("lhip z",  partdict["left_hip_z"])
    print("rhip z",  partdict["right_hip_z"])
    print("angle", ang)
    
    if(( partdict["right_heel_x"]> partdict["right_toe_x"])) and min( partdict["left_toe_y"], partdict["right_toe_y"], partdict["right_heel_y"], partdict["left_heel_y"])!= partdict["right_heel_y"]: #check left or right and ruling out heel in air condition
            if angle>250:  #impossible movement
                facing_left=facing_dir_prev #if ankle in air check the previous frame for reference
            else:
                facing_left=1
            ang=360-ang   #
            print("left")
    elif  partdict["left_heel_x"]< partdict["left_toe_x"] : #checking the other leg to rule out the heel in air condition
        facing_left=0
        print("right")
    else:
        if(angle>250):  #impossible movement
            ang=360-ang
        print("left")
    facing_dir_prev=facing_left
    try:
        if(ang>5 and ang<60):
            text="Forward Lean"
            if(shouldAngle>=12):
                text="Thoracic kyphosis"
            elif(headAngle>=15):
                text="Forward Head"

            color=(0,0,255)
        elif(ang>=0 and ang<=5):
            text="Good Posture"
            color=(255,255,255)
        elif(ang>250):
            text="Sway Back Posture"
            color=(0,0,255)
        else:
            text="Improper lean"
            color=(0,0,255)
        cv2.putText(img,text,(int(hip_middle_x),int(hip_middle_y)),cv2.FONT_HERSHEY_COMPLEX, font_size,color,2, lineType=cv2.LINE_AA)
        cv2.putText(img,"Angle:"+str(round(ang,2)),(int(hip_middle_x),int(hip_middle_y)+25),cv2.FONT_HERSHEY_COMPLEX, font_size,color,2, lineType=cv2.LINE_AA)
    except:
        pass
    return img,facing_dir_prev