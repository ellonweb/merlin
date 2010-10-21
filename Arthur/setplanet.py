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
 
from datetime import datetime, timedelta
import re
from Core.config import Config
from Core.db import session
from Core.maps import Planet, Alliance, Intel
from Arthur.loadable import loadable, load, PLANET_KEY

@load
class setplanet(loadable):
    coord = re.compile(r"(\d+)([. :\-])(\d+)(\2(\d+))")
    def execute(self, request, user):
        from Arthur.overview import home
        
        lookup = (request.REQUEST.get("coords") or "").strip()
        if not lookup:
            return home.execute(request, user)
        
        m = self.coord.match(lookup)
        if m is None:
            return home.execute(request, user, setplanet="Invalid coords")
        
        planet = Planet.load(*m.group(1,3,5))
        if planet is None:
            return home.execute(request, user, setplanet="No planet with coords %s:%s:%s" %m.group(1,3,5))
        
        if self.is_user(user):
            user.planet = planet
            if user.is_member():
                alliance = Alliance.load(Config.get("Alliance","name"))
                if planet.intel is None:
                    planet.intel = Intel(nick=user.name, alliance=alliance)
                else:
                    planet.intel.nick = user.name
                    planet.intel.alliance = alliance
            session.commit()
        else:
            user.planet = planet
            session.expunge(user)
        
        response = home.execute(request, user)
        response.set_cookie(PLANET_KEY, planet.id, expires=datetime.now()+timedelta(days=65))
        return response

@load
class clearplanet(loadable):
    def execute(self, request, user):
        from Arthur.overview import home
        
        user.planet = None
        if self.is_user(user):
            session.commit()
        
        response = home.execute(request, user)
        response.delete_cookie(PLANET_KEY)
        return response
