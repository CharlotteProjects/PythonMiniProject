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
import MyWeather
import MyMongoDB

import RPi.GPIO as GPIO
import subprocess
import time
import csv

from bluepy import btle

#################### Init BLE ####################
class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        # init the BLE connect with ESP32
        btle.DefaultDelegate.__init__(self)
        print("init BLE")

    def handleNotification(self, cHandle, data):
        # When Get data from the ESP32
        i = int.from_bytes(data, byteorder='big')
        #print(i)
        if i == 1:
            MyST7735.SetFloor(2, True)
            #print("on")
        else:
            MyST7735.SetFloor(2, False)
            #print("off")
    

#################### Time Variable ####################
uploadTime = 0                   # every 5 time will upload
time_addNextDHT11 = 4            # every 4 second get DHT11
time_getDHT11 = time.time()      # next time for getting  DHT11

time_addNextLED = 5              # every 5 second close LED
time_closeLED = time.time()      # next time for closing LED

time_addNextLCD = 6              # every 6 second change LCD
time_changeLCD = time.time()     # next time for changing LCD

time_addNextUltraSound = 20      # CD 20 second to get Next UltraSound 
time_getUltraSound = time.time() 

#################### Control Variable ####################

LEDon = False
displayLCD = 0

# less than 10 cm ,it will start OpenCV
ultraSoundnow = 0
ultraSoundRange = 10

# For checking Mask
OpenCV_Detecting = False
DisplayCameraInSt7735 = False
DisplayWeather = False

# set the daflaut camera
cameraNumber = 0

# the customCount and no mask count
customCount = 0
customCountNoMask = 0

#################### Function ####################

#---------------------------------------------- For Getting PIR ----------------------------------------------
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
        # Setting the default LCD
        MyLCD1602.DisplayLCD("Welcome!", "MyShop")
    elif displayLCD == 1:
        # Display the humidity, temperature 
        MyLCD1602.DisplayLCD_DHT11(humi, temp)
    else:
        pass

    # This is for change the LCD choose
    displayLCD += 1
    if displayLCD > 1:
        displayLCD = 0

#---------------------------------------------- For detect somebody have mask or not ----------------------------------------------
def GetOpenCVResult():
    global customCountNoMask
    print("open the openCV.csv")
    result = ""

    # open the CSV from getting the result
    with open('/home/pi/Project/csv/openCVResult.csv', 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            result = row[0]
            print(result)
    
    # checking the CSV result
    # if someone no mask
    if result == "not_weared_mask":
        print("No Mask")
        customCountNoMask = customCountNoMask + 1
        # upload the custom count to database
        MyMongoDB.UploadCustomer(customCount, customCountNoMask)
        # change the LCD Display
        MyLCD1602.DisplayLCD_OpenCV(False)
        # Play buzzer and Sound
        MyComponent.Buzzer(True)
        MyComponent.playSomeoneNoMaskMusic()

        # if somebody have no mask, it will take a photo
        # it will send an Email
        MyOpenCV.ScreenShotwithEmail()
        time_changeLCD = time.time() + time_addNextUltraSound
    # if someone has mask
    elif result == "weared_mask":
        print("Have Mask")
        # change the LCD Display
        MyLCD1602.DisplayLCD_OpenCV(True)
        time_changeLCD = time.time() + time_addNextUltraSound


#---------------------------------------------- Checking OnClick Keypad Input ----------------------------------------------
def CheckingInput(num):
    global cameraNumber
    global disp
    global DisplayCameraInSt7735
    global DisplayWeather
    global OpenCV_Detecting
    global time_getUltraSound
    global time_addNextUltraSound
    global Weather_data
    global customCount
    global customCountNoMask
    
    # nothing
    if num != "-":
        print(num)
    
    # if OnClick key 1, then ST7735 will display the mian screen
    if num == "1":
        MyOpenCV.DisplayCamera(False)
        MyOpenCV.CloseAllWindoes()
        DisplayCameraInSt7735 = False
        OpenCV_Detecting = False
        DisplayWeather = False
        MyComponent.Buzzer(False)
    
    # if OnClick key 2, then ST7735 will display the camera
    elif num == "2":
        time_getUltraSound = time.time() + time_addNextUltraSound
        print(time_getUltraSound)
        MyOpenCV.DisplayCamera(True, disp)
        DisplayCameraInSt7735 = True
        OpenCV_Detecting = True
        DisplayWeather = False
        MyComponent.Buzzer(False)
    
    # if OnClick key 3, then ST7735 will display the weather report (it will display 4 days)
    elif num == "3":
        MyST7735.DisplayFutureTemp(disp, Weather_data)
        DisplayWeather = True
        OpenCV_Detecting = False
        MyComponent.Buzzer(False)
    
    # if OnClick key 4, then ST7735 will display the customer count and no mask customer count , that give data from database
    elif num == "4":
        MyST7735.DisplayCustomer(disp, customCount, customCountNoMask)
        DisplayWeather = True
        OpenCV_Detecting = False
        MyComponent.Buzzer(False)
    
    # if OnClick key A, then will change to the Carmera A for Face Detection
    elif num == "A":
        cameraNumber = 0
        print("Change to Carmera A")
        MyComponent.Buzzer(False)
    
    # if OnClick key B, then will change to the Carmera B for Face Detection
    elif num == "B":
        cameraNumber = 2
        print("Change to Carmera B")
        MyComponent.Buzzer(False)
    
    # if OnClick key C, then will screen shot the camera photo
    elif num == "C":
        MyOpenCV.ScreenShot(cameraNumber)
        MyComponent.Buzzer(False)
    
    # if OnClick key D, then will screen shot the camera photo and send email
    elif num == "D":
        MyOpenCV.ScreenShotwithEmail()
        MyComponent.Buzzer(False)

#---------------------------------------------- BLE Initialisation ----------------------------------------------
# For init the BLE
def InitBLE():
    global p
    p = btle.Peripheral('7c:9e:bd:04:bf:46') # address
    p.setDelegate(MyDelegate())
    # init the BLE address
    svc = p.getServiceByUUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
    ch = svc.getCharacteristics("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")[0]

    setup_data = b"\x01\00"
    p.writeCharacteristic(ch.valHandle+1, setup_data)

#################### GPIO init ####################

GPIO.setwarnings(False)

pinPIR = 17    # 11 pin

GPIO.setup(pinPIR, GPIO.IN)

# Setup the Interrupt function for the PIR sensor
GPIO.add_event_detect(pinPIR, GPIO.RISING,callback = getPIR, bouncetime=50)


#################### Init ####################

# init the ST7735 to the disp
global disp
disp = MyST7735.init_ST7735()

# Display the Login Title and Member
# play music
MyComponent.Buzzer(False)
MyComponent.playMusic()
# init the BLE
InitBLE()
# display the Login the information and Animation in the ST7735
MyST7735.DisplayLogin(disp)
# Get Data from the Weather report website
Weather_data = MyWeather.GetWeatherReport()
# Init the MongoDB Database
MyMongoDB.InitMyDB()
# Get customer data from the MongoDB Database
customCount = MyMongoDB.GetCustomer()
customCountNoMask = MyMongoDB.GetNoMaskCustomer()

#################### Main Program ####################
try:
    while True:
        
        # Get Input
        CheckingInput(MyKeypad.DetectKeypad())
        
        # Get BLE
        try:
            if p.waitForNotifications(1.0):
                continue
        except:
                pass

        # Get DHT11
        if time.time() >= time_getDHT11 and not OpenCV_Detecting:
            time_getDHT11 = time.time() + time_addNextDHT11
            humi, temp = MyComponent.GetDHT11()
            uploadTime = uploadTime + 1
            if uploadTime >= 5:
                uploadTime = 0
                MyMongoDB.UploadDHT11(humi, temp)

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
                MyMongoDB.UploadCustomer(customCount, customCountNoMask)
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
            if not DisplayWeather:
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