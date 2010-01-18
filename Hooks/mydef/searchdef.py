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
from Core.config import Config
from Core.db import session
from Core.maps import Updates, User, Ship, UserFleet
from Core.loadable import loadable

@loadable.module("member")
class searchdef(loadable):
    """"""
    usage = " <number> <ship>"
    paramre = re.compile(r"\s+(\d+(?:\.\d+)?[mk]?)\s+(\S+)")
    
    def execute(self, message, user, params):
        
        count = self.short2num(params.group(1))
        name = params.group(2)

        ship = Ship.load(name=name)
        if ship is None:
            message.alert("No Ship called: %s" % (name,))
            return
        
        Q = session.query(User, UserFleet)
        Q = Q.join(User.fleets)
        Q = Q.filter(User.active == True)
        Q = Q.filter(User.access >= Config.getint("Access", "member"))
        Q = Q.filter(UserFleet.ship == ship)
        Q = Q.filter(UserFleet.ship_count >= count)
        Q = Q.filter(User.fleetcount > 0)
        Q = Q.order_by(desc(UserFleet.ship_count))
        result = Q.all()
        
        if len(result) < 1:
            message.reply("There are no planets with free fleets and at least %s ships matching '%s'"%(self.num2short(count),ship.name))
            return
        
        tick = Updates.current_tick()
        reply = "Fleets matching query: "
        reply+= ", ".join(map(lambda (u, x): "%s(%s) %s: %s %s"%(u.name,u.fleetupdated-tick,u.fleetcount,self.num2short(x.ship_count),ship.name),result))
        message.reply(reply)
