#importing required libraries
import cv2
import mediapipe as mp
import time
import numpy
import math


#function to get the coordinates of the different points of a user's hand on a 21 point based recognition system
def getdata():
    lmlist = []
    for handLms in results1.multi_hand_landmarks:
        for id, lm in enumerate (handLms.landmark):
            h, w, c = frame.shape
            cx, cy = int (lm.x * w), int (lm.y * h)
            lmlist.append([id, cx, cy])
            mpDraw.draw_landmarks (frame, handLms, mpHands.HAND_CONNECTIONS)
    return lmlist



#switching to webcam
cap = cv2.VideoCapture (0)
cap.set(3,1920)
cap.set(4,1080)


#using mediapipe to get recognition of hands (here only 2 further can be increased if required through mpHands)
mpHands = mp.solutions.hands
hands = mpHands.Hands ()
mpDraw = mp.solutions.drawing_utils
mphol=mp.solutions.holistic

#declaring variables of previous and current time to calculate FPS
ptime = 0
ctime = 0


#accessing volume control of the device by using pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
range_vol=volume.GetVolumeRange()
min_vol=range_vol[0]
max_vol=range_vol[1]

#Main program and detection of user's face hands and body postures
while (True):
    ret, frame = cap.read ()
    imgRGB = cv2.cvtColor (frame, cv2.COLOR_BGR2RGB)
    results1= hands.process (imgRGB)
    # print(results.multi_hand_landmarks)
    if results1.multi_hand_landmarks:
        list=getdata()
        if len(list)!=0:
            x1,y1=list[4][1],list[4][2]
            x2,y2=list[8][1],list[8][2]
            cv2.circle(frame, ((x1+x2)//2,(y1+y2)//2),10,(0, 255,0),cv2.FILLED)
            cv2.line(frame,(x1,y1) ,(x2,y2), (0, 255, 0), 7)
            length=math.hypot(x2-x1,y2-y1)
            volume1=numpy.interp(length,[10,260],[min_vol,max_vol])
            volume.SetMasterVolumeLevel (volume1, None)

        #drawing Face and posture landmarks on screen
        #calculating FPS and displaying
    ctime = time.time ()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText (frame, str (int (fps)), (5, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow ('frame', frame)
    if cv2.waitKey (1) == ord ('q'):
        break
cap.release ()

