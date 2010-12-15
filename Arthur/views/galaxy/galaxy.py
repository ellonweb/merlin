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
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from sqlalchemy.sql import asc, desc
from sqlalchemy.sql.functions import sum
from Core.db import session
from Core.maps import Galaxy, GalaxyHistory, Planet, PlanetExiles, Alliance, Intel
from Arthur.context import render
from Arthur.loadable import loadable, load

@load
class galaxy(loadable):
    def execute(self, request, user, x, y):
        
        galaxy = Galaxy.load(x,y)
        if galaxy is None:
            return HttpResponseRedirect(reverse("galaxy_ranks"))
        
        Q = session.query(Planet, Intel.nick, Alliance.name)
        Q = Q.outerjoin(Planet.intel)
        Q = Q.outerjoin(Intel.alliance)
        Q = Q.filter(Planet.active == True)
        Q = Q.filter(Planet.galaxy == galaxy)
        Q = Q.order_by(asc(Planet.z))
        planets = Q.all()
        
        high = aliased(GalaxyHistory)
        low = aliased(GalaxyHistory)
        Q = session.query(sum(Planet.totalroundroids).label("trr"),
                          sum(Planet.totallostroids).label("tlr"),
                          sum(Planet.ticksroiding).label("roiding"),
                          sum(Planet.ticksroided).label("roided"),
                          high.score_rank.label("highest"),
                          high.tick.label("hightick"),
                          low.score_rank.label("lowest"),
                          low.tick.label("lowtick"),
                          sum(Planet.xp).label("xp"),
                          sum(Planet.size).label("size"),
                          )
        Q = Q.join((Planet, Galaxy.planets))
        Q = Q.join((high, Galaxy.history_loader))
        Q = Q.join((low, Galaxy.history_loader))
        Q = Q.filter(Planet.active == True)
        Q = Q.filter(Planet.galaxy == galaxy)
        Q = Q.group_by(high.score_rank, high.tick, low.score_rank, low.tick)
        Q = Q.order_by(asc(high.score_rank), desc(high.tick), desc(low.score_rank), desc(low.tick))
        stats = Q.first()
        stats.exiles = len(galaxy.outs)
        
        Q = session.query(PlanetExiles)
        Q = Q.filter(or_(PlanetExiles.old == galaxy, PlanetExiles.new == galaxy))
        Q = Q.order_by(desc(PlanetExiles.tick))
        exiles = Q[:10]
        
        return render("galaxy.tpl", request, galaxy=galaxy,
                                             planets=planets,
                                             stats=stats,
                                             exiles=exiles,
                                             )
