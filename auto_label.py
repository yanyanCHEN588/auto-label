"""
@author :yan
@create-date :2021/11/28


"""


import numpy as np
import cv2
import os
import time

os.chdir(os.path.dirname(__file__))

def write_txt(anno_path , obj ,width=640 ,height=640):
    with open("sav/image"+anno_path+".txt", "w") as f:
        #x, y, w, h = a['bbox']  >>>obj[1],obj[2],obj[3],obj[4]
        xc, yc = obj[1] + obj[3] / 2, obj[2] + obj[4] / 2  # xy to center
        #參考 file.write(f"{cid} {x / width:.5f} {y / height:.5f} {w / width:.5f} {h / height:.5f}\n")
        f.write(f"{obj[0]} {xc / width:.8f} {yc / height:.8f} {obj[3]*0.99999999 / width:.8f} {obj[4]*0.999999/ height:.8f}\n")


label_id= 15
obj=[label_id,0,0,0,0] #id,x,y,w,h
cap = cv2.VideoCapture(1)

#設置後
imWidth= 1280
imHeight= 720 #c310:960 ,BRIO:720
cap.set(cv2.CAP_PROP_FRAME_WIDTH,imWidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,imHeight)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(width, height)

#ROI
upper_left = (300,50)
bottom_right = (upper_left[0]+640,upper_left[1]+640)
#MOG2
fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=16)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
label_area = 0



while cap.isOpened():
    
    ret, frame = cap.read()
    k=cv2.waitKey(1)
    
    
    roi_image = frame[upper_left[1] : bottom_right[1], upper_left[0] : bottom_right[0]]
    savImage = roi_image.copy()
    #僅是單純不想要讓紅框框變成截圖對象，所以各往外劃5厚度
    cv2.rectangle(frame, (upper_left[0]-5,upper_left[1]-5), (bottom_right[0]+5,bottom_right[1]+5), (100, 50, 200), 5)
    # cv2.rectangle(frame, (upper_left[0],upper_left[1]), (bottom_right[0],bottom_right[1]), (100, 50, 200), 5)
#-----------------------MOG2--------------
    fgmask = fgbg.apply(roi_image) #frame - >roi_image
    #只要移動的(open處理)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    contours, hierarchy = cv2.findContours(fgmask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    if not len(contours) ==0:
        areas = [cv2.contourArea(c) for c in contours]
        max_index = np.argmax(areas)
        cnt=contours[max_index]
        x,y,w,h = cv2.boundingRect(cnt)
        label_area=w*h
#-----------------------MOG2--------------


    #由MOG拿到物件框框 #這裡要加左上角起始點for ROI
    x_label=x+upper_left[0]
    y_label=y+upper_left[1]
    cv2.rectangle(frame,(x_label,y_label),(x_label+w,y_label+h), (0,255,0),2)#cv2.rectangle(影像, 頂點座標, 對向頂點座標, 顏色, 線條寬度)

    #這裡的x,y是剛好ROI內的
    obj=[label_id,x,y,w,h]

    
    if  label_area > 240*240 : #(160/640 * 160/640) = 1/16 region
        name=str(int(time.time()))
        
        cv2.putText(frame, "SAVE!!"+name, (100, 50), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 5, cv2.LINE_AA)
        cv2.imwrite("sav/image"+name+".jpg", savImage)     # save frame as JPG file
        write_txt(name, obj)

    cv2.imshow('drawimg',frame)
    if k == ord('s'):
        name=str(int(time.time()))
        cv2.putText(frame, "SAVE!!"+name, (100, 50), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 5, cv2.LINE_AA)
        cv2.imwrite("save/image"+name+".jpg", savImage)     # save frame as JPG file
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

