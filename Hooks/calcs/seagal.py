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
 
import math
import re
from Core.maps import Planet
from Core.loadable import loadable

@loadable.module()
class seagal(loadable):
    usage = " <x:y:z> [sum]"
    paramre = re.compile(loadable.planet_coordre.pattern+r"(?:\s+(\d+))?")
    
    @loadable.require_planet
    def execute(self, message, user, params):
        
        p = Planet.load(*params.group(1,3,5))
        if p is None:
            message.alert("No planet with coords %s:%s:%s" % params.group(1,3,5))
            return
        
        sum=params.group(6)
        res=user.planet.resources_per_agent(p)
        reply="Your Seagals will ninja %s resources from %s:%s:%s - 13: %s, 35: %s."%(res,p.x,p.y,p.z,self.num2short(res*13),self.num2short(res*35))
        if sum:
            reply+=" You need %s Seagals to ninja %sk res."%(int(math.ceil((float(sum)*1000)/res)),sum)
        message.reply(reply)
