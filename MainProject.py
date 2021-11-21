#!/usr/bin/python
#
# pin 3 , 5 for LCD
# pin 7   for DHT11
# pin 11 for PIR
# pint 13 for LED
# pin 18, 19, 22, 23, 24 for ST7735
#
#
#My library
import MyComponent, MyST7735, MyLCD1602

import RPi.GPIO as GPIO
import time

########## Time Variable ##########

time_addNextDHT11 = 2            # every 2 second get DHT11
time_getDHT11 = time.time()    # next time for getting  DHT11

time_addNextLED = 10               # every 10 second close LED
time_closeLED = time.time()      # next time for closing LED

time_addNextLCD = 6                 # every 6 second change LCD
time_changeLCD = time.time()   # next time for changing LCD

########## Control Variable ##########

LEDon = False
displayLCD = 0

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

########## Init ##########

global disp
disp = MyST7735.init_ST7735()


########## GPIO init ##########

GPIO.setwarnings(False)

pinPIR = 17    # 11 號腳

GPIO.setup(pinPIR, GPIO.IN)

GPIO.add_event_detect(pinPIR, GPIO.RISING,callback = getPIR, bouncetime=50)

########## Main Program ##########
try:
    while True:
        
        # Get DHT11
        if time.time() >= time_getDHT11:
            time_getDHT11 = time.time() + time_addNextDHT11
            humi, temp = MyComponent.GetDHT11()

        # Set LED
        if time.time() >= time_closeLED and LEDon:
            LEDon = MyComponent.LEDonOff(False)

        # Change LCD
        if time.time() >= time_changeLCD:
            changeLCD()

        # Display
        MyST7735.DisplayDHT11(disp, humi, temp)
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    MyLCD1602.CloseLCD()
    print("End of Program")
    GPIO.cleanup()

