#!/usr/bin/python
# coding: utf-8
#
# pin 3 , 5 for LCD
# pin 7   for DHT11
# pin 11 for PIR
# pin 13 for LED
# pin 15 for USoundTrig
# pin 16 for USoundEcho
# pin 18, 19, 22, 23, 24 for ST7735
# pin 35(13), 33(19), 31(26), 29(5) for Keypad -
# pin 40(21), 38(20), 26(16), 32(21) for Keypad -
#

#My library
import MyComponent
import MyST7735
import MyLCD1602
import MyOpenCV
import MyKeypad

import RPi.GPIO as GPIO
import subprocess
import time
import csv

#################### Time Variable ####################

time_addNextDHT11 = 4            # every 4 second get DHT11
time_getDHT11 = time.time()    # next time for getting  DHT11

time_addNextLED = 5               # every 5 second close LED
time_closeLED = time.time()      # next time for closing LED

time_addNextLCD = 6                 # every 6 second change LCD
time_changeLCD = time.time()  # next time for changing LCD

time_addNextUltraSound = 20    # CD 20 second to get Next UltraSound 
time_getUltraSound = time.time() 

#################### Control Variable ####################

LEDon = False
displayLCD = 0

# less than 100 cm ,it will start OpenCV
ultraSoundnow = 0
"""
ultraSoundRange = 100
"""
ultraSoundRange = 10

# For checking Mask
OpenCV_Detecting = False
DisplayCameraInSt7735 = False

# set the daflaut camera
cameraNumber = 0

customCount = 0
customCountNoMask = 0

#################### Function ####################

#When get PIR
def getPIR(channel):
    global LEDon, time_closeLED, time_addNextLED
    time_closeLED = time.time()  + time_addNextLED
    
    print("Get Moving")
    # set the floor
    MyST7735.SetFloor(1, True)
    if not LEDon:
        LEDon = MyComponent.LEDonOff(True)

#---------------------------------------------- For LCD loop ----------------------------------------------
def changeLCD():
    global displayLCD, humi, temp, time_changeLCD, time_addNextLCD
    time_changeLCD = time.time() + time_addNextLCD

    if displayLCD == 0:
        MyLCD1602.DisplayLCD("Welcome!", "MyShop")
    elif displayLCD == 1:
        MyLCD1602.DisplayLCD_DHT11(humi, temp)
    else:
        pass
    displayLCD += 1
    if displayLCD > 1:
        displayLCD = 0

#---------------------------------------------- For detect somebody have mask or not ----------------------------------------------
def GetOpenCVResult():
    global customCountNoMask
    print("open the openCV.csv")
    result = ""
    with open('/home/pi/Project/csv/openCVResult.csv', 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            result = row[0]
            print(result)
            
    if result == "not_weared_mask":
        print("No Mask")
        customCountNoMask = customCountNoMask + 1
        MyLCD1602.DisplayLCD_OpenCV(False)
        MyComponent.Buzzer(True)
        MyComponent.playSomeoneNoMaskMusic()
        # if somebody have no mask, it will take a photo
        # it will send an Email
        MyOpenCV.ScreenShotwithEmail()
        time_changeLCD = time.time() + time_addNextUltraSound
    elif result == "weared_mask":
        print("Have Mask")
        MyLCD1602.DisplayLCD_OpenCV(True)
        time_changeLCD = time.time() + time_addNextUltraSound


#---------------------------------------------- Check the Keypad Input ----------------------------------------------
def CheckingInput(num):
    global cameraNumber
    global disp
    global DisplayCameraInSt7735
    global OpenCV_Detecting
    global time_getUltraSound
    global time_addNextUltraSound
    
    if num != "-":
        print(num)
    
    if num == "1":
        MyOpenCV.DisplayCamera(False)
        MyOpenCV.CloseAllWindoes()
        DisplayCameraInSt7735 = False
        OpenCV_Detecting = False
        
    elif num == "2":
        time_getUltraSound = time.time() + time_addNextUltraSound
        print(time_getUltraSound)
        MyOpenCV.DisplayCamera(True, disp)
        DisplayCameraInSt7735 = True
        OpenCV_Detecting = True

    elif num == "A":
        cameraNumber = 0
        print("Change to Carmera A")
    elif num == "B":
        cameraNumber = 2
        print("Change to Carmera B")
    elif num == "C":
        MyOpenCV.ScreenShot(cameraNumber)
    elif num == "D":
        MyOpenCV.ScreenShotwithEmail()

#################### GPIO init ####################

GPIO.setwarnings(False)

pinPIR = 17    # 11 號腳

GPIO.setup(pinPIR, GPIO.IN)

GPIO.add_event_detect(pinPIR, GPIO.RISING,callback = getPIR, bouncetime=50)


#################### Init ####################

global disp
disp = MyST7735.init_ST7735()

# Display the Login Title and Member

"""
MyComponent.Buzzer(False)
MyComponent.playMusic()
MyST7735.DisplayLogin(disp)

"""
#################### Main Program ####################
try:
    while True:
        
        CheckingInput(MyKeypad.DetectKeypad())

        # Get DHT11
        if time.time() >= time_getDHT11 and not OpenCV_Detecting:
            time_getDHT11 = time.time() + time_addNextDHT11
            humi, temp = MyComponent.GetDHT11()

        # Set LED
        if time.time() >= time_closeLED and LEDon:
            LEDon = MyComponent.LEDonOff(False)
            # close the LED
            MyST7735.SetFloor(1, False)
        

        # UltraSound and OpenCV
        if not OpenCV_Detecting:
            #ultraSoundnow =120
            ultraSoundnow = MyComponent.Ultrasound()
            if ultraSoundnow <= ultraSoundRange:
                # Open Detect Mode
                OpenCV_Detecting = True
                time_getUltraSound = time.time() + time_addNextUltraSound
                # Open Extra Code For OpenCV
                if cameraNumber == 0:
                    subprocess.Popen(["python3", 'ExtraOpenCV.py'])
                else:
                    subprocess.Popen(["python3", 'ExtraOpenCV2.py'])
                # Music
                MyComponent.playSomeoneInMusic()
                # add customer Count
                customCount = customCount + 1
                print("Total Customer : {0} , NoMask Customer : {1}".format(customCount, customCountNoMask))
            else:
                pass
        else:
            if time.time() >= time_getUltraSound:
                GetOpenCVResult()
                OpenCV_Detecting = False

        # Change LCD
        if time.time() >= time_changeLCD:
            changeLCD()

        # Display DHT11
        if not DisplayCameraInSt7735:
            MyST7735.DisplayDHT11(disp, humi, temp)
        else:
            # Display Face Detection
            #print(cameraNumber)
            MyOpenCV.DetectfaceMask(cameraNumber)
            # Cannot same time detect
            time_getUltraSound = time.time() + time_addNextUltraSound

        # if no OpenCV detecting , it will wait for 0.1s
        if not OpenCV_Detecting:
            time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    MyLCD1602.CloseLCD()
    MyOpenCV.CloseAllWindoes()
    print("End of Program")
    GPIO.cleanup()
    
    