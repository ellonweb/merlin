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
 
from sqlalchemy.sql import asc
from Core.config import Config
from Core.db import session
from Core.maps import User, Planet, epenis
from Arthur.context import menu, render
from Arthur.loadable import loadable, load
name = Config.get("Alliance", "name")

@load
class equeens(loadable):
    access = "member"
    def execute(self, request, user):
        
        Q = session.query(User, Planet, epenis)
        Q = Q.join(User.planet)
        Q = Q.join(User.epenis)
        Q = Q.order_by(asc(epenis.rank))
        return render("equeens.tpl", request, queens=Q.all())
