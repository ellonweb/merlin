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
from Core.paconf import PA
from Core.db import session
from Core.maps import Updates, Galaxy, Planet, Attack
from Core.loadable import loadable, route

class editattack(loadable):
    usage = " [<id> add|remove <coordlist>] | [<id> land <tick|eta>] | [<id> comment <comment>]"
    access = "half"
    
    @route(r"(\d+)\s+add\s+([. :\-\d,]+)")
    def add(self, message, user, params):
        id = int(params.group(1))
        attack = Attack.load(id)
        if attack is None:
            message.alert("No attack exists with id %d" %(id))
            return
        
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
    
    @route(r"(\d+)\s+rem(?:ove)?\s+([. :\-\d,]+)")
    def remove(self, message, user, params):
        id = int(params.group(1))
        attack = Attack.load(id)
        if attack is None:
            message.alert("No attack exists with id %d" %(id))
            return
        
        for coord in re.findall(loadable.coord, params.group(2)):
            if not coord[4]:
                galaxy = Galaxy.load(coord[0],coord[2])
                if galaxy:
                    attack.removeGalaxy(galaxy)
            
            else:
                planet = Planet.load(coord[0],coord[2],coord[4])
                if planet:
                    attack.removePlanet(planet)
        
        session.commit()
        message.reply(str(attack))
    
    @route(r"(\d+)\s+land\s+(\d+)")
    def land(self, message, user, params):
        id = int(params.group(1))
        attack = Attack.load(id)
        if attack is None:
            message.alert("No attack exists with id %d" %(id))
            return
        
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
    
    @route(r"(\d+)\s+comment\s+(\S.*)")
    def comment(self, message, user, params):
        id = int(params.group(1))
        attack = Attack.load(id)
        if attack is None:
            message.alert("No attack exists with id %d" %(id))
            return
        
        if params.group(2) in self.nulls:
            attack.comment = ""
        else:
            attack.comment = params.group(2)
        
        session.commit()
        message.reply("Updated comment for attack %d: %s"%(id,attack.comment,))
