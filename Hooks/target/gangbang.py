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
 
from sqlalchemy.sql import asc
from Core.paconf import PA
from Core.db import session
from Core.maps import Updates, Planet, Alliance, User, Intel, Target
from Core.loadable import loadable, route

class gangbang(loadable):
    """List of booked targets in an alliance"""
    usage = " <alliance> [tick]"
    
    @route(r"(\S+)(?:\s+(\d+))?", access = "half")
    def execute(self, message, user, params):
        
        alliance = Alliance(name="Unknown") if params.group(1).lower() == "unknown" else Alliance.load(params.group(1))
        if alliance is None:
            message.reply("No alliance matching '%s' found"%(params.group(1),))
            return
        
        tick = Updates.current_tick()
        
        when = int(params.group(2) or 0)
        if when and when < PA.getint("numbers", "protection"):
            when += tick
        elif when and when <= tick:
            message.alert("Can not check status on the past. You wanted tick %s, but current tick is %s." % (when, tick,))
            return
        
        Q = session.query(Planet, User.name, Target.tick)
        Q = Q.join(Target.planet)
        Q = Q.join(Planet.intel) if alliance.id else Q.outerjoin(Planet.intel)
        Q = Q.join(Target.user)
        Q = Q.filter(Planet.active == True)
        Q = Q.filter(Intel.alliance == (alliance if alliance.id else None))
        Q = Q.filter(Target.tick == when) if when else Q.filter(Target.tick > tick)
        Q = Q.order_by(asc(Planet.x))
        Q = Q.order_by(asc(Planet.y))
        Q = Q.order_by(asc(Planet.z))
        result = Q.all()
        
        if len(result) < 1:
            reply="No active bookings matching alliance %s" %(alliance.name)
            if when:
                reply+=" for tick %s."%(when,)
            message.reply(reply)
            return
        
        reply="Target information for %s"%(alliance.name)
        reply+=" landing on tick %s (eta %s): "%(when,when-tick) if when else ": "
        
        ticks={}
        for planet, user, land in result:
            if not ticks.has_key(land):
                ticks[land]=[]
            ticks[land].append((planet, user,))
        sorted_keys=ticks.keys()
        sorted_keys.sort()
        
        replies = []
        for land in sorted_keys:
            prev=[]
            for planet, user in ticks[land]:
                prev.append("(%s:%s:%s %s)" % (planet.x,planet.y,planet.z,user))
            replies.append("Tick %s (eta %s) "%(land,land-tick) +", ".join(prev))
        replies[0] = reply + replies[0]
        
        message.reply("\n".join(replies))
