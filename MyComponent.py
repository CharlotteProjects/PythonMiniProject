#!/usr/bin/python

import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import pygame

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

humi = 0
temp = 0

# Function for Get DHT11
def GetDHT11():
    global pinDHT11
    global humi 
    global temp

    sensor = Adafruit_DHT.DHT11
    #humidity, temperature = Adafruit_DHT.read_retry(sensor, pinDHT11)
    humidity, temperature = Adafruit_DHT.read(sensor, pinDHT11)
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f} C*  Humidity={1:0.1f} %'.format(temperature, humidity))
        humi = humidity
        temp = temperature
        return humidity, temperature
    else:
        print('Failed to get reading. return the last record!')
        return humi, temp


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


def playMusic():
    pygame.mixer.init()
    pygame.mixer.music.load('PalletTown.mp3')
    pygame.mixer.music.play()
    
def stopMusic():
    pygame.mixer.music.stop()