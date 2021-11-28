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
import time

########## Time Variable ##########

time_addNextDHT11 = 4            # every 4 second get DHT11
time_getDHT11 = time.time()    # next time for getting  DHT11

time_addNextLED = 10               # every 10 second close LED
time_closeLED = time.time()      # next time for closing LED

time_addNextLCD = 6                 # every 6 second change LCD
time_changeLCD = time.time()  # next time for changing LCD

time_addNextUltraSound = 8    # CD 8 second to get Next UltraSound 
time_getUltraSound = time.time() 

########## Control Variable ##########

LEDon = False
displayLCD = 0

# less than 100 cm ,it will start OpenCV
ultraSoundnow = 0
ultraSoundRange = 100

# For checking Mask
OpenCV_Detecting = False
DisplayCameraInSt7735 = False

cameraNumber = 0

noFace = 0
noMask = 0
Mask = 0
customCount = 0
customCountNoMask = 0

########## Function ##########

#When get PIR
def getPIR(channel):
    global LEDon, time_closeLED, time_addNextLED
    time_closeLED = time.time()  + time_addNextLED
    
    print("Get Moving")
    
    if not LEDon:
        LEDon = MyComponent.LEDonOff(True)

# For LCD loop
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

# For cal count
def AddOpenCVCount(num):
    global noFace
    global noMask
    global Mask
    
    if num == 0:
        noFace = noFace + 1
    elif num == 1:
        Mask = Mask + 1
    else:
        noMask = noMask + 1

# For detect somebody have mask or not
def DetectingMask():
    global noFace
    global noMask
    global Mask
    global customCount
    global customCountNoMask
    print("noFace {0}, noMask {1}, Mask {2}".format(noFace, noMask, Mask))
    
    # custome add one
    customCount = customCount + 1
    
    if noFace > noMask + Mask:
        print("No Detect")
    elif noMask >= Mask:
        print("No Mask")
        MyLCD1602.DisplayLCD_OpenCV(False)
        # add the count
        customCountNoMask = customCountNoMask + 1
        time_changeLCD = time.time() + time_addNextUltraSound
        MyComponent.Buzzer(True)
        # if somebody have no mask, it will take a photo
        # it will send an Email
        MyOpenCV.ScreenShotwithEmail()
    else:
        print("Have Mask")
        MyLCD1602.DisplayLCD_OpenCV(True)
        time_changeLCD = time.time() + time_addNextUltraSound
    
    noFace = 0
    noMask = 0
    Mask = 0


def CheckingInput(num):
    global cameraNumber
    global disp
    global DisplayCameraInSt7735
    
    if num != "-":
        print(num)
    
    if num == "1":
        MyOpenCV.DisplayCamera(False)
        DisplayCameraInSt7735 = False
    elif num == "2":
        MyOpenCV.DisplayCamera(True, disp)
        DisplayCameraInSt7735 = True
    elif num == "A":
        cameraNumber = 0
    elif num == "B":
        cameraNumber = 2
    elif num == "C":
        MyOpenCV.ScreenShot(cameraNumber)
    elif num == "D":
        MyOpenCV.ScreenShotwithEmail()

########## GPIO init ##########

GPIO.setwarnings(False)

pinPIR = 17    # 11 號腳

GPIO.setup(pinPIR, GPIO.IN)

GPIO.add_event_detect(pinPIR, GPIO.RISING,callback = getPIR, bouncetime=50)


########## Init ##########

global disp
disp = MyST7735.init_ST7735()

# Display the Login Title and Member
# Close Testing
MyST7735.DisplayLogin(disp)
MyComponent.Buzzer(False)

########## Main Program ##########
try:
    while True:
        
        CheckingInput(MyKeypad.DetectKeypad())

        # Get DHT11
        if time.time() >= time_getDHT11:
            time_getDHT11 = time.time() + time_addNextDHT11
            humi, temp = MyComponent.GetDHT11()

        # Set LED
        if time.time() >= time_closeLED and LEDon:
            LEDon = MyComponent.LEDonOff(False)

        # UltraSound and OpenCV
        if not OpenCV_Detecting:
            ultraSoundnow = MyComponent.Ultrasound()
            if ultraSoundnow <= ultraSoundRange:
                # Close Testing
                OpenCV_Detecting = True
                time_getUltraSound = time.time() + time_addNextUltraSound
            else:
                pass
        else:
            if time.time() <= time_getUltraSound:
                AddOpenCVCount(MyOpenCV.DetectfaceMask(cameraNumber))
            else:
                # it will check the distance, if less than 100 will keep on detect
                DetectingMask()
                ultraSoundnow = MyComponent.Ultrasound()
                if ultraSoundnow <= ultraSoundRange:
                    OpenCV_Detecting = True
                    time_getUltraSound = time.time() + time_addNextUltraSound
                    AddOpenCVCount(MyOpenCV.DetectfaceMask(cameraNumber))
                else:
                    OpenCV_Detecting = False

        # Change LCD
        if time.time() >= time_changeLCD:
            changeLCD()

        # Display
        if not DisplayCameraInSt7735:
            MyST7735.DisplayDHT11(disp, humi, temp)

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

