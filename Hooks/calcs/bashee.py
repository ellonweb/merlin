# This file is part of Merlin.
 
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
 
# This work is Copyright (C)2008 of Robin K. Hansen, Elliot Rosemarine.
# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

from Core.exceptions_ import PNickParseError
from Core.paconf import PA
from Core.maps import Planet
from Core.loadable import loadable

@loadable.module()
class bashee(loadable):
    usage = " <x:y:z>"
    paramre = (loadable.planet_coordre, loadable.paramre,)
    
    def execute(self, message, user, params):
        
        if len(params.groups()) < 3:
            if not self.is_user(user):
                raise PNickParseError
            planet = user.planet
            if planet is None:
                message.alert("Make sure you've set your planet with !pref")
                return
        else:
            planet = Planet.load(*params.group(1,2,3))
            if planet is None:
                message.alert("No planet with coords %s:%s:%s" % params.group(1,2,3))
                return
        
        message.reply("%s:%s:%s can be hit by planets with value %d or below or score %d or below"%(planet.x,planet.y,planet.z,int(planet.value/PA.getfloat("bash","value")),int(planet.score/PA.getfloat("bash","score"))))
