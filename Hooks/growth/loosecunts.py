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
 
from sqlalchemy.sql import desc
from Core.config import Config
from Core.db import session
from Core.maps import Alliance, User, epenis
from Core.loadable import loadable, route

class loosecunts(loadable):
    
    @route(access = "member")
    def execute(self, message, user, params):
        
        alliance = Alliance.load(Config.get("Alliance","name"))
        if alliance is None:
            message.reply("No alliance matching '%s' found"%(Config.get("Alliance","name"),))
            return
        Q = session.query(User, epenis)
        Q = Q.join(User.epenis)
        Q = Q.order_by(desc(epenis.rank))
        result = Q[:5]
        
        if len(result) < 1:
            message.alert("There is no penis")
            return
        
        prev = []
        for user, penis in result:
            prev.append("%d:%s (%s)"%(penis.rank, user.name, self.num2short(penis.penis)))
        reply="Loose cunts: " + ", ".join(prev)
        message.reply(reply)
