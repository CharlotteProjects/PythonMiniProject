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

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        return characters[0]
    if(GPIO.input(C2) == 1):
        return characters[1]
    if(GPIO.input(C3) == 1):
        return characters[2]
    if(GPIO.input(C4) == 1):
        return characters[3]
    GPIO.output(line, GPIO.LOW)
    return "-"

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
        return get