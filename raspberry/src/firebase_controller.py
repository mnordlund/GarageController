import firebase_admin
import json
from firebase_admin import credentials
from firebase_admin import db
import logging
import sys

import doorHandler as door

log = logging.getLogger("gc.fbc")
app: firebase_admin.App

status: dict = {'locked': False, 'doorClosed': False, 'doorOpened': False, 'carInGarage': False}

listeners = []


def init(firebaseconfig: str) -> bool:
    global commands_ref
    global app

    log.debug("Initializing firebase")
    try:
        file = open(firebaseconfig)
        cfg = json.load(file)
    except:
        log.critical("Unable to read firebase config file:", firebaseconfig)
        return False

    try:
        cred = credentials.Certificate(cfg["credentials"])
        app = firebase_admin.initialize_app(cred, {'databaseURL':cfg["database"]})
    except:
        log.critical("Failed to initialize firebase")
        return False

    return True

def cleanup():
    log.info("Cleaning up firebase connections")
    for listener in listeners:
        listener.close()


def writeStatus():
    try:
        ref = db.reference('/status')
        ref.update(status)
    except:
        log.error("Failed to update status to database")

def isConnected() -> bool:
    try:
        ref = db.reference('/')
        ref.get(shallow=True)
        log.debug("Database connected")
        return True
    except:
        log.debug("Database not connected")
        return False

def isOperateCommand() -> bool:
    try:
        ref = db.reference('/commands')
        cmds = ref.get()
        if(cmds['operate']):
            cmds['operate'] = False
            ref.update(cmds)
            return True
    except:
        log.error("Failed to read commands from firebase")
    
    return False

def isLocked() -> bool:
    try:
        ref = db.reference('/commands')
        lock = ref.child('lock').get()
        if(lock):
            ref.child('operate').set(False)
        return lock
    except:
        log.error("Failed to read lock")
        return True

def lockCallback(event: db.Event):
    if(event.data != status['locked']):
        status['locked'] = event.data
        log.info("Locked: " + str(status['locked']))
        db.reference('/commands/operate').set(False)
        writeStatus()

def operateCallback(event: db.Event):
    if(event.data == True and not status['locked']):
        door.operateDoor()
        db.reference('/commands/operate').set(False)

def setupCallbacks():
    lockref = db.reference('/commands/lock')
    listeners.append(lockref.listen(lockCallback))
    operateref = db.reference('/commands/operate')
    operateref.listen(operateCallback)