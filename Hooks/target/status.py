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
from .variables import access
from .Core.modules import M
loadable = M.loadable.loadable

class status(loadable):
    """List of targets booked by user, or list of bookings for a given galaxy or planet"""
    
    def __init__(self):
        loadable.__init__(self)
        self.paramre = (re.compile(r"status(?:\s([\w-]+)(?:\s(\d+))?)?"), re.compile(self.coordre.pattern+r"(?:\s(\d+))?"),)
        self.usage += " [user|x:y[:z]|alliance] [tick]"
    
    @loadable.run_with_access(access.get('hc',0) | access.get('bc',0) | access['member'])
    def execute(self, message, user, params):
        
        tick = M.DB.Maps.Updates.current_tick()
        
        # Planet or Galaxy
        if params.group(1) is not None and params.group(1).isdigit():
            when = int(params.group(4) or 0)
            if when and when < 80:
                when += tick
            elif when and when <= tick:
                message.alert("Can not check status on the past. You wanted tick %s, but current tick is %s." % (when, tick,))
                return
            
            # Planet
            if params.group(3) is not None:
                planet = M.DB.Maps.Planet.load(*params.group(1,2,3))
                if planet is None:
                    message.alert("No planet with coords %s:%s:%s" % params.group(1,2,3))
                    return
                
                session = M.DB.Session()
                Q = session.query(M.DB.Maps.User.name, M.DB.Maps.Target.tick)
                Q = Q.join(M.DB.Maps.Target.user)
                Q = Q.filter(M.DB.Maps.Target.planet_id == planet.id)
                Q = Q.filter(M.DB.Maps.Target.tick == when) if when else Q.filter(M.DB.Maps.Target.tick > tick)
                Q = Q.order_by(M.DB.SQL.asc(M.DB.Maps.Target.tick))
                result = Q.all()
                session.close()
                
                if len(result) < 1:
                    reply="No bookings matching planet %s:%s:%s" % (planet.x, planet.y, planet.z,)
                    if when:
                        reply+=" for tick %s"%(when,)
                    message.reply(reply)
                    return
                
                reply="Status for %s:%s:%s - " % (planet.x, planet.y, planet.z,)
                if when:
                    user, land = result[0]
                    reply+="booked for landing pt %s (eta %s) by %s"%(land,land-tick,user)
                else:
                    prev=[]
                    for user, land in result:
                        prev.append("(%s user:%s)" % (land,owner))
                    reply+=", ".join(prev)
                message.reply(reply)
                return
            
            # Galaxy
            else:
                galaxy = M.DB.Maps.Galaxy.load(*params.group(1,2))
                if planet is None:
                    message.alert("No galaxy with coords %s:%s" % params.group(1,2))
                    return
                
                session = M.DB.Session()
                Q = session.query(M.DB.Maps.Planet.z, M.DB.Maps.User.name, M.DB.Maps.Target.tick)
                Q = Q.join(M.DB.Maps.Target.planet)
                Q = Q.join(M.DB.Maps.Target.user)
                Q = Q.filter(M.DB.Maps.Planet.x == galaxy.x)
                Q = Q.filter(M.DB.Maps.Planet.y == galaxy.y)
                Q = Q.filter(M.DB.Maps.Target.tick == when) if when else Q.filter(M.DB.Maps.Target.tick > tick)
                Q = Q.order_by(M.DB.SQL.asc(M.DB.Maps.Planet.z))
                result = Q.all()
                session.close()
                
                if len(result) < 1:
                    reply="No bookings matching galaxy %s:%s" % (galaxy.x, galaxy.y,)
                    if when:
                        reply+=" for tick %s"%(when,)
                    message.reply(reply)
                    return
                
                reply="Target information for %s:%s" % (galaxy.x, galaxy.y,)
                reply+=" landing on tick %s (eta %s): "%(when,when-tick) if when else ": "
                
                ticks={}
                for z, user, land in result:
                    if not ticks.has_key(land):
                        ticks[land]=[]
                    ticks[land].append((z, user,))
                sorted_keys=ticks.keys()
                sorted_keys.sort()
                
                replies = []
                for land in sorted_keys:
                    prev=[]
                    for z, user in ticks[land]:
                        prev.append("(%s user:%s)" % (z,user))
                    replies.append("Tick %s (eta %s) "%(land,land-tick) +", ".join(prev))
                replies[0] = reply + replies[0]
                
                message.reply("\n".join(replies))
                return
        
        # User or Alliance
        else:
            when = int(params.group(2) or 0)
            if when and when < 80:
                when += tick
            elif when and when <= tick:
                message.alert("Can not check status on the past. You wanted tick %s, but current tick is %s." % (when, tick,))
                return
            
            booker = M.DB.Maps.User.load(params.group(1)) if params.group(1) is not None else user
            alliance = (M.DB.Maps.Alliance(name="Unknown") if params.group(1).lower() == "unknown" else M.DB.Maps.Alliance.load(params.group(1))) if booker is None else None
            if (booker or alliance) is None:
                message.reply("No alliance or user matching '%s' found" % (param,.group(1),))
                return
            
            # User
            if booker is not None:
                session = M.DB.Session()
                Q = session.query(M.DB.Maps.Planet, M.DB.Maps.Target.tick)
                Q = Q.join(M.DB.Maps.Target.planet)
                Q = Q.join(M.DB.Maps.Target.user)
                Q = Q.filter(M.DB.Maps.Target.user_id == booker.id)
                Q = Q.filter(M.DB.Maps.Target.tick == when) if when else Q.filter(M.DB.Maps.Target.tick > tick)
                Q = Q.order_by(M.DB.SQL.asc(M.DB.Maps.Target.tick))
                Q = Q.order_by(M.DB.SQL.asc(M.DB.Maps.Planet.x))
                Q = Q.order_by(M.DB.SQL.asc(M.DB.Maps.Planet.y))
                Q = Q.order_by(M.DB.SQL.asc(M.DB.Maps.Planet.z))
                result = Q.all()
                session.close()
                
                if len(result) < 1:
                    reply="No bookings matching user %s" % (booker.name,)
                    if when:
                        reply+=" for tick %s"%(when,)
                    message.reply(reply)
                    return
                
                reply="Bookings matching user %s" % (booker.name,)
                reply+=" landing on tick %s (eta %s): "%(when,when-tick) if when else ": "
                
                prev=[]
                for planet, land in result:
                    prev.append("(%s:%s:%s%s)" % (planet.x, planet.y, planet.z, "" if when else " landing pt%s/eta %s" % (when,when-tick,),))
                reply+=", ".join(prev)
                message.reply(reply)
                return
            
            # Alliance
            else:
                session = M.DB.Session()
                Q = session.query(M.DB.Maps.Planet, M.DB.Maps.User.name, M.DB.Maps.Target.tick)
                Q = Q.join(M.DB.Maps.Target.planet)
                Q = Q.join(M.DB.Maps.Planet.intel) if alliance.id else Q.outerjoin(M.DB.Maps.Planet.intel)
                Q = Q.join(M.DB.Maps.Target.user)
                Q = Q.filter(M.DB.Maps.Intel.alliance_id == alliance.id)
                Q = Q.filter(M.DB.Maps.Target.tick == when) if when else Q.filter(M.DB.Maps.Target.tick > tick)
                Q = Q.order_by(M.DB.SQL.asc(M.DB.Maps.Planet.x))
                Q = Q.order_by(M.DB.SQL.asc(M.DB.Maps.Planet.y))
                Q = Q.order_by(M.DB.SQL.asc(M.DB.Maps.Planet.z))
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
                        prev.append("(%s:%s:%s %s)" % (planet.x,planet.y,planet.z,user))
                    replies.append("Tick %s (eta %s) "%(land,land-tick) +", ".join(prev))
                replies[0] = reply + replies[0]
                
                message.reply("\n".join(replies))
                return
