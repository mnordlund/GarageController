import RPi.GPIO as GPIO
import logging 

log = logging.getLogger("gc.b")
# Note choose a pin that has pull down on by default to avoid opening the door on reboot.
DOORPIN = 17

def init():
    """ Initializes GPIOS """
    log.debug("Setup GPIO")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DOORPIN, GPIO.OUT)

def cleanup():
    """ Cleans up GPIOS """
    log.debug("Clean up GPIOS")
    GPIO.cleanup()