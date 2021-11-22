import numpy as np
import cv2
import random

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
face_cascade = cv2.CascadeClassifier('/home/pi/Downloads/frontalface.xml')
eye_cascade = cv2.CascadeClassifier('/home/pi/Downloads/eye.xml')
mouth_cascade = cv2.CascadeClassifier('/home/pi/Downloads/mouth.xml')
upper_body = cv2.CascadeClassifier('/home/pi/Downloads/upperbody.xml')



# Adjust threshold value in range 80 to 105 based on your light.
bw_threshold = 80

# User message
font = cv2.FONT_HERSHEY_SIMPLEX
org = (30, 30)
weared_mask_font_color = (255, 255, 255)
not_weared_mask_font_color = (0, 0, 255)
thickness = 2
font_scale = 1
weared_mask = "Thank You for wearing MASK"
not_weared_mask = "Please wear MASK to defeat Corona"
result = ""
# Read video
cap = cv2.VideoCapture(0)

while 1:
    # Get individual frame
    ret, img = cap.read()
    img = cv2.flip(img,1)

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
        cv2.putText(img, "No face found", org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)
        result = "No face found"
    elif(len(faces) == 0 or len(faces) == 1  and len(faces) == 0 and  len(mouth_rects) >= 1 ):
        # It has been observed that for white mask covering mouth, with gray image face prediction is not happening
        cv2.putText(img, weared_mask, org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)
        result = "weared_mask"
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
                    result = "not_weared_mask"
                    cv2.putText(img, not_weared_mask, org, font, font_scale, not_weared_mask_font_color, thickness, cv2.LINE_AA)
                #cv2.rectangle(img, (mx, my), (mx + mh, my + mw), (0, 0, 255), 3)
                    break
    print(len(faces), len(faces_bw), len(mouth_rects))
    print(result)
    
    # Show frame with results
    cv2.imshow('Mask Detection', img)
    #k = cv2.waitKey(30) & 0xff
    #if k == 27:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video
cap.release()
cv2.destroyAllWindows()



if(len(faces) == 0 and len(faces_bw) == 0):
    cv2.putText(img, "No face found", org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)
    
elif(len(faces) > 0 and len(faces_bw) == 0 or len(faces_bw) > 1 and len(mouth_rects) == 0):
    # It has been observed that for white mask covering mouth, with gray image face prediction is not happening
    cv2.putText(img, weared_mask, org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)
else:
    # Draw rectangle on gace
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
    for (mx, my, mw, mh) in mouth_rects:
        if(y < my < y + h and len(mouth_rects) > 0 and len(faces_bw) == 0 or len(faces_bw) > 1 and len(faces) > 0):
        # Face and Lips are detected but lips coordinates are within face cordinates which means lips prediction is true and
        # person is not waring mask
            cv2.putText(img, not_weared_mask, org, font, font_scale, not_weared_mask_font_color, thickness, cv2.LINE_AA)
            #cv2.rectangle(img, (mx, my), (mx + mh, my + mw), (0, 0, 255), 3)
            break






