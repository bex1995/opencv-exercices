# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 08:43:54 2021

@author: alexa
"""

import cv2 as cv
import mediapipe as mp
import time


cap = cv.VideoCapture(0)

mpHands=mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime=0 #previoustime
cTime=0 #current time

while True:
    success, img = cap.read()
    imgRGB=cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            #retrieve landmark info
            for id, lm in enumerate (handLms.landmark):
                #print(id,lm)
                h, w, c=img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id,cx,cy)
                #if id==8:
                #    cv.circle(img, (cx,cy), 25, (255,0,255),cv.FILLED)
            #draw landmarks
            mpDraw.draw_landmarks(img, handLms,mpHands.HAND_CONNECTIONS)
            
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime=cTime    
    cv.putText(img, str(int(fps)), (10,70), cv.FONT_HERSHEY_PLAIN, 2, (255,0,255),2)
    cv.imshow('capture',img)
    
    if cv.waitKey(2) & 0xFF==ord('d'):
        break

cap.release()
cv.destroyAllWindows()