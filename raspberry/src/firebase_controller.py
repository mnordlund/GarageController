import firebase_admin
import json
from firebase_admin import credentials
from firebase_admin import db
import logging
import sys

log = logging.getLogger("gc.fbc")
commands_ref: db.Reference


def init(firebaseconfig: str) -> bool:
    global commands_ref
    log.debug("Initializing firebase")
    try:
        file = open(firebaseconfig)
        cfg = json.load(file)
    except:
        log.critical("Unable to read firebase config file:", firebaseconfig)
        sys.exit(0)

    cred = credentials.Certificate(cfg["credentials"])
    try:
        firebase_admin.initialize_app(cred, {'databaseURL':cfg["database"]})
        commands_ref = db.reference('/commands')
    except:
        log.warning("Failed to connect to firebase")
        return False
    return True

def isOperateCommand() -> bool:
    try:
        cmds = commands_ref.get()
    except:
        log.error("Failed to read commands from firebase")
    if(cmds['operate']):
        cmds['operate'] = False
        commands_ref.update(cmds)
        return True

    return False
