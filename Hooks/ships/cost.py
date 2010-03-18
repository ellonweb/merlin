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
from Core.maps import Ship
from Core.loadable import loadable, route

class cost(loadable):
    """Calculates the cost of producing the specified number of ships"""
    usage = " <number> <ship>"
    
    @route(r"(\d+(?:\.\d+)?[km]?)\s+(\w+)")
    def execute(self, message, user, params):
        
        num, name = params.groups()
        
        ship = Ship.load(name=name)
        if ship is None:
            message.alert("No Ship called: %s" % (name,))
            return
        
        num = self.short2num(num)
        reply="Buying %s %s will cost %s metal, %s crystal and %s eonium."%(num,ship.name,
                self.num2short(ship.metal*num),
                self.num2short(ship.crystal*num),
                self.num2short(ship.eonium*num))
        
        for gov in PA.options("govs"):
            bonus = PA.getfloat(gov, "prodcost")
            if bonus == 0:
                continue
            
            reply += " %s: %s metal, %s crystal and %s eonium."%(
                        PA.get(gov, "name"),
                        self.num2short(ship.metal*(1+bonus)*num),
                        self.num2short(ship.crystal*(1+bonus)*num),
                        self.num2short(ship.eonium*(1+bonus)*num))
        
        reply+=" It will add %s value"%(self.num2short(ship.total_cost*num/100),)
        message.reply(reply)
