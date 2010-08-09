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
 
from sqlalchemy.sql.functions import count, max
from Core.config import Config
from Core.paconf import PA
from Core.db import session
from Core.maps import Planet, Scan
from Core.chanusertracker import CUT
from Core.loadable import loadable, route, robohci

class scans(loadable):
    usage = " <x:y:z>"
    
    @route(loadable.planet_coord, access = "half")
    def execute(self, message, user, params):
        
        planet = Planet.load(*params.group(1,3,5))
        if planet is None:
            message.reply("No planet with coords %s:%s:%s found" % params.group(1,3,5))
            return
        
        Q = session.query(Scan.scantype, max(Scan.tick), count())
        Q = Q.filter(Scan.planet == planet)
        Q = Q.group_by(Scan.scantype)
        result = Q.all()
        
        if len(result) < 1:
            message.reply("No scans available on %s:%s:%s" % (planet.x,planet.y,planet.z,))
            return
        
        prev=[]
        for type, latest, number in result:
            prev.append("(%d %s, latest pt%s)" % (number,type,latest,))
        
        reply="scans for %s:%s:%s - " % (planet.x,planet.y,planet.z) + ", ".join(prev)
        message.reply(reply)
    
    @robohci
    def robocop(self, message, scantype, pa_id, x, y, z, names):
        nicks = []
        [nicks.extend(nick) for nick in [CUT.list_user_nicks(name) for name in names.split(",")]]
        
        reply = "%s on %s:%s:%s " % (PA.get(scantype,"name"),x,y,z,)
        reply+= Config.get("URL","viewscan") % (pa_id,)
        for nick in nicks:
            message.privmsg(reply, nick)
        
        reply = "%s on %s:%s:%s " % (PA.get(scantype,"name"),x,y,z,)
        reply+= "delivered to: "
        reply+= ", ".join(nicks)
        from Hooks.scans.request import request
        message.privmsg(reply, request().scanchan())
