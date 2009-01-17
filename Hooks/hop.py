# This module is used to restart the bot

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

from .variables import nick, admins
from .Core.exceptions_ import RebootConnection, PNickParseError

def hop(message):
    """Get the bot to quit and reconnect"""
    
    if message.get_msg() == "!hop":
        try:
            if message.get_pnick() in admins:
                dohop()
            else:
                message.alert("You don't have access for that.")
        except PNickParseError:
            message.alert("You don't have access for that.")

def dohop():
    # This is a separate function for legacy reasons
    raise RebootConnection

callbacks = [("PRIVMSG", hop)]