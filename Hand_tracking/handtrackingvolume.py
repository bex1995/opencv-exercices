# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 10:02:54 2021

@author: alexa
"""

import cv2 as cv
import handtrackingmodule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volumerange = volume.GetVolumeRange()
minVol=volumerange[0]
maxVol=volumerange[1]
#volume.SetMasterVolumeLevel(-5.0, None)
print(volumerange)
wCam, hCam = 1280,720
cap = cv.VideoCapture(0,cv.CAP_DSHOW)
cap.set(3,wCam)
cap.set(5,hCam)
detector=htm.handDetector()
while True:
    success, img = cap.read()
    img = detector.findHands(img,draw=False)
    lmList = detector.findPositions(img)
    if len(lmList)!=0: #insure that list is not empty
        x1,y1= lmList[4][1],lmList[4][2]
        x2,y2= lmList[8][1],lmList[8][2]
        cx,cy = (x1+x2)//2,(y1+y2)//2
        cv.circle(img, (x1,y1),10,(255,0,255),cv.FILLED)
        cv.circle(img, (x2,y2),10,(255,0,255),cv.FILLED)
        cv.line(img, (x1,y1), (x2,y2), (255,255,255))
        dist=math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        #print(dist)
        
        #Hand Range 20 - 200
        #volume range : -95, 0
        volumevalue = np.interp(dist,[20,200],[minVol,maxVol])
        print(volumevalue)
        volume.SetMasterVolumeLevel(volumevalue, None)
        
    detector.displayFps(img)
    
    imgRGB=cv.cvtColor(img, cv.COLOR_BGR2RGB)
    cv.imshow('capture',img)

    if cv.waitKey(2) & 0xFF==ord('d'):
        break

#cap.release()
cv.destroyAllWindows()