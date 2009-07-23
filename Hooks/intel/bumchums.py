# bumchums

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

class bumchums(loadable):
    """Pies"""
    
    def __init__(self):
        loadable.__init__(self)
        self.paramre = re.compile(r"\s([\w-]+)(?:\s(\d+))?")
        self.usage += " alliance number"
    
    @loadable.run_with_access(access.get('hc',0) | access.get('intel',access['member']))
    def execute(self, message, user, params):
        
        alliance = M.DB.Maps.Alliance.load(params.group(1))
        if alliance is None:
            message.reply("No alliance matching '%s' found"%(params.group(1),))
            return
        bums = int(params.group(2) or 1)
        session = M.DB.Session()
        Q = session.query(M.DB.Maps.Galaxy, M.DB.SQL.f.count())
        Q = Q.join(M.DB.Maps.Galaxy.planets)
        Q = Q.join(M.DB.Maps.Planet.intel)
        Q = Q.filter(M.DB.Maps.Intel.alliance==alliance)
        Q = Q.group_by(M.DB.Maps.Galaxy.x, M.DB.Maps.Galaxy.y)
        Q = Q.having(M.DB.SQL.f.count() >= bums)
        result = Q.all()
        session.close()
        if len(result) < 1:
            message.reply("No galaxies with at least %s bumchums from %s"%(bums,alliance.name,))
            return
        prev=[]
        for galaxy, chums in result:
            prev.append("%s:%s (%s)"%(galaxy.x, galaxy.y, chums))
        reply="Galaxies with at least %s bums from %s: "%(bums,alliance.name)+ ' | '.join(prev)
        message.reply(reply)
