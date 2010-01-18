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
from Core.db import session
from Core.maps import Updates, Planet, User, Target
from Core.loadable import loadable

@loadable.module("half")
class unbook(loadable):
    """"""
    usage = " x:y:z [eta|landing tick]"
    paramre = re.compile(loadable.planet_coordre.pattern+r"(?:\s(\d+))?(?:\s(yes))?")
    
    @loadable.require_user
    def execute(self, message, user, params):
        planet = Planet.load(*params.group(1,3,5))
        if planet is None:
            message.alert("No planet with coords %s:%s:%s" % params.group(1,3,5))
            return
        
        tick = Updates.current_tick()
        when = int(params.group(6) or 0)
        if 0 < when < 32:
            eta = when
            when += tick
        elif 0 < when <= tick:
            message.alert("Can not unbook targets in the past. You wanted tick %s, but current tick is %s." % (when, tick,))
            return
        else:
            eta = when - tick
        if when > 32767:
            when = 32767 
        
        override = params.group(7)
        
        Q = session.query(Target)
        Q = Q.join(Target.user)
        Q = Q.filter(Target.planet == planet)
        Q = Q.filter(Target.user == user) if override is None else Q
        Q = Q.filter(Target.tick == when) if when else Q.filter(Target.tick >= tick)
        Q = Q.order_by(asc(Target.tick))
        result = Q.all()
        for target in result:
            session.delete(target)
        count = len(result)
        session.commit()
        
        if count < 1:
            reply=("You have no " if override is None else "No ") +"bookings matching %s:%s:%s"%(planet.x,planet.y,planet.z,)
            if when:
                reply+=" for landing on tick %s"%(when,)
            reply+=". If you are trying to unbook someone else's target, you must confirm with 'yes'." if override is None else ""
        else:
            reply="You have unbooked %s:%s:%s"%(planet.x,planet.y,planet.z,)
            if when:
                reply+=" for landing pt %s"%(when,)
                if override:
                    reply+=" (previously held by user %s)"%(result[0].user.name)
            else:
                reply+=" for %d booking(s)"%(count,)
                if override:
                    prev=[]
                    for target in result:
                        prev.append("(%s user:%s)" % (target.tick,target.user.name))
                    reply+=": "+", ".join(prev)
                        
            reply+="."
        message.reply(reply)
        return
