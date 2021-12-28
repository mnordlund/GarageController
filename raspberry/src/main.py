import sys
import time
import signal
import firebase_controller as fb
import board
import doorHandler as door
import logging

log = logging.getLogger("gc")
logfilename = None # If no log is set through arguments log to console
firebaseconfig = "/home/pi/firebaseconfig.json"


def init():
    logging.basicConfig(filename=logfilename, format="%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
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
        print("logfilename:", logfilename )
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

    log.debug("GarageController starting")

    board.init()
    while not fb.init(firebaseconfig):
        time.sleep(3)

    fb.isOperateCommand() # If operate is set on bootup ignore it as it could be old.

    log.debug("Entering main loop")
    while True: # Loop forever
        if(fb.isOperateCommand()):
            door.operateDoor()
            
        time.sleep(1)


if __name__ == "__main__":
    sys.exit(main())
