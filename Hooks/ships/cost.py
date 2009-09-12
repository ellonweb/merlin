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
from Core.paconf import PA
from Core.maps import Ship
from Core.loadable import loadable

@loadable.module()
class cost(loadable):
    """Calculates the cost of producing the specified number of ships"""
    usage = " <number> <ship>"
    paramre = re.compile(r"\s(\d+(?:\.\d+)?[km]?)\s(\w+)")
    
    def execute(self, message, user, params):
        
        num, name = params.groups()
        
        ship = Ship.load(name=name)
        if ship is None:
            message.alert("No Ship called: %s" % (name,))
            return
        
        feud = PA.getfloat("feud","prodcost")
        num = self.short2num(num)
        reply="Buying %s %s will cost %s metal, %s crystal and %s eonium."%(num,ship.name,
                self.num2short(ship.metal*num),
                self.num2short(ship.crystal*num),
                self.num2short(ship.eonium*num))
        reply+=" Feudalism: %s metal, %s crystal and %s eonium."%(
                self.num2short(ship.metal*(1+feud)*num),
                self.num2short(ship.crystal*(1+feud)*num),
                self.num2short(ship.eonium*(1+feud)*num))
        reply+=" It will add %s value"%(self.num2short(ship.total_cost*num/100),)
        message.reply(reply)
