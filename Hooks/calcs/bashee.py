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
from Core.maps import Planet
from Core.loadable import loadable, route, require_planet

class bashee(loadable):
    usage = " <x:y:z>"
    
    @route(loadable.planet_coord)
    def planet(self, message, user, params):
        planet = Planet.load(*params.group(1,3,5))
        if planet is None:
            message.alert("No planet with coords %s:%s:%s" % params.group(1,3,5))
            return
        self.execute(message, planet)
    
    @route(r"")
    @require_planet
    def me(self, message, user, params):
        self.execute(message, user.planet)
    
    def execute(self, message, planet):
        message.reply("%s:%s:%s can be hit by planets with value %d or below or score %d or below"%(planet.x,planet.y,planet.z,int(planet.value/PA.getfloat("bash","value")),int(planet.score/PA.getfloat("bash","score"))))
