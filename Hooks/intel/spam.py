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
from sqlalchemy.sql.functions import count, sum
from .variables import access
from .Core.modules import M
loadable = M.loadable.loadable

class spam(loadable):
    """Spam alliance coords"""
    
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
        Q = session.query(M.DB.Maps.Planet, M.DB.Maps.Intel)
        Q = Q.join((M.DB.Maps.Intel, M.DB.Maps.Intel.planet_id==M.DB.Maps.Planet.id))
        Q = Q.filter(M.DB.Maps.Intel.alliance_id==alliance.id)
        result = Q.all()
        session.close()
        if len(result) < 1:
            message.reply("No planets in intel match alliance %s"%(alliance.name,))
            return
        printable=map(lambda (p, i): "%s:%s:%s" % (p.x,p.y,p.z),result)
        reply="Spam on alliance %s - " %(alliance.name)
        reply += str.join(' | ', printable)
        message.reply(reply)
