import RPi.GPIO as GPIO
import board
import time
import logging

log = logging.getLogger("gc.dist")

distance: float = 0.0 # Distance to object in cm

def updateDistance():
    """ 
    Called every cycle to update the distance 

    Code adapted from: https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/
    """
    global distance
    GPIO.output(board.TRIGGERPIN, True)
    time.sleep(0.00001)
    GPIO.output(board.TRIGGERPIN, False)

    StartTime = time.time()
    StopTime = time.time()

    
    BreakTime = time.time()
    while GPIO.input(board.ECHOPIN) == 0:
        if (time.time() - BreakTime) > 0.03:
            log.warning("Failed to get distance")
            return
        StartTime = time.time()

    BreakTime = time.time()
    while GPIO.input(board.ECHOPIN) == 1:
        if (time.time() - BreakTime) > 0.03:
            log.warning("Failed to get distance")
            return
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime

    distance = (TimeElapsed * 34300) / 2

def getDistance() -> float:
    """ Returns the current distance """
    return distance


