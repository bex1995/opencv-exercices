# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 17:47:00 2022

@author: alexa
"""
import cv2
import pickle

try:
    with open('carparkpos','rb') as f:
        posList=pickle.load(f)
except:
    posList=[]

width,height = 107,48

def mouseClick(events,x,y,flags,params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN:
         for index,position in enumerate(posList):
             x1,y1 = position
             if x1<x<x1+width and y1<y<y1+height:
                 posList.pop(index)
      
    with open('carparkpos','wb') as f:
        pickle.dump(posList,f)
    


while True:
    img = cv2.imread("carParkImg.png")

    #cv2.rectangle(img,(100,100),(200,150),(255,0,255),2)
    for position in posList:
      cv2.rectangle(img,(position[0],position[1]),(position[0]+width,position[1]+height),(255,0,0),2)  
    cv2.imshow('carpark',img)
    cv2.setMouseCallback("carpark", mouseClick)
    cv2.waitKey(1)


cv2.destroyAllWindows()