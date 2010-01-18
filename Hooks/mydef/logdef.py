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
from sqlalchemy.sql import desc
from Core.db import session
from Core.maps import Updates, User, Ship, FleetLog
from Core.loadable import loadable

@loadable.module("member")
class logdef(loadable):
    """"""
    usage = ""
    paramre=re.compile(r"\s*(\S*)")
    
    def execute(self, message, user, params):
        
        search=params.group(1)
        
        Q = session.query(FleetLog)
        
        if search != "":
            ship = Ship.load(name=search)
            if ship is not None:
                Q = Q.filter(FleetLog.ship == ship)
            else:
                u = User.load(search, exact=False, access="member")
                if u is not None:
                    Q = Q.filter(FleetLog.user == u)
                else:
                    Q = Q.filter(FleetLog.id == -1)
        Q = Q.order_by(desc(FleetLog.tick))
        
        result = Q[:10]
        
        if len(result) < 1:
            message.reply("No matches found in the deflog for search '%s'"%(search,))
            return
        
        tick = Updates.current_tick()
        reply = ", ".join(map(lambda x:"%s gave %s %s to %s (%s)"%(x.user.name,self.num2short(x.ship_count),x.ship.name,x.taker.name,x.tick-tick),result))
        message.reply(reply)
