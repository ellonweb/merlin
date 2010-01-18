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
from sqlalchemy.sql import asc
from Core.exceptions_ import PNickParseError
from Core.db import session
from Core.maps import Updates, Galaxy, Planet, Alliance, User, Intel, Target
from Core.loadable import loadable

@loadable.module("half")
class status(loadable):
    """List of targets booked by user, or list of bookings for a given galaxy or planet"""
    usage = " [user|x:y[:z]|alliance] [tick]"
    paramre = (re.compile(loadable.coordre.pattern+r"(?:\s(\d+))?"), re.compile(r"(?:\s(\S+))?(?:\s(\d+))?"),)
    
    def execute(self, message, user, params):
        
        tick = Updates.current_tick()
        
        # Planet or Galaxy
        if len(params.groups()) == 6:
            when = int(params.group(6) or 0)
            if when and when < 32:
                when += tick
            elif when and when <= tick:
                message.alert("Can not check status on the past. You wanted tick %s, but current tick is %s." % (when, tick,))
                return
            
            # Planet
            if params.group(5) is not None:
                planet = Planet.load(*params.group(1,3,5))
                if planet is None:
                    message.alert("No planet with coords %s:%s:%s" % params.group(1,3,5))
                    return
                
                Q = session.query(User.name, Target.tick)
                Q = Q.join(Target.user)
                Q = Q.filter(Target.planet == planet)
                Q = Q.filter(Target.tick == when) if when else Q.filter(Target.tick > tick)
                Q = Q.order_by(asc(Target.tick))
                result = Q.all()
                
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
                        prev.append("(%s user:%s)" % (land,user))
                    reply+=", ".join(prev)
                message.reply(reply)
                return
            
            # Galaxy
            else:
                galaxy = Galaxy.load(*params.group(1,3))
                if galaxy is None:
                    message.alert("No galaxy with coords %s:%s" % params.group(1,3))
                    return
                
                Q = session.query(Planet.z, User.name, Target.tick)
                Q = Q.join(Target.planet)
                Q = Q.join(Target.user)
                Q = Q.filter(Planet.active == True)
                Q = Q.filter(Planet.galaxy == galaxy)
                Q = Q.filter(Target.tick == when) if when else Q.filter(Target.tick > tick)
                Q = Q.order_by(asc(Planet.z))
                result = Q.all()
                
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
            
            if params.group(1) is None and not self.is_user(user):
                raise PNickParseError
            booker = User.load(params.group(1), exact=False) if params.group(1) is not None else user
            alliance = (Alliance(name="Unknown") if params.group(1).lower() == "unknown" else Alliance.load(params.group(1))) if booker is None else None
            if (booker or alliance) is None:
                message.reply("No alliance or user matching '%s' found" % (params.group(1),))
                return
            
            # User
            if booker is not None:
                Q = session.query(Planet, Target.tick)
                Q = Q.join(Target.planet)
                Q = Q.join(Target.user)
                Q = Q.filter(Planet.active == True)
                Q = Q.filter(Target.user == booker)
                Q = Q.filter(Target.tick == when) if when else Q.filter(Target.tick > tick)
                Q = Q.order_by(asc(Target.tick))
                Q = Q.order_by(asc(Planet.x))
                Q = Q.order_by(asc(Planet.y))
                Q = Q.order_by(asc(Planet.z))
                result = Q.all()
                
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
                    prev.append("(%s:%s:%s%s)" % (planet.x, planet.y, planet.z, "" if when else " landing pt%s/eta %s" % (land,land-tick,),))
                reply+=", ".join(prev)
                message.reply(reply)
                return
            
            # Alliance
            else:
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
                return
