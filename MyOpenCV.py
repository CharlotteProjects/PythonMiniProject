#!/usr/bin/env python

import cv2
import multiprocessing
import numpy as np
import math
import os
import time
import random
from PIL import Image

import MyEmail
import MyST7735

face_cascade = cv2.CascadeClassifier('OpenCV/frontalface.xml')
eye_cascade = cv2.CascadeClassifier('OpenCV/eye.xml')
mouth_cascade = cv2.CascadeClassifier('OpenCV/mouth.xml')
upper_body = cv2.CascadeClassifier('OpenCV/upperbody.xml')

saveImg = 0

disp = None
display = False

# For setting the display
def DisplayCamera(displayCamera, Mydisp = None):
    global display
    global disp
    display = displayCamera
    if Mydisp is not None:
        disp = Mydisp
        print("Display Camera")
    else:
        print("Closing Display")

def DetectfaceMask(capNum):
    global face_cascade
    global eye_cascade
    global mouth_cascade
    global upper_body
    global saveImg
    global display
    global disp
    
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
    # 0 = "No face found"
    # 1 = "weared_mask"
    # 2 = "not_weared_mask"
    result = 0
    
    # Read video
    cap = cv2.VideoCapture(capNum)

    # Get individual frame
    ret, img = cap.read()
    img = cv2.flip(img, 1)

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
        result = 0
    elif(len(faces) == 0 and len(faces) == 0 and  len(mouth_rects) >= 1 ):
        # It has been observed that for white mask covering mouth, with gray image face prediction is not happening
        cv2.putText(img, weared_mask, org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)
        result = 1
    else:
        # Draw rectangle on gace
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            for (mx, my, mw, mh) in mouth_rects:
                if(len(faces) == 1 and len(faces_bw) == 0 and y < my < y + h or len(mouth_rects) >= 3 ):
                    # Face and Lips are detected but lips coordinates are within face cordinates which means lips prediction is true and
                    # person have not waring mask
                    result = 2
                    cv2.putText(img, not_weared_mask, org, font, font_scale, not_weared_mask_font_color, thickness, cv2.LINE_AA)
                    # For save image
                    saveImg = img
                    break
    # print the detect
    #print(len(faces), len(faces_bw), len(mouth_rects))

    cv2.imshow('Mask Detection', img)
    
    if display == True and disp is not None:
        array = np.array(img)          # array is a numpy array 
        image2 = Image.fromarray(array) 
        MyST7735.DisplayCamera(disp, image2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        pass
    #    break
    # return Finresult
    # Release video
    #cap.release()
    #cv2.destroyAllWindows()
    return result

def ScreenShot(CamNum):
    camera = cv2.VideoCapture(CamNum)
    return_value, image = camera.read()
    dateTime = time.strftime('%d%m%y_%H%M%S')
    cv2.imwrite(str(dateTime)+'.png', image)
    print("Save Compoleted")


def ScreenShotwithEmail():
    global saveImg
    dateTime = time.strftime('%d%m%y_%H%M%S')
    cv2.imwrite(str(dateTime)+'.png', saveImg)
    print("Save Compoleted")
    MyEmail.SendEmail(str(dateTime)+'.png')


def CloseAllWindoes():
    cv2.destroyAllWindows()