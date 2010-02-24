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
 
from Core.maps import Planet
from Core.loadable import loadable, route

class maxcap(loadable):
    usage = " (<total roids>|<x:y:z> [a:b:c])"
    
    @route(r"(\d+)\s*$")
    def size(self, message, user, params):
        target = Planet(size=int(params.group(1)))
        attacker = None
        self.execute(message, target, attacker)
    
    @route(r"%s(?:\s+%s)?"%((loadable.planet_coord,)*2))
    def planet(self, message, user, params):
        if params.group(6) is None:
            target = Planet.load(*params.group(1,3,5))
            if target is None:
                message.alert("No planet with coords %s:%s:%s" % params.group(1,3,5))
                return
            if self.user_has_planet(user):
                attacker = user.planet
            else:
                attacker = None
        else:
            target = Planet.load(*params.group(1,3,5))
            if target is None:
                message.alert("No planet with coords %s:%s:%s" % params.group(1,3,5))
                return
            attacker = Planet.load(*params.group(6,8,10))
            if attacker is None:
                message.alert("No planet with coords %s:%s:%s" % params.group(6,8,10))
                return
        
        self.execute(message, target, attacker)
    
    def execute(self, message, target, attacker):
        reply = ""
        total = 0
        for i in range(1,5):
            cap = target.maxcap(attacker)
            total += cap
            reply+="Wave %d: %d (%d), " % (i,cap,total,)
            target.size -= cap
        message.reply("Caprate: %s%% %s"%(int(target.caprate(attacker)*100),reply.strip(', ')))
