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
 
from sqlalchemy import and_, or_
from sqlalchemy.orm import aliased
from Core.config import Config
from Core.db import session
from Core.maps import User
from Core.loadable import loadable, route

class orphans(loadable):
    """Lists all members whose sponsors are no longer members. Use !adopt to someone."""
    
    @route(access = "member")
    def execute(self, message, user, params):
        
        user = aliased(User)
        sponsor = aliased(User)
        Q = session.query(user.name)
        Q = Q.filter(and_(user.active == True, user.access >= Config.get("Access", "member")))
        Q = Q.filter(user.sponsor.ilike(sponsor.name))
        Q = Q.filter(or_(sponsor.active == False, sponsor.access < Config.get("Access", "member")))
        result = Q.all()
        
        if len(result) < 1:
            message.reply("There are no orphans. KILL A PARENT NOW.")
            return
        
        reply = "The following members are orphans: "
        reply+= ", ".join(map(lambda x:x[0],result))
        message.reply(reply)
