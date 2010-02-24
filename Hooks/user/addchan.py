# This file is part of Merlin.
# Merlin is the Copyright (C)2008,2009,2010 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.

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

class addchan(loadable):
    """Adds a channel with the given level with maxlevel equal to your own access level"""
    usage = " <chan> <level>"
    
    @route(r"(#\S+)\s+(\S+)", access = "admin")
    @require_user
    def execute(self, message, user, params):
        
        chan = params.group(1)
        access = params.group(2)
        if not access.isdigit():
            try:
                access = Config.getint("Access",access)
            except Exception:
                message.reply("Invalid access level '%s'" % (access,))
                return
        else:
            access = int(access)
        
        if access > user.access:
            message.reply("You may not add a user with higher access to your own")
            return
        
        try:
            session.add(Channel(name=chan, userlevel=access, maxlevel=user.access))
            session.commit()
            message.reply("Added chan %s at level %s" % (chan,access,))
            message.privmsg("set %s autoinvite on" %(chan,),'P');
            message.privmsg("invite %s" %(chan,),'P');
        except IntegrityError:
            session.rollback()
            message.reply("Channel %s already exists" % (chan,))
