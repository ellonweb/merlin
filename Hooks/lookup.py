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
from Core.exceptions_ import PNickParseError
from Core.db import session
from Core.maps import Galaxy, Planet, Alliance, User
from Core.loadable import loadable

@loadable.module()
class lookup(loadable):
    """"""
    usage = " [x:y[:z]|alliance|user]"
    paramre = (loadable.coordre, re.compile(r"(?:\s(\S+))?"),)
    
    def execute(self, message, user, params):
        
        # Planet or Galaxy
        if len(params.groups()) == 5:
            # Planet
            if params.group(5) is not None:
                planet = Planet.load(*params.group(1,3,5))
                if planet is None:
                    message.reply("No planet with coords %s:%s:%s found" % params.group(1,3,5))
                    return
                message.reply(str(planet))
                return
            
            # Galaxy
            else:
                galaxy = Galaxy.load(*params.group(1,3))
                if galaxy is None:
                    message.reply("No galaxy with coords %s:%s" % params.group(1,3))
                    return
                message.reply(str(galaxy))
                return
            
        
        # User or Alliance
        else:
            alliance = Alliance.load(params.group(1)) if params.group(1) is not None else None
            # Alliance
            if alliance is not None:
                message.reply(str(alliance))
                return
            
            # User
            if params.group(1) is None:
                message.reply(str(self.get_user_planet(user)))
                return
            elif not self.is_user(user):
                raise PNickParseError
            elif not user.is_member():
                message.reply("No alliance matching '%s' found" % (params.group(1),))
                return
            else:
                lookup = User.load(params.group(1), exact=False)
                if lookup is None:
                    message.reply("No alliance or user matching '%s' found" % (params.group(1),))
                    return
                elif lookup.planet is None:
                    message.reply("User %s has not entered their planet details" % (lookup.name,))
                    return
                else:
                    message.reply(str(lookup.planet))
                    return
