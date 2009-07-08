# Book

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

class book(loadable):
    """Book a target for attack. You should always book your targets, so someone doesn't inadvertedly piggy your attack."""
    
    def __init__(self):
        loadable.__init__(self)
        self.paramre = re.compile(self.planet_coordre.pattern+r"\s(\d+)(?:\s(yes))?")
        self.usage += " x:y:z (eta|landing tick)"
    
    @loadable.run_with_access(access['member'])
    def execute(self, message, user, params):
        planet = M.DB.Maps.Planet.load(*params.group(1,2,3))
        if planet is None:
            message.alert("No planet with coords %s:%s:%s" % params.group(1,2,3))
            return
        
        tick = M.DB.Maps.Updates.current_tick()
        when = int(params.group(4))
        if when < 80:
            eta = when
            when += tick
        elif when <= tick:
            message.alert("Can not book targets in the past. You wanted tick %s, but current tick is %s." % (when, tick,))
            return
        else:
            eta = when - tick
        if when > 32767:
            when = 32767        
        
        session = M.DB.Session()
        session.add(planet)
        
        if planet.intel and planet.intel.alliance and (planet.alliance.name == alliance):
            message.reply("%s:%s:%s is %s in %s. Quick, launch before they notice the highlight." % (planet.x,planet.y,planet.z, planet.intel.nick or 'someone', alliance,))
            session.close()
            return
        
        Q = session.query(M.DB.Maps.User.name, M.DB.Maps.Target.tick)
        Q = Q.join(M.DB.Maps.Target.user)
        Q = Q.filter(M.DB.Maps.Target.planet == planet)
        Q = Q.filter(M.DB.Maps.Target.tick >= when)
        Q = Q.order_by(M.DB.SQL.asc(M.DB.Maps.Target.tick))
        result = Q.all()
        
        if len(result) >= 1:
            booker, land = result[0]
            if land == when:
                message.reply("Target %s:%s:%s is already booked for landing tick %s by user %s" % (planet.x,planet.y,planet.z, land, booker,))
                session.close()
                return
            
            if params.group(5) is None:
                reply="There are already bookings for that target after landing pt %s (eta %s). To see status on this target, do !status %s:%s:%s." % (when,eta, planet.x,planet.y,planet.z,)
                reply+=" To force booking at your desired eta/landing tick, use !book %s:%s:%s %s yes (Bookers: " %(planet.x,planet.y,planet.z, when,)
                prev=[]
                for booker, land in result:
                    prev.append("(%s user:%s)" % (land, booker,))
                reply += ", ".join(prev) + ")"
                message.reply(reply)
                return
        
        try:
            planet.bookings.append(M.DB.Maps.Target(user=user, tick=when)
            session.commit()
            message.reply("Booked landing on %s:%s:%s tick %s for user %s" % (planet.x,planet.y,planet.z, when, user.name,))
            return
        except M.DB.sqlalchemy.exceptions.IntegrityError:
            session.rollback()
            raise Exception("Integrity error? Unable to booking for pid %s and tick %s"%(planet.id, when,))
            return
