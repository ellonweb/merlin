# Search

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

class search(loadable):
    """Search for a planet by alliance or nick."""
    
    def __init__(self):
        loadable.__init__(self)
        self.paramre = re.compile(r"\s([\w-]+)")
        self.usage += " alliance|nick"
    
    @loadable.run_with_access(access.get('hc',0) | access.get('intel',access['member']))
    def execute(self, message, user, params):
        
        param = "%"+params.group(1)+"%"
        session = M.DB.Session()
        Q = session.query(M.DB.Maps.Planet, M.DB.Maps.Intel, M.DB.Maps.Alliance)
        Q = Q.join(M.DB.Maps.Planet.intel)
        Q = Q.outerjoin(M.DB.Maps.Intel.alliance)
        Q = Q.filter(M.DB.or_(M.DB.Maps.Intel.nick.ilike(param), M.DB.Maps.Alliance.name.ilike(param)))
        result = Q[:6]
        session.close()
        if len(result) < 1:
            message.reply("No planets in intel matching nick or alliance: %s"%(params.group(1),))
            return
        replies = []
        for planet, intel, alliance in result[:5]:
            reply="%s:%s:%s (%s)" % (planet.x,planet.y,planet.z,planet.race)
            reply+=" Score: %s Value: %s Size: %s" % (planet.score,planet.value,planet.size)
            if intel.nick:
                reply+=" Nick: %s" % (intel.nick,)
            if alliance:
                reply+=" Alliance: %s" % (alliance.name,)
            if intel.reportchan:
                reply+=" Reportchan: %s" % (intel.reportchan,)
            if intel.comment:
                reply+=" Comment: %s" % (intel.comment,)
            replies.append(reply)
        if len(result) > 5:
            replies[-1]+=" (Too many results to list, please refine your search)"
        message.reply("\n".join(replies))
