# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 09:21:11 2021

@author: alexa
"""


import cv2 as cv
import mediapipe as mp
import time




class handDetector():
    def __init__(self,mode = False,max_num_hands = 2,model_complexity=1, detection_confidence = 0.5, track_confidence =0.5):
        self.mode = mode
        self.max_num_hands = max_num_hands
        self.model_complexity=model_complexity
        self.detection_confidence=detection_confidence
        self.track_confidence=track_confidence
        self.mpHands=mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.max_num_hands,self.model_complexity,self.detection_confidence,self.track_confidence)
        self.mpDraw = mp.solutions.drawing_utils
        self.pTime=0
        self.cTime=0

    def findHands(self,img,draw=True):
        imgRGB=cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,self.mpHands.HAND_CONNECTIONS)
        return img
   
    def findPositions(self,img,handNo=0):
        lmList = []
             #retrieve landmark info
        if self.results.multi_hand_landmarks:
            myhand=self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate (myhand.landmark):
                   h, w, c=img.shape
                   cx, cy = int(lm.x*w), int(lm.y*h)
                   #print(id,cx,cy)
                   lmList.append([id,cx,cy])
        return lmList
    
    def displayFps(self,img):
        self.cTime = time.time()
        fps = 1/(self.cTime-self.pTime)
        self.pTime=self.cTime    
        cv.putText(img, str(int(fps)), (10,70), cv.FONT_HERSHEY_PLAIN, 2, (255,0,255),2)
        
def main():
    cap = cv.VideoCapture(0,cv.CAP_DSHOW)
    detector=handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPositions(img)
        if len(lmList)!=0:
            print(lmList[8])
        #FPS calculation
        detector.displayFps(img)
        
        imgRGB=cv.cvtColor(img, cv.COLOR_BGR2RGB)
        cv.imshow('capture',img)
    
        if cv.waitKey(2) & 0xFF==ord('d'):
            break

    #cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()