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
 
from Core.paconf import PA
from Core.db import session
from Core.maps import Ship
from Core.loadable import loadable, route

class eff(loadable):
    """Calculates the efficiency of the specified number of ships"""
    usage = " <number> <ship> [t1|t2|t3]"
    
    @route(r"(\d+(?:\.\d+)?[km]?)\s+(\w+)(?:\s+(t1|t2|t3))?")
    def execute(self, message, user, params):
        
        num, name, target = params.groups()
        target = (target or "t1").lower()
        
        ship = Ship.load(name=name)
        num = self.short2num(num)
        if ship is None:
            message.alert("No Ship called: %s" % (name,))
            return
        efficiency = PA.getfloat("teffs",target.lower())
        target_class = getattr(ship, target)
        if ship.damage:
            total_damage = ship.damage * num
        if ship.t1 == "Roids":
            killed = total_damage/50
            message.reply("%s %s (%s) will capture Asteroid: %s (%s)" % (
                num, ship.name, self.num2short(num*ship.total_cost/100),
                killed, self.num2short(killed*PA.getint("numbers", "roid_value")),))
            return
        if ship.t1 == "Struct":
            killed = total_damage/500
            message.reply("%s %s (%s) will destroy Structure: %s (%s)" % (
                num, ship.name, self.num2short(num*ship.total_cost/100),
                killed, self.num2short(killed*PA.getint("numbers", "cons_value")),))
            return
        targets = session.query(Ship).filter(Ship.class_ == target_class)
        if targets.count() == 0:
            message.reply("%s does not have any targets in that category (%s)" % (ship.name,target))
            return
        reply="%s %s (%s) hitting %s will " % (num, ship.name,self.num2short(num*ship.total_cost/100),target_class)
        if ship.type.lower() == "norm" or ship.type.lower() == 'cloak':
            reply+="destroy "
        elif ship.type.lower() == "emp":
            reply+="hug "
        elif ship.type.lower() == "steal":
            reply+="steal "
        else:
            raise Exception("Erroneous type %s" % (ship.type,))
        for target in targets:
            if ship.type.lower() == "emp" :
                killed=int(efficiency * ship.guns*num*float(100-target.empres)/100)
            else:
                killed=int(efficiency * total_damage/target.armor)
            reply+="%s: %s (%s) " % (target.name,killed,self.num2short(target.total_cost*killed/100))
        message.reply(reply)
