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
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import asc
from Core.config import Config
from Core.db import session
from Core.maps import Updates, Planet, User, Target
from Core.loadable import loadable

@loadable.module("half")
class book(loadable):
    """Book a target for attack. You should always book your targets, so someone doesn't inadvertedly piggy your attack."""
    usage = " x:y:z (eta|landing tick) [later]"
    paramre = re.compile(loadable.planet_coordre.pattern+r"\s+(\d+)(?:\s+(y)\S*)?(?:\s+(l)\S*)?",re.I)
    
    @loadable.require_user
    def execute(self, message, user, params):
        planet = Planet.load(*params.group(1,3,5))
        if planet is None:
            message.alert("No planet with coords %s:%s:%s" % params.group(1,3,5))
            return
        
        tick = Updates.current_tick()
        when = int(params.group(6))
        if when < 32:
            eta = when
            when += tick
        elif when <= tick:
            message.alert("Can not book targets in the past. You wanted tick %s, but current tick is %s." % (when, tick,))
            return
        else:
            eta = when - tick
        if when > 32767:
            when = 32767        
        
        override = params.group(7)
        later = params.group(8)
        
        if planet.intel and planet.alliance and planet.alliance.name == Config.get("Alliance","name"):
            message.reply("%s:%s:%s is %s in %s. Quick, launch before they notice the highlight." % (planet.x,planet.y,planet.z, planet.intel.nick or 'someone', Config.get("Alliance","name"),))
            return
        
        free, book1, book2 = self.get_free_book(planet, when, later)
        
        if free is None:
            if later is None:
                message.reply("Target %s:%s:%s is already booked for landing tick %s by user %s" % (planet.x,planet.y,planet.z, when, book1.user.name,))
            else:
                message.reply("You cannot hit %s:%s:%s. Not even sloppy seconds. This target is more taken than your mum, amirite?" % (planet.x,planet.y,planet.z,))
            return
        
        if override is None and later is None:
            books = planet.bookings.filter(Target.tick >= when).order_by(asc(Target.tick)).all()
            if len(books) >= 1:
                reply = "There are already bookings for that target after landing pt %s (eta %s). To see status on this target, do !status %s:%s:%s." % (when,eta, planet.x,planet.y,planet.z,)
                reply+= " To force booking at your desired eta/landing tick, use !book %s:%s:%s %s yes (Bookers: " %(planet.x,planet.y,planet.z, when,)
                prev=[]
                for book in books:
                    prev.append("(%s user:%s)" % (book.tick, book.user.name,))
                reply += ", ".join(prev) + ")"
                message.reply(reply)
                return
        
        if free == when:
            reply = "Booked landing on %s:%s:%s tick %s (eta %s) for user %s" % (planet.x,planet.y,planet.z, free, (free-tick), user.name,)
        elif free == when + 1:
            reply = "You have been beaten to %s:%s:%s by %s. You are now getting sloppy seconds at tick %s (eta %s)" % (planet.x,planet.y,planet.z, book1.user.name, free, (free-tick),)
        elif free == when + 2:
            reply = "You've been beaten to %s:%s:%s by %s and %s you slow retarded faggot. I feel sorry for you, so have tick %s (eta %s)" % (planet.x,planet.y,planet.z, book1.user.name, book2.user.name, free, (free-tick),)
        
        try:
            planet.bookings.append(Target(user=user, tick=free))
            session.commit()
            message.reply(reply)
            return
        except IntegrityError:
            session.rollback()
            raise Exception("Integrity error? Unable to booking for pid %s and tick %s"%(planet.id, when,))
            return
    
    def get_free_book(self, planet, when, later):
        book1 = planet.bookings.filter(Target.tick == when).first()
        if book1 is None:
            return when, None, None
        if later is None:
            return None, book1, None
        when += 1
        book2 = planet.bookings.filter(Target.tick == when).first()
        if book2 is None:
            return when, book1, None
        when += 1
        book3 = planet.bookings.filter(Target.tick == when).first()
        if book3 is None:
            return when, book1, book2
        else:
            return None, book1, book2
