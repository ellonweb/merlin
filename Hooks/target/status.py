# Status

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
from .variables import nick, access
from .Core.modules import M
loadable = M.loadable.loadable

class status(loadable):
    """List of targets booked by user, or list of bookings for a given galaxy or planet"""
    
    def __init__(self):
        loadable.__init__(self)
        self.paramre = re.compile(r"status(?:\s([\w-]+|)(?:\s(\d+))?")
        self.usage += " alliance [tick]"
    
    @loadable.run_with_access(access.get('hc',0) | access.get('bc',access['member']))
    def execute(self, message, user, params):
        
        alliance = M.DB.Maps.Alliance(name="Unknown") if params.group(1).lower() == "unknown" else M.DB.Maps.Alliance.load(params.group(1))
        if alliance is None:
            message.reply("No alliance matching '%s' found"%(params.group(1),))
            return
        
        tick = M.DB.Maps.Updates.current_tick()
        
        when = int(params.group(2) or 0)
        if when and when < 80:
            when += tick
        elif when and when <= tick:
            message.alert("Can not check status on the past. You wanted tick %s, but current tick is %s." % (when, tick,))
            return
        
        session = M.DB.Session()
        Q = session.query(M.DB.Maps.Planet, M.DB.Maps.User, M.DB.Maps.Target.tick)
        Q = Q.join(M.DB.Maps.Planet.bookings_loader)
        Q = Q.join(M.DB.Maps.Planet.intel) if alliance.id else Q.outerjoin(M.DB.Maps.Planet.intel)
        Q = Q.join(M.DB.Maps.Target.user)
        Q = Q.filter(M.DB.Maps.Intel.alliance_id == alliance.id)
        Q = Q.filter(M.DB.Maps.Target.tick == when) if when else Q.filter(M.DB.Maps.Target.tick > tick)
        Q = Q.order_by(M.DB.SQL.asc(M.DB.Maps.Target.tick))
        result = Q.all()
        session.close()
        
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
                prev.append("(%s:%s:%s %s)" % (planet.x,planet.y,planet.z,user.name))
            replies.append("Tick %s (eta %s) "%(land,land-tick) +", ".join(prev))
        replies[0] = reply + replies[0]
        
        message.reply("\n".join(replies))
