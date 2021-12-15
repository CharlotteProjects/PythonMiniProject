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

# For store the one time humidity and temperature data
humi = 0
temp = 0

# Function for Get DHT11
def GetDHT11():
    global pinDHT11
    global humi 
    global temp

    sensor = Adafruit_DHT.DHT11
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pinDHT11)
    # humidity, temperature = Adafruit_DHT.read(sensor, pinDHT11)
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f} C*  Humidity={1:0.1f} %'.format(temperature, humidity))
        humi = humidity
        temp = temperature
        # return the humidity, temperature data to the main script
        return humidity, temperature
    else:
        # if Fail will return the last record
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
    # It will return the distance to the main script
    return distance


def Buzzer(long):
    num = 260
    
    # This is the short time buzz for start program
    time.sleep(0.3)
    for r in range(1000):
        for x in range(num):
            GPIO.output(pinBuzzer, 1)
        for x in range(num):
            GPIO.output(pinBuzzer, 0)
    
    # This is the long time buzz for face detect a no mask customer
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

# Play the Music (BGM) in the bluetooth speaker
def playMusic():
    pygame.mixer.init()
    pygame.mixer.music.load('Music/PalletTown.mp3')
    pygame.mixer.music.play()

# Stop the Music
def stopMusic():
    pygame.mixer.music.stop()

# Play the Music (When a customer enter shop) in the bluetooth speaker
def playSomeoneInMusic():
    pygame.mixer.init()
    pygame.mixer.music.load('Music/in.mp3')
    pygame.mixer.music.play()
    time.sleep(3)
    playMusic()

# Play the Music (When a customer who without mask)  in the bluetooth speaker
def playSomeoneNoMaskMusic():
    pygame.mixer.init()
    pygame.mixer.music.load('Music/nomask2.mp3')
    pygame.mixer.music.play()
    time.sleep(3)
    playMusic()