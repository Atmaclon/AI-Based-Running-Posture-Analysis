from turtle import width
from types import NoneType
import cv2
from cv2 import VideoCapture
import mediapipe as mp
import time
import math
import numpy as np
import os
import ffmpeg    

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
    
def angle3(a,b,c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang

def calculateDistance(x1,y1,x2,y2):  
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
     return dist 

def slopee(x1,y1,x2,y2):
    try:
        return ((y2 - y1) / (x2 - x1))
    except:
        return

#variables
ox=0
oy=0
count=0
ang=0
flag=0
flagg=0
c=5 #for counting the number of frames the resulting text should appear
prev_ground_assumption=0 #checking previous
flag=0 #for checking foot not moving (ground)

print(cv2.__version__)

#cv2 taking input
video_path="testrun.mp4"
cap = cv2.VideoCapture(1)

if not cap:
    print("Video not loaded")
    exit()
rotateCode = check_rotation(video_path)
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

        left_ear_x=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_EAR].x)*frame_width)
        left_ear_y=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_EAR].y)*frame_height)
        
        #LEFT INDEX
        left_toe_x=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_FOOT_INDEX].x)*frame_width)
        left_toe_y=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_FOOT_INDEX].y)*frame_height)
    
        #LEFT HEEL
        left_heel_x=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HEEL].x)*frame_width)
        left_heel_y=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HEEL].y)*frame_height)
    
        #LEFT HIP
        left_hip_x=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].x)*frame_width)
        left_hip_y=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].y)*frame_height)
        left_hip_z=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].z)*frame_width)
        
        #KNEE
        left_knee_x=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].x)*frame_width)
        left_knee_y=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].y)*frame_height)
    
        #RIGHT------------------------------------

        right_ear_x=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_EAR].x)*frame_width)
        right_ear_y=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_EAR].y)*frame_height)
        
        #RIGHT INDEX
        right_toe_x=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_FOOT_INDEX].x)*frame_width)
        right_toe_y=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_FOOT_INDEX].y)*frame_height)
        #RIGHT HEEL
        right_heel_x=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HEEL].x)*frame_width)
        right_heel_y=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HEEL].y)*frame_height)
    
        #RIGHT HIP
        right_hip_x=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].x)*frame_width)
        right_hip_y=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].y)*frame_height)
        right_hip_z=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].z)*frame_width)
        
        #KNEE
        right_knee_x=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].x)*frame_width)
        right_knee_y=int((results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].y)*frame_height)
        #ANCLE
    except:
        continue
    
    ground_assump=max(left_toe_y,right_toe_y,right_heel_y,left_heel_y)
     
    print(f"right toe height:{right_toe_y} left toe height:{left_toe_y}")                 #greater than statement added as test 
    
    if(int(ground_assump/10)==int(prev_ground_assumption/10) and not prev_ground_assumption>ground_assump):  #checks if bottomost leg stays at the same place for 3 frames
        if(count==3): #3 frames found to be ideal               ^#upto the 10s digit as units place my vary no matter what
            flag=1                                              
            count=0
        else:
            print("ground", count)
            count+=1
            
    elif not flag==1:
        prev_ground_assumption=ground_assump
        if (ground_assump==left_heel_y or ground_assump==left_toe_y) and ((not facing_left and left_toe_x==max(left_toe_x,right_toe_x)) or (facing_left and left_toe_x==min(left_toe_x,right_toe_x))): #to check left is on the ground or right
            
            #alternating foot check(no idea)
            #left=1
            #right=0
            print("ox is the left toe")
            ox=left_toe_x
            oy=left_toe_y
            
            slope=slopee(left_heel_x,left_heel_y,left_toe_x,left_toe_y)
            ang=angle3((left_knee_x,left_knee_y),(left_heel_x,left_heel_y),(left_toe_x,left_toe_y))
        elif (ground_assump==right_heel_y or ground_assump==right_toe_y):
            #alternating foot check
            #left=0
            #right=1
            print("ox is the right toe")
            ox=right_toe_x # as we dont know if the left side or the right side touches the ground while displaying slope instead we send the values as ox and oy as 
            oy=right_toe_y
            slope=slopee(right_heel_x,right_heel_y,right_toe_x,right_toe_y)
            ang=angle3((right_knee_x,right_knee_y),(right_heel_x,right_heel_y),(right_toe_x,right_toe_y))
        else:
            pass
        
        if((right_heel_x>right_toe_x)) and min(left_toe_y,right_toe_y,right_heel_y,left_heel_y)!=right_heel_y: #check left or right and ruling out heel in air condition
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
        elif left_heel_x<left_toe_x : #checking the other leg to rule out the heel in air condition
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
    cTime = time.time()
    fps=1/(cTime-pTime)
    cv2.putText(img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),3)
    print(f"angle {ang}")
    #print(f"slope {slope}")
    print(f"rheel {right_heel_x}")
    print(f"toe {right_toe_x}")
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
        print(f"hips{left_hip_x,right_hip_x}")
        print(f"ox ={ox}")
        print(f"going for a {landingtxt}")
        if ((ox<(min(left_hip_x,right_hip_x))) and facing_left): #not displaying when the leg is behind the hip 
            cv2.putText(img,landingtxt,(ox,oy),cv2.FONT_HERSHEY_COMPLEX,font_size,(255,255,255),2, lineType=cv2.LINE_AA)
        elif (not facing_left and ox>(max(left_hip_x,right_hip_x))):
            cv2.putText(img,landingtxt,(ox,oy),cv2.FONT_HERSHEY_COMPLEX,font_size,(255,255,255),2, lineType=cv2.LINE_AA)
        else :
            cv2.putText(img,landingtxt+'?',(ox,oy),cv2.FONT_HERSHEY_COMPLEX,font_size,(255,0,0),2, lineType=cv2.LINE_AA)
        c-=1
        if(c==0):
            c=5
            flag=0
    
    head_middle_x=((left_ear_x+right_ear_x)/2)
    head_middle_y=((left_ear_y+right_ear_y)/2)
    
    hip_middle_x=(left_hip_x+right_hip_x)/2
    hip_middle_y=(left_hip_y+right_hip_y)/2
    
    slopex=slopee(left_hip_x,left_hip_y,right_hip_x,right_hip_y)
    slopez=slopee(left_hip_z,left_hip_y,right_hip_z,right_hip_y)
    cv2.line(img,(int(hip_middle_x),0),(int(hip_middle_x),int(hip_middle_y)),(255,255,0),3)
    cv2.line(img,(int(head_middle_x),int(head_middle_y)),(int(hip_middle_x),int(hip_middle_y)),(255,0,0),3)
    print("lhip z", left_hip_z)
    print("rhip z", right_hip_z)
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
        cv2.line(img,(right_hip_x,right_hip_y),(left_hip_x,left_hip_y),(255,0,0),3)
        if flagg>0:
            if left_hip_y>right_hip_y:
                cv2.putText(img,"Left Hip drop",(left_hip_x,left_hip_y-40),cv2.FONT_HERSHEY_COMPLEX,font_size,(255,255,255),2, lineType=cv2.LINE_AA)
            else:
                cv2.putText(img,"Right Hip drop",(right_hip_x,right_hip_y-40),cv2.FONT_HERSHEY_COMPLEX,font_size,(255,255,255),2, lineType=cv2.LINE_AA)
            flagg-=1
    except:
        pass
    angle=angle3((left_knee_x,left_knee_y),(left_heel_x,left_heel_y),(left_toe_x,left_toe_y))
    angg=angle3((int(hip_middle_x),0),(int(hip_middle_x),int(hip_middle_y)),(int(head_middle_x),int(head_middle_y)))
    print("lhip z", left_hip_z)
    print("rhip z", right_hip_z)
    print("angle", angg)
    
    if((right_heel_x>right_toe_x)) and min(left_toe_y,right_toe_y,right_heel_y,left_heel_y)!=right_heel_y: #check left or right and ruling out heel in air condition
            if angle>250:  #impossible movement
                facing_left_slope=facing_dir_prev  #if ankle in air check the previous frame for reference
            else:
                facing_left_slope=1
            angg=360-angg   #
            print("left")
    elif left_heel_x<left_toe_x : #checking the other leg to rule out the heel in air condition
        facing_left_slope=0
        print("right")
    else:
        if(angle>250):  #impossible movement
            angg=360-angg
        print("left")
    facing_dir_prev=facing_left_slope
    try:
        if(angg>5 and angg<60):
            text="Forward Lean"
            color=(0,255,0)
        elif(angg>=0 and angg<=5):
            text="No lean"
            color=(255,255,255)
        elif(angg>250):
            text="Backward lean"
            color=(0,0,255)
        else:
            text="Improper lean"
            color=(0,0,255)
        cv2.putText(img,text,(int(hip_middle_x),int(hip_middle_y)),cv2.FONT_HERSHEY_COMPLEX,font_size,color,2, lineType=cv2.LINE_AA)
        cv2.putText(img,"Angle:"+str(round(angg,2)),(int(hip_middle_x),int(hip_middle_y)+25),cv2.FONT_HERSHEY_COMPLEX,font_size,color,2, lineType=cv2.LINE_AA)
    except:
        pass
    cv2.imshow("Image",img)
    cv2.imwrite(os.path.join('folder',"{:d}.jpg".format(count)), img)
    a=0
    #input(a)
    result.write(img)
    
    ch=cv2.waitKey(1)
    if ch & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()