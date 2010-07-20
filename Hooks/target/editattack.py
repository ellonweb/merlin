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
from Core.config import Config
from Core.paconf import PA
from Core.db import session
from Core.maps import Updates, Planet, User, Attack, Galaxy, AttackTarget
from Core.loadable import loadable, route, require_user

class editattack(loadable):
    usage = " [<id> add|remove <coordlist>] | [<id> land <tick|eta>]"
    
    @route(r"(\d+)\s+add\s+([. :\-\d,]+)?", access = "member")
    def add(self, message, user, params):
        error = ""
        added = ""
        
        id = int(params.group(1))
        attack = Attack.load(id)
        if attack is None:
            message.alert("No attack exists with id %d" %(id))
            return
        
        for coord in re.findall(loadable.coord, params.group(2)):
            if not coord[4]:
                
                galaxy = Galaxy.load(coord[0],coord[2])
                
                if galaxy is None:
                    error += " %s:%s" % (coord[0],coord[2])
                else:
                    errordetail,planetadded= attack.addGalaxy(galaxy)
                    error += errordetail
                    if planetadded:
                        added += " %d:%d" %(galaxy.x,galaxy.y)

            else:
                planet = Planet.load(coord[0],coord[2],coord[4])
                
                if planet and attack.addPlanet(planet):
                    added += " %d:%d:%d" %(planet.x,planet.y,planet.z)
                else:
                    error += " %s:%s:%s" %(coord[0],coord[2],coord[4])
                
        session.commit()
        
        if added == "":
            added = "No coords "
            
        message.reply("%s added to attack %d. Coords not added: %s" %(added,attack.id,error))
            
    @route(r"(\d+)\s+remove\s+([. :\-\d,]+)?", access = "member")
    def remove(self, message, user, params):
        error = ""
        removed = ""
        id = int(params.group(1))
        attack = Attack.load(id)
      
        if attack is None:
            message.alert("No attack exists with id %d" %(id))
            return
        
        for coord in re.findall(loadable.coord, params.group(2)):
            if not coord[4]:
                
                galaxy = Galaxy.load(coord[0],coord[2])
                
                if galaxy is None:
                    error+=" %s:%s" % (coord[0],coord[2])
                else:
                    errordetail,planetremoved = attack.removeGalaxy(galaxy)
                    error += errordetail
                    if planetremoved:
                        removed += " %d:%d" %(galaxy.x,galaxy.y)
                
            else:
                
                planet = Planet.load(coord[0],coord[2],coord[4])
                
                if planet and attack.removePlanet(planet):
                    removed += " %d:%d:%d" %(planet.x,planet.y,planet.z)
                else:
                    error += " %s:%s:%s" %(coord[0],coord[2],coord[4])
                
        session.commit()
        
        if removed == "":
            removed = "No coords "
            
        message.reply("%s removed from attack %d. Coords not removed: %s" %(removed,attack.id,error))    

    @route(r"(\d+)\s+land\s+(\d+)",access="member")
    def land(self, message, user, params):
        id = int(params.group(1))
        attack = Attack.load(id) 
        
        if attack is None:
            message.alert("No attack exists with id %d" %(id))
            
        tick = Updates.current_tick()
        when = int(params.group(2))
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
            
        old = attack.landtick
        
        attack.landtick = when
        
        session.commit()
        
        message.reply("Changed LT for attack %d from %d to %d"%(id,old,when))
