import RPi.GPIO as GPIO
import logging 

log = logging.getLogger("gc.b")
# Note choose a pin that has pull down on by default to avoid opening the door on reboot.
DOORPIN = 17
ECHOPIN = 27
TRIGGERPIN = 22
REEDPIN = 23

def init():
    """ Initializes GPIOS """
    log.debug("Setup GPIO")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DOORPIN, GPIO.OUT)
    GPIO.setup(ECHOPIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(TRIGGERPIN, GPIO.OUT)
    GPIO.setup(REEDPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def cleanup():
    """ Cleans up GPIOS """
    log.debug("Clean up GPIOS")
    GPIO.cleanup()