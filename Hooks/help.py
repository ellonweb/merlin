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

import re
from Core.exceptions_ import PNickParseError, UserError
from Core.maps import Channel
from Core.loadable import loadable
from Core.callbacks import Callbacks

@loadable.module()
class help(loadable):
    """Help"""
    usage = " [command]"
    paramre = re.compile(r"\s*(\S*)")
    
    def execute(self, message, user, params):
        if params.group(1) is not "":
            return
        commands = []
        message.reply(self.doc+". For more information use: "+self.usage)
        if message.in_chan():
            channel = Channel.load(message.get_chan())
        else:
            channel = None
        for callback in Callbacks.callbacks["PRIVMSG"]:
            try:
                if callback.check_access(message, user, channel) is not None:
                    commands.append(callback.name)
            except PNickParseError:
                continue
            except UserError:
                continue
        message.reply("Loaded commands: " + ", ".join(commands))
