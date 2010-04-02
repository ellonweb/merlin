# This file is part of Merlin/Arthur.
# Merlin/Arthur is the Copyright (C)2009,2010 of Elliot Rosemarine.

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
 
from sqlalchemy.sql import asc, desc, case
from sqlalchemy.sql.functions import count, sum
from Core.config import Config
from Core.db import session
from Core.maps import Updates, Planet, User, PhoneFriend
from Arthur.context import menu, render
from Arthur.loadable import loadable, load

@menu(Config.get("Alliance", "name"), "Members", prefix = True)
@load
class members(loadable):
    access = "admin"
    def execute(self, request, user):
        
        levels = sorted(Config.items("Access"), key=lambda acc: int(acc[1]), reverse=True)
        
        members = []
        for level in levels:
            Q = session.query(User.name, User.alias, User.sponsor, Planet, User.fleetupdated,
                              User.phone, User.pubphone, User.id.in_(session.query(PhoneFriend.user_id).filter_by(friend=user)))
            Q = Q.outerjoin(User.planet)
            Q = Q.filter(User.access >= level[1])
            Q = Q.filter(User.access < levels[levels.index(level)-1][1]) if levels.index(level) > 0 else Q
            Q = Q.order_by(User.name)
            
            members.append((level[0], Q.all(),))
        
        return render("members.tpl", request, accesslist=members, tick=Updates.current_tick()*-1)
