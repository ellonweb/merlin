# This file is part of Merlin.

# RoBoCoP core placeholder

import socket
from .variables import robocop as addr
def push(msg):
    try:
        s=socket.socket(socket.AF_UNIX)
        s.connect((addr))
        s.send(msg+"\n")
        s.close()
    except socket.error:
        pass
