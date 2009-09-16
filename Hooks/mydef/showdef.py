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
 
import re
from Core.db import session
from Core.maps import Updates, User
from Core.loadable import loadable

@loadable.module(100)
class showdef(loadable):
    """"""
    usage = " <pnick>"
    paramre = re.compile(r"(?:\s+(\S+))?")
    
    @loadable.require_user
    def execute(self, message, user, params):
        
        name=params.group(1)
        if name is not None:
            u = User.load(name=name,exact=False)
        else:
            u = user
        if u is None or not u.is_member():
            message.reply("No members matching %s found"%(name,))
            return
        
        ships = u.fleets.all()
        
        if len(ships) < 1:
            message.reply("%s is either a lazy pile of shit that hasn't entered any ships for def, or a popular whore who's already turned their tricks."%(u.name,))
            return
        
        tick = Updates.current_tick()
        reply ="%s def info: fleetcount %s, updated: %s (%s), ships: " %(u.name,u.fleetcount,u.fleetupdated,u.fleetupdated-tick)
        reply+= ", ".join(map(lambda x:"%s %s" %(self.num2short(x.ship_count),x.ship),ships))
        reply+=" comment: %s"%(u.fleetcomment,)
        message.reply(reply)
