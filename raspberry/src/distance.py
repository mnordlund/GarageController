import RPi.GPIO as GPIO
import board
import time
import logging

log = logging.getLogger("gc.dist")

distance: float = 0.0 # Distance to object in cm

def readDistance() -> float:
    GPIO.output(board.TRIGGERPIN, True)
    time.sleep(0.00001)
    GPIO.output(board.TRIGGERPIN, False)

    StartTime = time.time()
    StopTime = time.time()

    
    BreakTime = time.time()
    while GPIO.input(board.ECHOPIN) == 0:
        if (time.time() - BreakTime) > 0.03:
            log.warning("Failed to get distance")
            return 0.03
        StartTime = time.time()

    BreakTime = time.time()
    while GPIO.input(board.ECHOPIN) == 1:
        if (time.time() - BreakTime) > 0.03:
            log.warning("Failed to get distance")
            return 0.03
        StopTime = time.time()

    return StopTime - StartTime

def median(a, b, c):
    """
    Adapted from:
    https://stackoverflow.com/questions/17158667/minimum-no-of-comparisons-to-find-median-of-3-numbers
    """
    x = a - b
    y = b - c
    z = a - c

    if x * y > 0:
        return b
    if x * z > 0:
        return c
    
    return a

def updateDistance():
    echos = []
    for x in range(3):
        echos.append(readDistance())
        time.sleep(0.03)

    medianEcho = median(echos[0], echos[1], echos[2])

    if medianEcho < 0.03:
        distance = (medianEcho * 34300) / 2

def getDistance() -> float:
    """ Returns the current distance """
    return distance


