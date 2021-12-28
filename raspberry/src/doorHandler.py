import RPi.GPIO as GPIO
import board
import time
import logging

log = logging.getLogger("gc.dh")

def operateDoor():
    log.info("Operating door")
    GPIO.output(board.DOORPIN, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(board.DOORPIN, GPIO.LOW)

