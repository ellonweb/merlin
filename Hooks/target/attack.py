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
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import asc
from Core.config import Config
from Core.paconf import PA
from Core.db import session
from Core.maps import Updates, Planet, User, Attack, Galaxy, AttackTarget
from Core.loadable import loadable, route, require_user

class attack(loadable):
    usage = "[ (eta|landingtick) <coordlist>] | list"
    
    @route(r"list",access="member")
    def list(self,message,user,params):
        reply = "Open attacks:"
        
        Q = session.query(Attack)
        Q = Q.order_by(asc(Attack.landtick))
        
        
        for attack in Q:
            if attack.active:
                comment = attack.comment
                if comment is None:
                    comment= " "
                else:
                    comment = " '" + comment + "' "
                reply += "  %d %sLT: %d |" %(attack.id,comment,attack.landtick)
        
        message.reply(reply)
        
    @route(r"show\s+(\d+)",access = "member")
    def show(self,message,user,params):
        id = params.group(1)
        attack = Attack.load(id)
        
        comment = attack.comment
        if comment is None:
            comment= " "
        else:
            comment = " '" + comment + "' "
        
        message.reply("Attack%sLT: %d Url: http://www.my-url.com/attack/%d"%(comment,attack.landtick,attack.id)) 

    @route(r"(\d+)\s+([. :\-\d,]+)(?:\s*(.+))?", access = "member")
    def new(self, message, user, params):
        error = ""
        added = ""

        tick = Updates.current_tick()
        comment = params.group(3)
        when = int(params.group(1))
        if when < PA.getint("numbers", "protection"):
            eta = when
            when += tick
        elif when <= tick:
            error += "Can not create attacks in the past. You wanted tick %s, but current tick is %s." % (when, tick,)
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
                
                if galaxy is None:
                    error+= " %s:%s" % (coord[0],coord[2])
                else:
                    errordetail,planetadded = attack.addGalaxy(galaxy)
                    error += errordetail
                    if planetadded:                
                        added += " %d:%d" %(galaxy.x,galaxy.y)
                    
            else:
                planet = Planet.load(coord[0],coord[2],coord[4])
                
                if planet is None or planet in attack.planets or (planet.intel and planet.alliance and planet.alliance.name == Config.get("Alliance","name")):
                    error += " %s:%s:%s" %(coord[0],coord[2],coord[4])
                else:    
                    attack.planets.append(planet)
                    added += " %d:%d:%d" %(planet.x,planet.y,planet.z)

        session.commit()
        if comment is None:  
            comment= " "
        else:
            comment = " " + comment + " "

        message.reply("Attack%screated with id %d for targets: %s. Targets not included( or doubles): %s"%(comment,attack.id,added,error))