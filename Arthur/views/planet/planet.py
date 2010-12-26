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
 
from datetime import timedelta
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from sqlalchemy import and_
from sqlalchemy.orm import aliased
from sqlalchemy.sql import desc
from sqlalchemy.sql.functions import sum
from Core.paconf import PA
from Core.db import session
from Core.maps import Updates, Planet, PlanetHistory
from Arthur.context import render
from Arthur.loadable import loadable, load

@load
class planet(loadable):
    def execute(self, request, user, x, y, z):
        planet = Planet.load(x,y,z)
        if planet is None:
            return HttpResponseRedirect(reverse("planet_ranks"))
        
        history = aliased(PlanetHistory)
        next = aliased(PlanetHistory)
        sizediff = history.size - next.size
        sizediffvalue = sizediff * PA.getint("numbers", "roid_value")
        valuediff = history.value - next.value
        valuediffwsizevalue = valuediff - sizediffvalue
        resvalue = valuediffwsizevalue * PA.getint("numbers", "res_value")
        shipvalue = valuediffwsizevalue * PA.getint("numbers", "ship_value")
        xpdiff = history.xp - next.xp
        xpvalue = xpdiff * PA.getint("numbers", "xp_value")
        scorediff = history.score - next.score
        Q = session.query(history, Updates.timestamp - timedelta(minutes=1),
                            next.score_rank,
                            sizediff, sizediffvalue,
                            valuediff, valuediffwsizevalue,
                            resvalue, shipvalue,
                            xpdiff, xpvalue,
                            scorediff
                            )
        Q = Q.join(Updates)
        Q = Q.outerjoin((next, and_(history.id==next.id, history.tick-1==next.tick)))
        Q = Q.filter(history.current == planet)
        Q = Q.order_by(desc(history.tick))
        history = Q[:12]
        
        return render("planet.tpl", request, planet=planet,
                                             history=history,
                                             )
