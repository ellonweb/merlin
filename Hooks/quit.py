# This module provides a means of quitting the bot sanely

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

import sys
from .variables import admins
from .Core.exceptions_ import PNickParseError
from .Core.modules import M
callback = M.loadable.callback

@callback('PRIVMSG')
def quit(message):
    """Does exactly what one would think it does."""
    
    if message.get_msg()[:5] == "!quit":
        try:
            if message.get_pnick() in admins:
                message.quit(message.get_msg()[6:])
                sys.exit(0)
            else:
                message.alert("You don't have access for that.")
        except PNickParseError:
            message.alert("You don't have access for that.")
