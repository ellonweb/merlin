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
    usage = " [ add attackID <coordlist>] | [ (eta|landingtick) <coordlist>] | [ remove attackID <coordlist>] | list"
    
    @route(r"list",access="member")
    def list(self,message,user,params):
        reply = "Open attacks:"
        
        Q = session.query(Attack)
        Q = Q.order_by(asc(Attack.landtick))
        
        for attack in Q:
            if attack.active:
                reply += " %d : %s LT: %d" %(attack.id,attack.comment,attack.landtick)
        
        message.reply(reply)

    @route(r"add\s+(\d+)\s+([. :\-\d,]+)?", access = "member")
    def add(self, message, user, params):
        id = int(params.group(1))
        attack = Attack.load(id)
        if attack is None:
            message.alert("No attack exists with id %d" %(id))
            return
            
        for coord in re.findall(loadable.coord, params.group(2)):
            if not coord[4]:
                print "galaxy"
                galaxy = Galaxy.load(coord[0],coord[2])
                
                if galaxy is None:
                    message.alert("No galaxy with coords %s:%s" % (coord[0],coord[2]))
                    return
            
                attack.addGalaxy(galaxy)
                    
            else:
                planet = Planet.load(coord[0],coord[2],coord[4])
                
                if planet is None:
                    message.alert("No planet with coords %s:%s:%s" %(coord[0],coord[2],coord[4]))
                    return
                    
                attack.planets.append(planet)
                
                
        session.commit()
            
        message.reply("Coords added to attack %d" %(attack.id))
            
    
    @route(r"(\d+)\s+([. :\-\d,]+)(?:\s*(.+))?", access = "member")
    def new(self, message, user, params):
        
        tick = Updates.current_tick()
        comment = params.group(3)
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
            
            
        for coord in re.findall(loadable.coord, params.group(2)):
            if not coord[4]:
                print "galaxy"
                galaxy = Galaxy.load(coord[0],coord[2])
                
                if galaxy is None:
                    message.alert("No galaxy with coords %s:%s" % (coord[0],coord[2]))
                    return
            
                attack = Attack(landtick=when,comment=comment)
                session.add(attack)
        
                attack.addGalaxy(galaxy)
                    
            else:
                planet = Planet.load(coord[0],coord[2],coord[4])
                
                if planet is None:
                    message.alert("No planet with coords %s:%s:%s" %(coord[0],coord[2],coord[4]))
                    return
                    
                attack = Attack(landtick=when,comment=comment)
                session.add(attack)
            
                attack.planets.append(planet)

        session.commit()
            
        message.reply("Attack %s created with id %d"%(comment,attack.id))        
    
    @route(r"remove\s+(\d+)\s+([. :\-\d,]+)?", access = "member")
    def remove(self, message, user, params):
        id = int(params.group(1))
        attack = Attack.load(id)
        if attack is None:
            message.alert("No attack exists with id %d" %(id))
            return
            
        for coord in re.findall(loadable.coord, params.group(2)):
            if not coord[4]:
                print "galaxy"
                galaxy = Galaxy.load(coord[0],coord[2])
                
                if galaxy is None:
                    message.alert("No galaxy with coords %s:%s" % (coord[0],coord[2]))
                    return
            
                attack.removeGalaxy(galaxy)
                    
            else:
                planet = Planet.load(coord[0],coord[2],coord[4])
                
                if planet is None:
                    message.alert("No planet with coords %s:%s:%s" %(coord[0],coord[2],coord[4]))
                    return
                    
                attack.planets.remove(planet)
                
                
        session.commit()
            
        message.reply("Coords removed from attack %d" %(attack.id))