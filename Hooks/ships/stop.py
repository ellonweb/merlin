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
 
import math
from Core.paconf import PA
from Core.db import session
from Core.maps import Ship
from Core.loadable import loadable, route

class stop(loadable):
    """Calculates the required defence to the specified number of ships"""
    usage = " <number> <ship> [t1|t2|t3]"
    
    @route(r"hammertime")
    def hammertime(self, message, user, params):
        message.reply("Can't touch this!")
    
    @route(r"(\d+(?:\.\d+)?[km]?)\s+(\w+)(?:\s+(t1|t2|t3))?")
    def execute(self, message, user, params):
        
        num, name, attacker = params.groups()
        attacker = (attacker or "t1").lower()
        
        num = self.short2num(num)
        ship = Ship.load(name=name)
        if ship is not None:
            pass
        elif "asteroids".rfind(name.lower()) > -1:
            ship = Ship(name="Asteroids",class_="Roids",armor=50,total_cost=PA.getint("numbers", "roid_value")*PA.getint("numbers", "ship_value"))
        elif "constructions".rfind(name.lower()) > -1:
            ship = Ship(name="Constructions",class_="Struct",armor=500,total_cost=PA.getint("numbers", "cons_value")*PA.getint("numbers", "ship_value"))
        else:
            message.alert("No Ship called: %s" % (name,))
            return
        efficiency = PA.getfloat("teffs",attacker.lower())
        attacker_class = getattr(Ship, attacker)
        attackers = session.query(Ship).filter(attacker_class == ship.class_)
        if attackers.count() == 0:
            message.reply("%s are not hit by anything as that category (%s)" % (ship.name,attacker))
            return
        if ship.class_ == "Roids":
            reply="Capturing"
        elif ship.class_ == "Struct":
            reply="Destroying"
        else:
            reply="Stopping"
        reply+=" %s %s (%s) as %s requires " % (num, ship.name,self.num2short(num*ship.total_cost/PA.getint("numbers", "ship_value")),attacker)
        for attacker in attackers:
            if attacker.type.lower() == "emp" :
                needed=int((math.ceil(num/(float(100-ship.empres)/100)/attacker.guns))/efficiency)
            else:
                needed=int((math.ceil(float(ship.armor*num)/attacker.damage))/efficiency)
            reply+="%s: %s (%s) " % (attacker.name,needed,self.num2short(attacker.total_cost*needed/PA.getint("numbers", "ship_value")))
        message.reply(reply)
