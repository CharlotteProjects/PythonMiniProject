import RPi.GPIO as GPIO
import time

L1 = 5
L2 = 6
L3 = 13
L4 = 19

C1 = 12
C2 = 16
C3 = 20
C4 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Setting the GPIO pin output
GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

# Setting the GPIO pin input
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Function for check the input and return the input Key name
def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        GPIO.output(line, GPIO.LOW)
        return characters[0]
    if(GPIO.input(C2) == 1):
        GPIO.output(line, GPIO.LOW)
        return characters[1]
    if(GPIO.input(C3) == 1):
        GPIO.output(line, GPIO.LOW)
        return characters[2]
    if(GPIO.input(C4) == 1):
        GPIO.output(line, GPIO.LOW)
        return characters[3]
    GPIO.output(line, GPIO.LOW)
    return "-"

# For Detecting the Keypad onClick
# It will call by MainProject.py and return the input
def DetectKeypad():
    get = "-"
    try:
        get = readLine(L1, ["1","2","3","A"])
        if get == "-":
            get = readLine(L2, ["4","5","6","B"])
        if get == "-":
            get = readLine(L3, ["7","8","9","C"])
        if get == "-":
            get = readLine(L4, ["*","0","#","D"])
    except KeyboardInterrupt:
        print("\nApplication stopped!")
    finally:
        # it will return the input to the MainProject.py
        # if no input will return the "-"
        return get