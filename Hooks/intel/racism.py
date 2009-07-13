# Racism

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

import re
from .variables import access
from .Core.modules import M
loadable = M.loadable.loadable

class racism(loadable):
    """Shows averages for each race matching a given alliance in intel."""
    
    def __init__(self):
        loadable.__init__(self)
        self.paramre = re.compile(r"\s([\w-]+)")
        self.usage += " alliance"
    
    @loadable.run_with_access(access.get('hc',0) | access.get('intel',access['member']))
    def execute(self, message, user, params):
        
        alliance = M.DB.Maps.Alliance.load(params.group(1))
        if alliance is None:
            message.reply("No alliance matching '%s' found"%(params.group(1),))
            return
        
        session = M.DB.Session()
        Q = session.query(M.DB.SQL.f.sum(M.DB.Maps.Planet.value), M.DB.SQL.f.sum(M.DB.Maps.Planet.score),
                          M.DB.SQL.f.sum(M.DB.Maps.Planet.size), M.DB.SQL.f.sum(M.DB.Maps.Planet.xp),
                          M.DB.SQL.f.count(), M.DB.Maps.Planet.race)
        Q = Q.join(M.DB.Maps.Planet.intel)
        Q = Q.filter(M.DB.Maps.Intel.alliance_id==alliance.id)
        Q = Q.group_by(M.DB.Maps.Intel.alliance_id, M.DB.Maps.Planet.race)
        Q = Q.order_by(M.DB.SQL.asc(M.DB.Maps.Planet.race))
        result = Q.all()
        session.close()
        if len(result) < 1:
            message.reply("No planets in intel match alliance %s"%(alliance.name,))
            return
        prev=[]
        for value, score, size, xp, members, race in result:
            reply="%s %s Val(%s)" % (members,race,self.num2short(value/members),)
            reply+=" Score(%s)" % (self.num2short(score/members),)
            reply+=" Size(%s) XP(%s)" % (size/members,self.num2short(xp/members),)
            prev.append(reply)
        reply="Demographics for %s: "%(alliance.name,)+ ' | '.join(prev)
        message.reply(reply)
