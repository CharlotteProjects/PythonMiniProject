#!/usr/bin/env python
# coding: utf-8

import cv2
import multiprocessing
import numpy as np
import math
import os
import time
import random
import csv
import MyEmail

count = 0
roundCount = 0
lifeTime = time.time()
startTime = time.time()

face_cascade = cv2.CascadeClassifier('OpenCV/frontalface.xml')
eye_cascade = cv2.CascadeClassifier('OpenCV/eye.xml')
mouth_cascade = cv2.CascadeClassifier('OpenCV/mouth.xml')
upper_body = cv2.CascadeClassifier('OpenCV/upperbody.xml')

def faceMask(capNum):
    global count
    global startTime
    global lifeTime
    global roundCount
    global saveImg
    # Adjust threshold value in range 80 to 105 based on your light.
    bw_threshold = 90

    # User message
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (30, 30)
    weared_mask_font_color = (255, 255, 255)
    not_weared_mask_font_color = (0, 0, 255)
    thickness = 2
    font_scale = 1
    weared_mask = "Thank You for wearing MASK"
    not_weared_mask = "Please wear MASK "
    result = []
    
    # Read video
    cap = cv2.VideoCapture(capNum)

    while 1:
        # Get individual frame
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        saveImg = cv2.flip(img, 1)
        # Convert Image into gray
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Convert image in black and white
        (thresh, black_and_white) = cv2.threshold(gray, bw_threshold, 255, cv2.THRESH_BINARY)
        cv2.imshow('black_and_white', black_and_white)

        # detect face
        faces = face_cascade.detectMultiScale(gray, 1.3,5)

        # Face prediction for black and white
        faces_bw = face_cascade.detectMultiScale(black_and_white, 1.3,5)

        #Face detected but Lips not detected which means person is wearing mask
        mouth_rects = mouth_cascade.detectMultiScale(gray, 1.3, 5)

        if(len(faces) == 0 and len(faces_bw) == 0 and len(mouth_rects) == 0):
            result.append("No face found")
        elif(len(faces) == 0 and len(faces) == 0 and  len(mouth_rects) >= 1 ):
            # It has been observed that for white mask covering mouth, with gray image face prediction is not happening
            cv2.putText(img, weared_mask, org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)
            result.append("weared_mask")
        else:
            # Draw rectangle on gace
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = img[y:y + h, x:x + w]
                for (mx, my, mw, mh) in mouth_rects:
                    if(len(faces) == 1 and len(faces_bw) == 0 and y < my < y + h or len(mouth_rects) >= 3 ):
                # Face and Lips are detected but lips coordinates are within face cordinates which means lips prediction is true and
                # person is not waring mask
                        result.append("not_weared_mask")
                        saveImg = img
                        cv2.putText(img, not_weared_mask, org, font, font_scale, not_weared_mask_font_color, thickness, cv2.LINE_AA)
                        break
        # print the detect
        #print(len(faces), len(faces_bw), len(mouth_rects))
        
        # calc the using time
        count = count +1
        print("Time : {0:.1f}s,  count : {1}, time : {2:.1f}s ".format(time.time() - lifeTime, count, time.time() - startTime))
        
        if len(result) == 60:
            wm = 0
            nwm = 0
            roundCount = roundCount + 1
            print("Round : {0}, count : {1} speed : {2:.1f}/s".format(roundCount, count, count / (time.time() - startTime)))
            count = 0
            startTime = time.time()
            
            for i in result:
                if i == 'weared_mask':
                    wm = wm +1
                elif i == 'not_weared_mask':
                    nwm = nwm +1
            if wm > nwm:
                Finresult = 'weared_mask'
            else:
                Finresult = 'not_weared_mask'
                
            result = []
            
            #Save to CSV
            with open('csv/openCVResult.csv', 'w') as csvfile:
                fieldnames = ['Result']
                writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
                writer.writeheader()
                writer.writerow({'Result': Finresult})
                csvfile.close()
            print(Finresult)
            if Finresult == 'not_weared_mask':
                ScreenShotwithEmail()
            print("End of OpenCv Detection , Bye !") 
            #cv2.destroyAllWindows()
            return
            
        cv2.imshow('Mask Detection', img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass

    # Release video
    #cap.release()

def ScreenShotwithEmail():
    global saveImg
    if saveImg is None:
        print("No Image")
        return
    else:
        dateTime = time.strftime('%d%m%y_%H%M%S')
        cv2.imwrite(str(dateTime)+'.png', saveImg)
        print("Save Compoleted")
        MyEmail.SendEmail(str(dateTime)+'.png')

faceMask(2)