# Relay a message

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
from .variables import channels, access
from .Core.modules import M
loadable = M.loadable.loadable

class relay(loadable):
    """Relays a message"""
    
    def __init__(self):
        loadable.__init__(self)
        self.robore = re.compile(r"\s(\S+?)\s(.+)")
        self.usage += " message"
    
    @loadable.run_with_access(access['admin'])
    def execute(self, message, user, params):
        self.relay(message, message.get_nick(), params.group(1))
    
    def robocop(self, message):
        params = loadable.robocop(self, message)
        if not params:
            return
        self.relay(message, params.group(1), params.group(2))
    
    def relay(self, message, nick, msg):
        message.privmsg(r"04,01 %s Reports: 08,01%s " % (nick, msg.replace("\t"," "),), channels['off'])

callbacks = [("PRIVMSG", relay())]