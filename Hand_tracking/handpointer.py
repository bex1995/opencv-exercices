# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 13:52:42 2021

@author: alexa
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 10:02:54 2021

@author: alexa
"""

import cv2 as cv
import handtrackingmodule as htm
import math
import numpy as np
import pyautogui
wCam, hCam = 1280,720
cap = cv.VideoCapture(0,cv.CAP_DSHOW)
cap.set(3,wCam)
cap.set(4,hCam)
detector=htm.handDetector()
while True:
    success, img = cap.read()
    img = detector.findHands(img,draw=False)
    lmList = detector.findPositions(img)
    if len(lmList)!=0: #insure that list is not empty
        x1,y1= lmList[4][1],lmList[4][2]
        x2,y2= lmList[8][1],lmList[8][2]
        x3,y3= lmList[12][1],lmList[12][2]
        cx,cy = (x1+x3)//2,(y1+y3)//2
        cv.circle(img, (x1,y1),10,(255,0,255),cv.FILLED)
        cv.circle(img, (x2,y2),10,(255,0,255),cv.FILLED)
        cv.circle(img, (x3,y3),10,(255,0,255),cv.FILLED)
        cv.line(img, (x1,y1), (x3,y3), (255,255,255))
        dist=math.sqrt((x3 - x1)**2 + (y3 - y1)**2)
        posx=np.interp(x2,[0,1280],[1920,0])
        posy=np.interp(y2,[0,720],[0,1080])
        pyautogui.moveTo(x2, y2)
        if dist< 70:
            cv.circle(img, (cx,cy),10,(0,255,0),cv.FILLED)
            pyautogui.click(x2, y2)
        # posx1=np.interp(x1,[0,720],[0,1080])
        # posx1=np.interp(x1,[0,720],[0,1080])
        print (posx,posy)
        #print(dist)
        
        #Hand Range 20 - 200
        #volume range : -95, 0

        
    detector.displayFps(img)
    
    imgRGB=cv.cvtColor(img, cv.COLOR_BGR2RGB)
    cv.imshow('capture',img)

    if cv.waitKey(2) & 0xFF==ord('d'):
        break

#cap.release()
cv.destroyAllWindows()