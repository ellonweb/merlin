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
from Core.db import session
from Core.maps import Updates, Ship, UserFleet
from Core.loadable import loadable

@loadable.module("member")
class mydef(loadable):
    """Add your fleets for defense listing. For example: 2x 20k Barghest 30k Harpy Call me any time for hot shipsex."""
    usage = " [fleets] x <[ship count] [ship name]> [comment]"
    paramre = re.compile(r"\s+(\d)\s*x\s*(.*)",re.I)
    countre = re.compile(r"^(\d+(?:\.\d+)?[mk]?)$",re.I)
    shipre = re.compile(r"^(\w+),?$")
    
    @loadable.require_user
    def execute(self, message, user, params):
        
        fleetcount=int(params.group(1))
        garbage=params.group(2)
        # assign param variables
        reset_ships=False
        ships={}
        comment=""
        if garbage in self.nulls:
            reset_ships=True
        else:
            (ships, comment)=self.parse_garbage(garbage)
        
        self.reset_ships_and_comment(user,ships,fleetcount,comment,reset_ships)
        
        ships = user.fleets.all()
        
        reply = "Updated your def info to: fleetcount %s, updated: pt%s ships: " %(user.fleetcount,user.fleetupdated)
        reply+= ", ".join(map(lambda x:"%s %s" %(self.num2short(x.ship_count),x.ship.name),ships))
        reply+= " and comment: %s" %(user.fleetcomment)
        message.reply(reply)
    
    def reset_ships_and_comment(self,user,ships,fleetcount,comment,reset_ships):
        self.update_comment_and_fleetcount(user,fleetcount,comment)
        if len(ships) > 0 or reset_ships:
            self.update_fleets(user,ships)
        session.commit()
    
    def update_fleets(self,user,ships):
        user.fleets.delete()
        
        for ship, count in ships.items():
            user.fleets.append(UserFleet(ship=ship, ship_count=count))
    
    def update_comment_and_fleetcount(self,user,fleetcount,comment):
        user.fleetcount = fleetcount
        if comment != "":
            if comment in self.nulls:
                comment=""
            user.fleetcomment = comment
        user.fleetupdated = Updates.current_tick()

    def parse_garbage(self,garbage):
        parts=garbage.split()
        ships={}
        while len(parts) > 1:
            mc=self.countre.match(parts[0])
            ms=self.shipre.match(parts[1])
            if not mc or not ms:
                break
            
            count=self.short2num(mc.group(1))
            ship=ms.group(1)
            
            s = Ship.load(name=ship)
            
            if s is not None:
                ship=s.name
            else:
                break
            
            ships[ship]=count
            
            parts.pop(0)
            parts.pop(0)
        comment=" ".join(parts)
        return (ships, comment)
