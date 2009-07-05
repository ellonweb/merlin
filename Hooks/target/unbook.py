# UnBook

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
from .variables import alliance, access
from .Core.modules import M
loadable = M.loadable.loadable

class unbook(loadable):
    """"""
    
    def __init__(self):
        loadable.__init__(self)
        self.paramre = re.compile(self.planet_coordre.pattern+r"(?:\s(\d+))?(?:\s(yes))?")
        self.usage += " x:y:z (eta|landing tick)"
    
    @loadable.run_with_access(access.get('bc',0) | access['member'])
    def execute(self, message, user, params):
        planet = M.DB.Maps.Planet.load(*params.group(1,2,3))
        if planet is None:
            message.alert("No planet with coords %s:%s:%s" % params.group(1,2,3))
            return
        
        tick = M.DB.Maps.Updates.current_tick()
        when = int(params.group(4) or 0)
        if 0 < when < 80:
            eta = when
            when += tick
        elif when <= tick:
            message.alert("Can not unbook targets in the past. You wanted tick %s, but current tick is %s." % (when, tick,))
            return
        else:
            eta = when - tick
        if when > 32767:
            when = 32767 
        
        override = params.group(5)
        
        session = M.DB.Session()
        
        Q = session.query(M.DB.Maps.User.name, M.DB.Maps.Target.tick)
        Q = Q.join(M.DB.Maps.Target.user)
        Q = Q.filter(M.DB.Maps.Target.planet == planet)
        Q = Q.filter(M.DB.Maps.User == user) if override is None else Q
        Q = Q.filter(M.DB.Maps.Target.tick == when) if when else Q.filter(M.DB.Maps.Target.tick >= tick)
        Q = Q.order_by(M.DB.SQL.asc(M.DB.Maps.Target.tick))
        result = Q.all() if override else None
        count = Q.delete(synchronize_session=False)
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
                    reply+=" (previously held by user %s)"%(result[0][0])
            else:
                reply+=" for %d booking(s)"%(count,)
                if override:
                    reply+=": "
                    prev=[]
                    for booker, land in result:
                        prev.append("(%s user:%s)" % (land,booker))
                    reply+=": "+", ".join(prev)
                        
            reply+="."
        message.reply(reply)
        return
