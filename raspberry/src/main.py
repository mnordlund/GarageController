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
    logging.basicConfig(filename=logfilename, filemode = 'a', format="%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.ERROR)
    log.setLevel(logging.INFO)
    log.setLevel(logging.DEBUG) # Set when debugging


def sigintHandler(sig, frame):
    """ Handles ctrl - c """
    log.debug("sigint handler")
    board.cleanup()
    fb.cleanup() # Not working properly for now an could hang, so we skip the cleanup
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
    fb.setupCallbacks()
    log.info("Entering main loop")

    while True: # Loop forever
        distance.updateDistance()

        update = False
        if(door.isDoorClosed() != fb.status['doorClosed']):
            fb.status['doorClosed'] = door.isDoorClosed()
            log.info("Door closed: "+ str(fb.status['doorClosed']))
            update = True

        if(door.isDoorOpened() != fb.status['doorOpened']):
            fb.status['doorOpened'] = door.isDoorOpened()
            log.info("Door Opened: " + str(fb.status['doorOpened']))
            update = True
        
        if(door.isCarInGarage() != fb.status['carInGarage'] and not fb.status['doorOpened']):
            fb.status['carInGarage'] = door.isCarInGarage()
            log.info("Car in garage: " + str(fb.status['carInGarage']))
            update = True
        
        if(update):
            fb.writeStatus()

        time.sleep(0.5)


if __name__ == "__main__":
    sys.exit(main())
