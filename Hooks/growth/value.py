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
from sqlalchemy import and_
from sqlalchemy.orm import aliased
from sqlalchemy.sql import asc
from Core.db import session
from Core.maps import Updates, Planet, PlanetHistory
from Core.loadable import loadable

@loadable.module()
class value(loadable):
    """Value of a planet over the last 15 ticks"""
    usage = " x:y:z"
    paramre = re.compile(loadable.planet_coordre.pattern+r"(?:\s(\d+))?")
    
    def execute(self, message, user, params):
        
        p = Planet.load(*params.group(1,3,5))
        if p is None:
            message.alert("No planet with coords %s:%s:%s" % params.group(1,3,5))
            return
        tick = params.group(6)
        
        p1 = aliased(PlanetHistory)
        p2 = aliased(PlanetHistory)
        Q = session.query(p1.tick, p1.value, p1.value-p2.value, p1.size, p1.size-p2.size)
        Q = Q.filter(and_(p1.id==p2.id, p1.tick-1==p2.tick))
        Q = Q.filter(p1.current==p)
        
        if tick:
            Q = Q.filter(p1.tick == tick)
            result = Q.first()
            if result is None:
                message.reply("No data for %s:%s:%s on tick %s" % (p.x,p.y,p.z,tick))
                return
            
            tick, value, vdiff, size, sdiff = result
            reply="Value on pt%s for %s:%s:%s: " % (tick,p.x,p.y,p.z)
            reply+="value: %s (%s%s)" % (value,["+",""][vdiff<0],vdiff)
            if sdiff!=0:
                reply+=" roids: %s%s" % (["+",""][sdiff<0],sdiff)
            message.reply(reply)
        else:
            tick = Updates.current_tick()
            Q = Q.filter(p1.tick > (tick-16)).order_by(asc(p1.tick))
            result = Q.all()
            if len(result) < 1:
                message.reply("No data for %s:%s:%s" % (p.x,p.y,p.z))
                return
            
            prev=[]
            for tick, value, vdiff, size, sdiff in result:
                reply="pt%s %s (%s%s)" % (tick, self.num2short(value), ["+",""][vdiff<0],self.num2short(vdiff),)
                if sdiff!=0:
                    reply+=" roids: %s%s" % (["+",""][sdiff<0],sdiff)
                prev.append(reply)
            reply="Value in the last 15 ticks on %s:%s:%s: " % (p.x,p.y,p.z)+ ' | '.join(prev)
            message.reply(reply)
