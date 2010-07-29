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
 
import re
from sqlalchemy.sql import asc
from Core.paconf import PA
from Core.db import session
from Core.maps import Updates, Galaxy, Planet, Attack
from Core.loadable import loadable, route

class attack(loadable):
    """Create an attack page on the webby with automatic parsed scans"""
    usage = " [<eta|landingtick> <coordlist> [comment]] | [list] | [show <id>]"
    access = "half"
    
    @route(r"list")
    def list(self,message,user,params):
        Q = session.query(Attack)
        Q = Q.filter(Attack.landtick >= Updates.current_tick() - Attack._active_ticks)
        Q = Q.order_by(asc(Attack.id))
        
        replies = []
        for attack in Q:
            replies.append("(%d LT: %d %s)" %(attack.id,attack.landtick,attack.comment,))
        
        reply = "Open attacks: " + " ".join(replies)
        message.reply(reply)
    
    @route(r"(?:show\s+)?(\d+)")
    def show(self,message,user,params):
        id = params.group(1)
        attack = Attack.load(id)
        
        if attack is None:
            message.alert("No attack exists with id %s" %(id))
            return
        
        message.reply(str(attack))
    
    @route(r"(?:new\s+)?(\d+)\s+([. :\-\d,]+)(?:\s*(.+))?")
    def new(self, message, user, params):
        tick = Updates.current_tick()
        comment = params.group(3) or ""
        when = int(params.group(1))
        if when < PA.getint("numbers", "protection"):
            eta = when
            when += tick
        elif when <= tick:
            message.alert("Can not create attacks in the past. You wanted tick %s, but current tick is %s." % (when, tick,))
            return
        else:
            eta = when - tick
        if when > 32767:
            when = 32767
        
        attack = Attack(landtick=when,comment=comment)
        session.add(attack)
        
        for coord in re.findall(loadable.coord, params.group(2)):
            if not coord[4]:
                galaxy = Galaxy.load(coord[0],coord[2])
                if galaxy:
                    attack.addGalaxy(galaxy)
            
            else:
                planet = Planet.load(coord[0],coord[2],coord[4])
                if planet:
                    attack.addPlanet(planet)
        
        session.commit()
        message.reply(str(attack))
