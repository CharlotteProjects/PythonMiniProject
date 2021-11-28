#!/usr/bin/python

import RPi.GPIO as GPIO
import Adafruit_DHT
import time

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

# LED
pinLED = 27     # pin 13
GPIO.setup(pinLED, GPIO.OUT)

# DHT11
pinDHT11 = 4  # pin 7

# UltraSound
pin_USoundTrig = 22 # pin 15
pin_USoundEcho = 23 # pin16
GPIO.setup(pin_USoundTrig, GPIO.OUT)
GPIO.setup(pin_USoundEcho, GPIO.IN)

# Buzzer
pinBuzzer = 26 # pin 37
GPIO.setup(pinBuzzer, GPIO.OUT)

# Function for Get DHT11
def GetDHT11():
    global pinDHT11
    sensor = Adafruit_DHT.DHT11
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pinDHT11)
    #humidity, temperature = Adafruit_DHT.read(sensor, pin)
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f} C*  Humidity={1:0.1f} %'.format(temperature, humidity))
        return humidity, temperature
    else:
        print('Failed to get reading. Try again!')


# Function for Set LED
def LEDonOff(on):
    if on:
        GPIO.output(pinLED, True)
        print("LED on")
        return True
    else:
        GPIO.output(pinLED, False)
        print("LED off")
        return False


# Function for checking Ultrasound
def Ultrasound():
    GPIO.output(pin_USoundTrig, False)
    time.sleep(0.5)
    GPIO.output(pin_USoundTrig, True)
    time.sleep(0.00001)
    GPIO.output(pin_USoundTrig, False)
    start = time.time()
    
    while GPIO.input(pin_USoundEcho) == 0:
        start = time.time()
    
    while GPIO.input(pin_USoundEcho) == 1:
        stop = time.time()
    elapsed = stop - start
    distance = elapsed * 34300
    distance = distance / 2
    print(distance)
    return distance


def Buzzer(long):
    num = 260
    
    time.sleep(0.3)
    for r in range(1000):
        for x in range(num):
            GPIO.output(pinBuzzer, 1)
        for x in range(num):
            GPIO.output(pinBuzzer, 0)
    
    if long:
        time.sleep(0.3)
        for r in range(1000):
            for x in range(num):
                GPIO.output(pinBuzzer, 1)
            for x in range(num):
                GPIO.output(pinBuzzer, 0)
                
        time.sleep(0.3)
        for r in range(1000):
            for x in range(num):
                GPIO.output(pinBuzzer, 1)
            for x in range(num):
                GPIO.output(pinBuzzer, 0)
