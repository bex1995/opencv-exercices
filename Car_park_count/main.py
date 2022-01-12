# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 18:28:23 2022

@author: alexa
"""

import cv2
import cvzone
import pickle
import numpy as np


with open('carparkpos','rb') as f:
        posList=pickle.load(f)
width,height = 107,48
cap = cv2.VideoCapture('carPark.mp4')

def checkParkingSpace(imgPro):
    spacecount=0
    for position in posList:
      x,y = position
     # cv2.rectangle(img,(position[0],position[1]),(position[0]+width,position[1]+height),(255,0,0),2) 
      imgCrop = imgPro[y:y+height,x:x+width]
      count = cv2.countNonZero(imgCrop)
      cvzone.putTextRect(img, str(count), (x,y+height-5),scale=1,thickness = 1,offset=0)
     #  cv2.imshow(str(x*y),imgCrop)
      if count <900:
         color = (0,255,0)
         spacecount = spacecount +1
      else:
         color = (0,0,255)
      cv2.rectangle(img,(position[0],position[1]),(position[0]+width,position[1]+height),color,2)
    cvzone.putTextRect(img, f'Freespace: {spacecount}/{len(posList)}', (100,50),scale = 2)
while True:
    success,img = cap.read()
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3),1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,25,16) 
    imgMedian=cv2.medianBlur(imgThreshold, 5)
    dilateKernel = np.ones((3,3),np.uint8)
    imgDilate = cv2.dilate(imgMedian,dilateKernel,iterations=1)
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    checkParkingSpace(imgDilate)

   # cv2.imshow('carparkDilate',imgDilate)
    cv2.imshow('carpark',img)
      
    if cv2.waitKey(10) & 0xFF==ord('d'):
        break

cap.release()
cv2.destroyAllWindows()