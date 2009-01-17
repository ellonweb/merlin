# Help

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

from .variables import admins, access
from .Core.exceptions_ import PNickParseError, UserError
from .Core.modules import M
loadable = M.loadable.loadable

class help(loadable):
    """Help"""
    
    def __init__(self):
        loadable.__init__(self)
        self.paramre = self.commandre
        self.usage += " [command]"
    
    def execute(self, message):
        user, params = loadable.execute(self, message) or (None,None)
        if not params:
            return
        
        if len(message.get_msg().split()) == 1:
            modules = {}
            commands = []
            message.alert(self.helptext+". For more information use: "+self.usage)
            for event, callback, module_name in message.callbackmod.callbacks:
                if event != "PRIVMSG":
                    continue
                try:
                    if hasattr(callback, "has_access"):
                        if callback.has_access(message):
                            commands.append(callback.__class__.__name__)
                    else:
                        if message.get_pnick() in admins:
                            commands.append(callback.__name__)
                except PNickParseError:
                    continue
                except UserError:
                    continue
            message.alert("Loaded commands: " + ", ".join(commands))
        else:
            for event, callback, module_name in message.callbackmod.callbacks:
                if event != "PRIVMSG":
                    continue
                try:
                    if hasattr(callback, "help"):
                        continue
                    else:
                        if (message.get_pnick() in admins) and (message.get_msg()[6:] == callback.__name__):
                            message.reply(callback.__doc__)
                except PNickParseError:
                    continue
    
callbacks = [("PRIVMSG", help())]