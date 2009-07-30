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

from Core.exceptions_ import PNickParseError, UserError
from Core.config import Config
from Core.loadable import loadable
from Core.callbacks import Callbacks

class help(loadable):
    """Help"""
    
    def __init__(self):
        loadable.__init__(self)
        self.paramre = self.commandre
        self.usage += " [command]"
    
    @loadable.run
    def execute(self, message, user, params):
        
        if len(message.get_msg().split()) == 1:
            commands = []
            message.reply(self.helptext+". For more information use: "+self.usage)
            for callback in Callbacks.callbacks:
                try:
                    if hasattr(callback, "has_access"):
                        if callback.has_access(message):
                            commands.append(callback.__class__.__name__)
                    else:
                        if message.get_pnick() == Config.get("Auth", "admin"):
                            commands.append(callback.__name__)
                except PNickParseError:
                    continue
                except UserError:
                    continue
            message.reply("Loaded commands: " + ", ".join(commands))
        else:
            for callback in Callbacks.callbacks:
                try:
                    if hasattr(callback, "help"):
                        continue
                    else:
                        if (message.get_pnick() == Config.get("Auth", "admin")) and (message.get_msg().split()[1] == callback.__name__):
                            message.reply(callback.__doc__)
                except PNickParseError:
                    continue
