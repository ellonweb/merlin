# Details

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

from .variables import access
from .Core.modules import M
loadable = M.loadable.loadable

class details(loadable):
    """This command basically collates lookup, xp, intel and status into one simple to use command. Neat, huh?"""
    
    def __init__(self):
        loadable.__init__(self)
        self.paramre = self.planet_coordre
        self.usage += " x.y.z"
    
    @loadable.run_with_access(access.get('hc',0) | access.get('intel',access['member']))
    def execute(self, message, user, params):
        
        target = M.DB.Maps.Planet.load(*params.groups())
        if target is None:
            message.reply("No planet matching '%s:%s:%s' found"%params.groups(),)
            return
        message.reply(target)
        
        session = M.DB.Session()
        session.add(user)
        if user.planet is not None:
            attacker = user.planet
            reply="Target "
            reply+="%s:%s:%s (%s|%s) "%(target.x,target.y,target.z,
                                        self.num2short(target.value*100),self.num2short(target.score*100))
            reply+="| Attacker %s:%s:%s (%s|%s) "%(attacker.x,attacker.y,attacker.z,
                                                   self.num2short(attacker.value*100),self.num2short(attacker.score*100))
            bravery = attacker.bravery(target)
            reply+="| Bravery: %.2f " % (bravery,)
            cap=target.maxcap()
            xp=int(cap*bravery)
            reply+="| Roids: %s | XP: %s | Score: %s" % (cap,xp,xp*60)
            message.reply(reply)
        
        session.add(target)
        if target.intel is not None:
            message.reply(("Information stored for %s:%s:%s -"+str(target.intel) if str(target.intel) else "No information stored for %s:%s:%s") % (target.x, target.y, target.z,))
        
        session.close()
