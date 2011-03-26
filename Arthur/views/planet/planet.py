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
 
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from sqlalchemy.sql import desc
from Core.paconf import PA
from Core.db import session
from Core.maps import Planet, PlanetHistory
from Arthur.context import render
from Arthur.loadable import loadable, load

@load
class planet(loadable):
    def execute(self, request, user, x, y, z, h=False, ticks=None):
        planet = Planet.load(x,y,z)
        if planet is None:
            return HttpResponseRedirect(reverse("planet_ranks"))
        
        ticks = int(ticks or 0) if h else 12
        
        sizediffvalue = PlanetHistory.rdiff * PA.getint("numbers", "roid_value")
        valuediffwsizevalue = PlanetHistory.vdiff - sizediffvalue
        resvalue = valuediffwsizevalue * PA.getint("numbers", "res_value")
        shipvalue = valuediffwsizevalue * PA.getint("numbers", "ship_value")
        xpvalue = PlanetHistory.xdiff * PA.getint("numbers", "xp_value")
        Q = session.query(PlanetHistory,
                            sizediffvalue,
                            valuediffwsizevalue,
                            resvalue, shipvalue,
                            xpvalue,
                            )
        Q = Q.filter(PlanetHistory.current == planet)
        Q = Q.order_by(desc(PlanetHistory.tick))
        
        return render(["planet.tpl","hplanet.tpl"][h],
                        request,
                        planet = planet,
                        history = Q[:ticks] if ticks else Q.all(),
                        ticks = ticks,
                      )
