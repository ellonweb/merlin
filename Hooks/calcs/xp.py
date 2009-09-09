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
from Core.maps import Planet
from Core.loadable import loadable

@loadable.module()
class xp(loadable):
    usage = " <x:y:z> [a:b:c]"
    paramre = re.compile(r"%s(?:\s+%s)?"%((loadable.planet_coordre.pattern,)*2))
    
    def execute(self, message, user, params):
        
        if params.group(4) is None:
            target = Planet.load(*params.group(1,2,3))
            if target is None:
                message.alert("No planet with coords %s:%s:%s" % params.group(1,2,3))
                return
            if not self.is_user(user):
                raise PNickParseError
            attacker = user.planet
            if attacker is None:
                message.alert("Make sure you've set your planet with !pref")
                return
        else:
            target = Planet.load(*params.group(1,2,3))
            if target is None:
                message.alert("No planet with coords %s:%s:%s" % params.group(1,2,3))
                return
            attacker = Planet.load(*params.group(4,5,6))
            if attacker is None:
                message.alert("No planet with coords %s:%s:%s" % params.group(4,5,6))
                return
        
        reply="Target "
        target_val = target.value
        attacker_val = attacker.value
        target_score = target.score
        attacker_score = attacker.score

        reply+="%s:%s:%s (%s|%s) "%(target.x,target.y,target.z,
                                 self.num2short(target.value),self.num2short(target.score))
        reply+="| Attacker %s:%s:%s (%s|%s) "%(attacker.x,attacker.y,attacker.z,
                                            self.num2short(attacker.value),self.num2short(attacker.score))

        reply+="| Bravery: %.2f " % (attacker.bravery(target),)

        cap=target.maxcap(attacker)
        xp=attacker.calc_xp(target)
        reply+="| Roids: %s | XP: %s | Score: %s" % (cap,xp,xp*60)
        message.reply(reply)
