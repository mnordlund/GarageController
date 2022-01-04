import RPi.GPIO as GPIO
import board
import time
import logging
import distance

log = logging.getLogger("gc.dh")

def operateDoor():
    log.info("Operating door")
    GPIO.output(board.DOORPIN, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(board.DOORPIN, GPIO.LOW)

def isDoorClosed() -> bool:
    """ Checks the sensor to determine if the door is closed """
    if(GPIO.input(board.REEDPIN) == 1):
        return False
    else:
        return True

def isDoorOpened() -> bool:
    """ Checks if the door is fully opened using distance """
    dist = distance.getDistance()
    if(dist < 9 and dist > 5.5):
        return True
    else:
        return False 

def isCarInGarage() -> bool:
    """ Checks if a car is in  the garage using distance """
    dist = distance.getDistance()
    if(dist < 100 and dist > 20):
        return True
    else:
        return False