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
 
from sqlalchemy.sql import asc
from sqlalchemy.sql.functions import count, sum
from Core.db import session
from Core.maps import Galaxy, Planet, Alliance, Intel
from Core.loadable import loadable, route

class racism(loadable):
    """Shows averages for each race matching a given alliance in intel or for a galaxy."""
    usage = " <alliance> | <x:y>"
    
    @route(r"(\S+)", access = "galmate")
    def intel_alliance(self, message, user, params):
        
        alliance = Alliance.load(params.group(1))
        if alliance is None:
            message.reply("No alliance matching '%s' found"%(params.group(1),))
            return
        
        Q = session.query(sum(Planet.value), sum(Planet.score),
                          sum(Planet.size), sum(Planet.xp),
                          count(), Planet.race)
        Q = Q.join(Planet.intel)
        Q = Q.filter(Planet.active == True)
        Q = Q.filter(Intel.alliance==alliance)
        Q = Q.group_by(Intel.alliance_id, Planet.race)
        Q = Q.order_by(asc(Planet.race))
        result = Q.all()
        if len(result) < 1:
            message.reply("No planets in intel match alliance %s"%(alliance.name,))
            return
        
        self.execute(message, alliance.name, result)
    
    @route(loadable.coord, access = "galmate")
    def galaxy(self, message, user, params):
        galaxy = Galaxy.load(*params.group(1,3))
        if galaxy is None:
            message.alert("No galaxy with coords %s:%s" % params.group(1,3))
            return
        
        Q = session.query(sum(Planet.value), sum(Planet.score),
                          sum(Planet.size), sum(Planet.xp),
                          count(), Planet.race)
        Q = Q.filter(Planet.galaxy == galaxy)
        Q = Q.filter(Planet.active == True)
        Q = Q.group_by(Planet.race)
        Q = Q.order_by(asc(Planet.race))
        result = Q.all()
        
        self.execute(message, "%s:%s" % (galaxy.x, galaxy.y,), result)
    
    def execute(self, message, target, result):
        prev=[]
        for value, score, size, xp, members, race in result:
            reply="%s %s Val(%s)" % (members,race,self.num2short(value/members),)
            reply+=" Score(%s)" % (self.num2short(score/members),)
            reply+=" Size(%s) XP(%s)" % (size/members,self.num2short(xp/members),)
            prev.append(reply)
        reply="Demographics for %s - "%(target,)+ ' | '.join(prev)
        message.reply(reply)
