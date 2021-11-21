#!/usr/bin/python

import RPi.GPIO as GPIO
import Adafruit_DHT

GPIO.setwarnings(False)

pinLED = 27     # pin 13
pinDHT11 = 4  # pin 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(pinLED, GPIO.OUT)


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