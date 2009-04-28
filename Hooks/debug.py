# This module adds debug functionality

# This file is part of Merlin.
 
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
 
# This work is Copyright (C)2008 of Robin K. Hansen, Elliot Rosemarine.
# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

import traceback
from .Core.exceptions_ import PNickParseError
from .Core.callbacks import callbacks as cb
from .Core.modules import M
callback = M.loadable.callback

@callback('PRIVMSG', admin=True)
def raw(message):
    """Send a raw message to the server."""
    message.write(msg[5:])

@callback('PRIVMSG', admin=True)
def debug(message):
    """Execute a statement. Warning: Playing with this is risky!"""
    try:
        exec(message.get_msg()[7:])
    except:
        message.alert(traceback.format_exc())

@callback('PRIVMSG', admin=True)
def viewlog(message):
    """Sends the error log to an admin."""
    message.reply(open("errorlog.txt","r").read()+"\nDone")

@callback('PRIVMSG', admin=True)
def clearlog(message):
    """Sends the error log to an admin."""
    open("errorlog.txt","w").close()
    message.reply("Done")
