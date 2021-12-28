import firebase_admin
import json
from firebase_admin import credentials
from firebase_admin import db
import logging
import sys

log = logging.getLogger("gc.fbc")
app: firebase_admin.App


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

