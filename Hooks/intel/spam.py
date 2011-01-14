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
from Core.db import session
from Core.maps import Planet, Alliance, Intel
from Core.loadable import loadable, route

class spam(loadable):
    """Spam alliance coords"""
    usage = " <alliance>"
    
    @route(r"(\S+)", access = "galmate")
    def execute(self, message, user, params):
        
        alliance = Alliance.load(params.group(1), active=False)
        if alliance is None:
            message.reply("No alliance matching '%s' found"%(params.group(1),))
            return
        
        Q = session.query(Planet, Intel)
        Q = Q.join(Planet.intel)
        Q = Q.filter(Planet.active == True)
        Q = Q.filter(Intel.alliance==alliance)
        Q = Q.order_by(asc(Planet.x), asc(Planet.y), asc(Planet.z))
        result = Q.all()
        if len(result) < 1:
            message.reply("No planets in intel match alliance %s"%(alliance.name,))
            return
        printable=map(lambda (p, i): "%s:%s:%s" % (p.x,p.y,p.z),result)
        reply="Spam on alliance %s - " %(alliance.name)
        reply += ' | '.join(printable)
        message.reply(reply)
