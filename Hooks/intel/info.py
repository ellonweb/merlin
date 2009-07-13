# Info

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

class info(loadable):
    """Alliance information (All information taken from intel, for tag information use the lookup command)"""
    
    def __init__(self):
        loadable.__init__(self)
        self.paramre = re.compile(r"\s([\w-]+)")
        self.usage += " alliance"
    
    @loadable.run_with_access(access.get('hc',0) | access.get('intel',access['member))
    def execute(self, message, user, params):
        
        alliance = M.DB.Maps.Alliance.load(params.group(1))
        if alliance is None:
            message.reply("No alliance matching '%s' found"%(params.group(1),))
            return
        
        session = M.DB.Session()
        Q = session.query(M.DB.SQL.f.sum(M.DB.Maps.Planet.value), M.DB.SQL.f.sum(M.DB.Maps.Planet.score),
                          M.DB.SQL.f.sum(M.DB.Maps.Planet.size), M.DB.SQL.f.sum(M.DB.Maps.Planet.xp),
                          M.DB.SQL.f.count())
        Q = Q.join(M.DB.Maps.Planet.intel)
        Q = Q.filter(M.DB.Maps.Intel.alliance_id==alliance.id)
        Q = Q.group_by(M.DB.Maps.Intel.alliance_id)
        result = Q.first()
        session.close()
        if result is None:
            message.reply("No planets in intel match alliance %s"%(alliance.name,))
            return
        
        value, score, size, xp, members = result
        if members <= 60:
            reply="%s Members: %s, Value: %s, Avg: %s," % (alliance.name,members,value,value/members)
            reply+=" Score: %s, Avg: %s," % (score,score/members) 
            reply+=" Size: %s, Avg: %s, XP: %s, Avg: %s" % (size,size/members,xp,xp/members)
            message.reply(reply)
        else:
            session = M.DB.Session()
            Q = session.query(M.DB.Maps.Planet.value, M.DB.Maps.Planet.score, 
                              M.DB.Maps.Planet.size, M.DB.Maps.Planet.xp, 
                              M.DB.Maps.Intel.alliance_id)
            Q = Q.join(M.DB.Maps.Planet.intel)
            Q = Q.filter(M.DB.Maps.Intel.alliance_id==alliance.id)
            Q = Q.order_by(M.DB.SQL.desc(M.DB.Maps.Planet.score))
            Q = Q.limit(60)
            Q = Q.from_self(M.DB.SQL.f.sum(M.DB.Maps.Planet.value), M.DB.SQL.f.sum(M.DB.Maps.Planet.score),
                            M.DB.SQL.f.sum(M.DB.Maps.Planet.size), M.DB.SQL.f.sum(M.DB.Maps.Planet.xp),
                            M.DB.SQL.f.count())
            Q = Q.group_by(M.DB.Maps.Intel.alliance_id)
            ts_result = Q.first()
            session.close()
            
            ts_value, ts_score, ts_size, ts_xp, ts_members = ts_result
            reply="%s Members: %s (%s)" % (alliance.name,members,ts_members)
            reply+=", Value: %s (%s), Avg: %s (%s)" % (value,ts_value,value/members,ts_value/ts_members)
            reply+=", Score: %s (%s), Avg: %s (%s)" % (score,ts_score,score/members,ts_score/ts_members)
            reply+=", Size: %s (%s), Avg: %s (%s)" % (size,ts_size,size/members,ts_size/ts_members)
            reply+=", XP: %s (%s), Avg: %s (%s)" % (xp,ts_xp,xp/members,ts_xp/ts_members)
            message.reply(reply)
