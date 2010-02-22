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
 
from sqlalchemy.exc import IntegrityError
from Core.config import Config
from Core.db import session
from Core.maps import Channel
from Core.loadable import loadable, route, require_user

class remchan(loadable):
    usage = " <chan>"
    
    @route(r"\s+(#\S+)", access = "member")
    @require_user
    def execute(self, message, user, params):
        
        channel = params.group(1)
        chan = Channel.load(channel)
        if chan is None:
            message.reply("Channel '%s' does not exist" % (channel,))
            if user.is_admin():
                message.privmsg("remuser %s %s" %(channel, Config.get('Connection', 'nick')),'P')
                message.part(channel)
            return
        
        if chan.userlevel >= user.access:
            message.reply("You may not remove %s, the channel's access (%s) exceeds your own (%s)" % (chan.name, chan.userlevel, user.access,))
            return
        
        session.delete(chan)
        session.commit()
        
        message.privmsg("remuser %s %s" %(chan.name, Config.get('Connection', 'nick')),'P')
        message.part(chan.name)
        message.reply("Removed channel %s" % (chan.name,))
