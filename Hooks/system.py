# This file is part of Merlin.
# Merlin is the Copyright (C)2008-2009 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.

# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
 
# This module provides an entry point for system reboots or reloads

from traceback import format_exc
from merlin import Merlin
from Core.exceptions_ import Quit, Reboot, Reload
from Core.config import Config
from Core.chanusertracker import CUT
from Core.callbacks import Callbacks
from Core.loadable import loadable

@loadable.system('PRIVMSG', admin=True)
def quit(message):
    """Quit IRC and close down"""
    msg = message.get_msg().split(None,1)
    if len(msg) > 1:
        raise Quit(msg[1])
    else:
        raise Quit

@loadable.system('PRIVMSG', admin=True)
def reboot(message):
    """Quit IRC reboot, reload and reconnect"""
    msg = message.get_msg().split(None,1)
    if len(msg) > 1:
        raise Reboot(msg[1])
    else:
        raise Reboot

@loadable.system('PRIVMSG', admin=True)
def reload(message):
    """Dynamically reload the Core and Hooks"""
    msg = message.get_msg().split(None,1)
    if len(msg) > 1:
        raise Reload(msg[1])
    else:
        raise Reload

@loadable.system('PRIVMSG', admin=True)
def raw(message):
    """Send a raw message to the server."""
    msg = message.get_msg().split(None,1)
    if len(msg) > 1:
        message.write(msg[1])

@loadable.system('PRIVMSG', admin=True)
def debug(message):
    """Execute a statement. Warning: Playing with this is risky!"""
    msg = message.get_msg().split(None,1)
    if len(msg) > 1:
        try:
            exec(msg[1])
        except Exception:
            message.alert(format_exc())
