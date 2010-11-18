# This file is part of Merlin/Arthur.
# Merlin/Arthur is the Copyright (C)2009,2010 of Elliot Rosemarine.

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
 
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import asc
from Core.config import Config
from Core.paconf import PA
from Core.db import session
from Core.maps import Updates, Planet, Target, Attack
from Arthur.context import render
from Arthur.loadable import loadable, load, require_user

@load
@require_user
class book(loadable):
    access = "half"
    
    def execute(self, request, user, id, x, y, z, when):
        planet = Planet.load(x,y,z)
        if planet is None:
            return self.attack(request, user, id, "No planet with coords %s:%s:%s" %(x,y,z,))
        
        tick = Updates.current_tick()
        when = int(when)
        if when < PA.getint("numbers", "protection"):
            eta = when
            when += tick
        elif when <= tick:
            return self.attack(request, user, id, "Can not book targets in the past. You wanted tick %s, but current tick is %s." % (when, tick,))
        else:
            eta = when - tick
        if when > 32767:
            when = 32767        
        
        if planet.intel and planet.alliance and planet.alliance.name == Config.get("Alliance","name"):
            return self.attack(request, user, id, "%s:%s:%s is %s in %s. Quick, launch before they notice!" % (x,y,z, planet.intel.nick or 'someone', Config.get("Alliance","name"),))
        
        try:
            planet.bookings.append(Target(user=user, tick=when))
            session.commit()
        except IntegrityError:
            session.rollback()
            target = planet.bookings.filter(Target.tick == when).first()
            if target is not None:
                return self.attack(request, user, id, "Target %s:%s:%s is already booked for landing tick %s by user %s" % (x,y,z, when, target.user.name,))
        else:
            return self.attack(request, user, id, "Booked landing on %s:%s:%s tick %s (eta %s) for user %s" % (x,y,z, when, (when-tick), user.name,))
        
        return self.attack(request, user, id)
    
    def attack(self, request, user, id, message=None):
        attack = Attack.load(id)
        if attack and attack.active:
            from Arthur.views.attack.attack import view
            return view.execute(request, user, id, message)
        else:
            from Arthur.views.attack.attack import attack
            return attack.execute(request, user, message)

@load
@require_user
class unbook(loadable):
    access = "half"
    
    def execute(self, request, user, id, x, y, z, when):
        planet = Planet.load(x,y,z)
        if planet is None:
            return self.attack(request, user, id, "No planet with coords %s:%s:%s" %(x,y,z,))
        
        tick = Updates.current_tick()
        when = int(when or 0)
        if 0 < when < PA.getint("numbers", "protection"):
            eta = when
            when += tick
        elif 0 < when <= tick:
            return self.attack(request, user, id, "Can not unbook targets in the past. You wanted tick %s, but current tick is %s." % (when, tick,))
        else:
            eta = when - tick
        if when > 32767:
            when = 32767        
        
        Q = session.query(Target)
        Q = Q.join(Target.user)
        Q = Q.filter(Target.planet == planet)
        Q = Q.filter(Target.user == user)
        Q = Q.filter(Target.tick == when) if when else Q.filter(Target.tick >= tick)
        Q = Q.order_by(asc(Target.tick))
        result = Q.all()
        for target in result:
            session.delete(target)
        count = len(result)
        session.commit()
        
        if count < 1:
            reply="You have no bookings matching %s:%s:%s"%(planet.x,planet.y,planet.z,)
            if when:
                reply+= " for landing on tick %s"%(when,)
        else:
            reply = "You have unbooked %s:%s:%s"%(planet.x,planet.y,planet.z,)
            if when:
                reply+=" for landing pt %s"%(when,)
            else:
                reply+=" for %d booking(s)"%(count,)
        
        return self.attack(request, user, id, reply)
    
    def attack(self, request, user, id, message=None):
        attack = Attack.load(id)
        if attack and attack.active:
            from Arthur.views.attack.attack import view
            return view.execute(request, user, id, message)
        else:
            from Arthur.views.attack.attack import attack
            return attack.execute(request, user, message)
