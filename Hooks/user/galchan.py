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

class galchan(loadable):
    """Adds a channel where the access of commands is limited to 1 in that channel (so you don't accidentally do !intel or something 'important')"""
    usage = " <chan>"
    
    @route(r"(#\S+)", access = "member")
    @require_user
    def execute(self, message, user, params):
        
        chan = params.group(1)
        if "galmate" in Config.options("Access"):
            access = Config.getint("Access","galmate")
        else:
            access = 0
        
        try:
            session.add(Channel(name=chan, userlevel=access, maxlevel=access))
            session.commit()
            message.reply("Added your galchannel as %s (if you didn't add me to the channel with at least access 24 first, I'm never going to bother joining)" % (chan,))
            message.privmsg("set %s autoinvite on" %(chan,),'P');
            message.privmsg("invite %s" %(chan,),'P');
        except IntegrityError:
            session.rollback()
            message.reply("Channel %s already exists" % (chan,))
