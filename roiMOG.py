"""
@author :yan
@create-date :2021/11/12

只對有興趣的區域框選

[X]目前有沒有動靜會停止的BUG
        if not len(contours) ==0:

[x]不要自動調節曝光
cap.set(cv2.CAP_PROP_EXPOSURE, 40)  
"""


import numpy as np

import cv2


#for ROI 
upper_left = (100-50,100-50)
bottom_right = (500+50, 400+50)
# upper_left = (100,100)
# bottom_right = (400, 300)
#---

cap = cv2.VideoCapture(1)
# cap.set(cv2.CAP_PROP_EXPOSURE, 40) #webcam曝光值設定
# cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT,964)

fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=50)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
while(1):
    
    ret, frame = cap.read()
    #ROI plot
    cv2.rectangle(frame, upper_left, bottom_right, (100, 50, 200), 5)
    #----
    roi_image = frame[upper_left[1] : bottom_right[1], upper_left[0] : bottom_right[0]]

    fgmask = fgbg.apply(roi_image) #frame - >roi_image
    #只要移動的(open處理)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    contours, hierarchy = cv2.findContours(fgmask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    # print(len(contours))
#------
    if not len(contours) ==0:
        areas = [cv2.contourArea(c) for c in contours]
        max_index = np.argmax(areas)
        cnt=contours[max_index]
        x,y,w,h = cv2.boundingRect(cnt)
        # img=cv2.drawContours(frame,cnt,-1,(0,255,0),5) 
    #------
        # x,y,w,h = cv2.boundingRect(contours)
        # img=cv2.drawContours(frame,contours,-1,(0,255,0),5)  
    #---
        # cv2.imshow('frame',fgmask)

        #這裡要加左上角起始點for ROI
        x=x+upper_left[0]
        y=y+upper_left[1]
        cv2.rectangle(frame,(x,y),(x+w,y+h), (0,255,0),2)#cv2.rectangle(影像, 頂點座標, 對向頂點座標, 顏色, 線條寬度)
    cv2.imshow('drawimg',frame)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()