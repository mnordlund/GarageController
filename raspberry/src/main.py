import sys
import time
import signal
import firebase_controller as fb
import board
import doorHandler as door
import logging
import distance

log = logging.getLogger("gc")
logfilename = None # If no log is set through arguments log to console
firebaseconfig = "/home/pi/firebaseconfig.json"


def init():
    logging.basicConfig(filename=logfilename, format="%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.ERROR)
    log.setLevel(logging.INFO)
    log.setLevel(logging.DEBUG) # Set when debugging


def sigintHandler(sig, frame):
    """ Handles ctrl - c """
    log.debug("sigint handler")
    board.cleanup()
    sys.exit(0)

def parseArgs():
    global logfilename
    global firebaseconfig

    if(len(sys.argv) > 1):
        logfilename = sys.argv.pop(1)
    if(len(sys.argv) > 1):
        firebaseconfig = sys.argv.pop(1)


def main() -> int:
    """ 
    Main function

    Initializes all modules and runs the main loop
    """
    parseArgs()
    init()
    signal.signal(signal.SIGINT, sigintHandler)
    signal.signal(signal.SIGTERM, sigintHandler)

    log.info("GarageController starting")

    board.init()
    fb.init(firebaseconfig)

    log.info("Waiting for database to connect")

    while not fb.isConnected():
        time.sleep(3)

    log.info("Database connected")

    fb.isOperateCommand() # If operate is set on bootup ignore it as it could be old.

    log.info("Entering main loop")

    closed = True
    opened = True

    while True: # Loop forever
        distance.updateDistance()
        locked = fb.isLocked()
        if(not locked):
            if(fb.isOperateCommand()):
                #door.operateDoor()
                log.debug("Should open door!")

        fb.status['doorClosed'] = door.isDoorClosed()
        fb.status['doorOpened'] = door.isDoorOpened()
        fb.status['carInGarage'] = door.isCarInGarage()
        fb.status['locked'] = locked
        
        fb.writeStatus()
        time.sleep(1)


if __name__ == "__main__":
    sys.exit(main())
