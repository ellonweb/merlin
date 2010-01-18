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
from Core.maps import Updates, User, Ship, UserFleet, FleetLog
from Core.loadable import loadable

@loadable.module("member")
class usedef(loadable):
    """"""
    usage = " <pnick> <ship>"
    paramre=re.compile(r"\s+(\S+)\s+(.*)")
    
    @loadable.require_user
    def execute(self, message, user, params):
        
        name=params.group(1)
        ships=params.group(2)
        u=User.load(name, exact=False, access="member")
        if u is None:
            message.reply("No members matching %s found"%(name,))
            return
        
        if u.fleetcount == 0:
            reply = "%s's fleetcount was already 0, please ensure that they actually had a fleet free to launch."%(u.name,)
        else:
            u.fleetcount -= 1
            reply = "Removed a fleet for %s, they now have %s fleets left."%(u.name,u.fleetcount,)
        
        removed = self.drop_ships(u,user,ships)
        
        reply+= " Used the following ships: "
        reply+= ", ".join(map(lambda x:"%s %s"%(self.num2short(removed[x]),x),removed.keys()))
        message.reply(reply)
    
    def drop_ships(self,user,taker,ships):
        removed={}
        tick = Updates.current_tick()
        for name in ships.split():
            ship = Ship.load(name=name)
            if ship is None:
                continue
            for fleet in user.fleets.filter_by(ship=ship):
                removed[fleet.ship.name] = fleet.ship_count
                self.delete_ships(user,taker,fleet,tick)
        session.commit()
        return removed
    
    def delete_ships(self,user,taker,fleet,tick):
        session.delete(fleet)
        session.add(FleetLog(taker=taker, user=user, ship=fleet.ship, ship_count=fleet.ship_count, tick=tick))
