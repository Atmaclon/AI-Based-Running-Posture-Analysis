from multiprocessing import Process,Queue,Pipe
from turtle import width
import types
import cv2
from cv2 import VideoCapture
import mediapipe as mp
import time
import math
import numpy as np
import os
import ffmpeg
from baseangle import findlean  
from baselanding import findlanding  
from basehip import findhipdrop

NoneType = type(None)

def check_rotation(path_video_file):
    # this returns meta-data of the video file in form of a dictionary
    meta_dict = ffmpeg.probe(path_video_file)

    # from the dictionary, meta_dict['streams'][0]['tags']['rotate'] is the key
    # we are looking for
    rotateCode = None
    try:
        if int(meta_dict['streams'][0]['tags']['rotate']) == 90:
            rotateCode = cv2.ROTATE_90_CLOCKWISE
        elif int(meta_dict['streams'][0]['tags']['rotate']) == 180:
            rotateCode = cv2.ROTATE_180
        elif int(meta_dict['streams'][0]['tags']['rotate']) == 270:
            rotateCode = cv2.ROTATE_90_COUNTERCLOCKWISE
    except KeyError:
        pass
    return rotateCode

def correct_rotation(frame, rotateCode):  
     return cv2.rotate(frame, rotateCode) 

#from original code
def pointIsOnLine(m, c, x, y):
     
    # If (x, y) satisfies the
    # equation of the line
    if (y == ((m * x) + c)):
        return True
 
    return False

def Ang_bw_TwoPoints(x1, y1, x2, y2):
    angle = math.atan2(x2-x1, y2-y1)
    print("angle1: ", angle)
    angle = angle * 180 / 3.14
    print("angle2: ", angle)
    return angle
    
def calculateDistance(x1,y1,x2,y2):  
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
     return dist 


#variables
ox=0
oy=0
count=0
count_hip=0
ang=0
flag=0
flagg=0
slope=None
facing_dir_prev=0
c=5 #for counting the number of frames the resulting text should appear
prev_ground_assumption=0 #checking previous
flag=0 #for checking foot not moving (ground)

print(cv2.__version__)

#cv2 taking input
video_path=0
cap = cv2.VideoCapture(video_path)

if not cap:
    print("Video not loaded")
    exit()
#rotateCode = check_rotation(video_path)
pTime =0

#init mediapipe 
mpDraw=mp.solutions.drawing_utils
mpPose =mp.solutions.pose
pose=mpPose.Pose()

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
size = (frame_width, frame_height)
print(f"frame width{frame_width}")
facing_left=0
if frame_width>400:
    font_size=.8
else:
    font_size=.5
result=cv2.VideoWriter('filename.avi', cv2.VideoWriter_fourcc(*'MJPG'),10, size)

partdict={} #empty dictionary for parts
while(True):
    ret,img = cap.read()
    
    if not ret:
        break
    
#    if rotateCode is not None:
#        frame = correct_rotation(frame, rotateCode)
    
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=pose.process(imgRGB)

    #print(results.pose_landmarks)

    if (results.pose_landmarks):
        mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS)
    
    
    try:
        #LEFT------------------------------------

        partdict["left_ear_x"]=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_EAR].x)*frame_width)
        partdict["left_ear_y"]=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_EAR].y)*frame_height)
        
        #LEFT INDEX
        partdict["left_toe_x"]=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_FOOT_INDEX].x)*frame_width)
        partdict["left_toe_y"]=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_FOOT_INDEX].y)*frame_height)
    
        #LEFT HEEL
        partdict["left_heel_x"]=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HEEL].x)*frame_width)
        partdict["left_heel_y"]=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HEEL].y)*frame_height)
    
        #LEFT HIP
        partdict["left_hip_x"]=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].x)*frame_width)
        partdict["left_hip_y"]=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].y)*frame_height)
        partdict["left_hip_z"]=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].z)*frame_width)
        
        #KNEE
        partdict["left_knee_x"]=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].x)*frame_width)
        partdict["left_knee_y"]=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].y)*frame_height)
    
        #RIGHT------------------------------------

        partdict["right_ear_x"]=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_EAR].x)*frame_width)
        partdict["right_ear_y"]=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_EAR].y)*frame_height)
        
        #RIGHT INDEX
        partdict["right_toe_x"]=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_FOOT_INDEX].x)*frame_width)
        partdict["right_toe_y"]=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_FOOT_INDEX].y)*frame_height)
        #RIGHT HEEL
        partdict["right_heel_x"]=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HEEL].x)*frame_width)
        partdict["right_heel_y"]=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HEEL].y)*frame_height)
    
        #RIGHT HIP
        partdict["right_hip_x"]=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].x)*frame_width)
        partdict["right_hip_y"]=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].y)*frame_height)
        partdict["right_hip_z"]=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].z)*frame_width)
        
        #KNEE
        partdict["right_knee_x"]=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].x)*frame_width)
        partdict["right_knee_y"]=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].y)*frame_height)
        #ANCLE
    except:
        continue
    
    #img= call landing with arguments
    #img,ox,oy,slope,count,ang,prev_ground_assumption,flag,c=findlanding(img,ox,oy,slope,count,ang,prev_ground_assumption,flag,c,facing_left,frame_width,font_size,partdict)
    #img= call lean with arguments
    #img,facing_dir_prev=findlean(img,facing_left,font_size,partdict,facing_dir_prev)
    #img=call hip with arguments
    #img,count_hip,flagg=findhipdrop(img,flagg,count_hip,font_size,partdict)
    
    #img=call landing with arguments
    cv2.imshow("Image",img)
    cv2.imwrite(os.path.join('folder',"{:d}.jpg".format(count)), img)
    a=0
    #input(a)
    result.write(img)
    
    ch=cv2.waitKey(1)
    if ch & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()