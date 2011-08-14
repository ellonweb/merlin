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
from sqlalchemy import and_, or_
from sqlalchemy.sql import asc, desc
from Core.db import session
from Core.maps import Galaxy, Planet, PlanetExiles
from Arthur.context import menu, render
from Arthur.loadable import loadable, load

@menu("Tracker")
@load
class exiles(loadable):
    def execute(self, request, user, page="1"):
        Q = session.query(PlanetExiles)
        Q = Q.order_by(desc(PlanetExiles.tick),
                        asc(PlanetExiles.oldx), asc(PlanetExiles.oldy), asc(PlanetExiles.oldz),
                        asc(PlanetExiles.newx), asc(PlanetExiles.newy), asc(PlanetExiles.newz))
        
        page = int(page)
        offset = (page - 1)*50
        count = Q.count()
        pages = count/50 + int(count%50 > 0)
        pages = range(1, 1+pages)
        Q = Q.limit(50).offset(offset)
        
        return render("exiles.tpl",  request, exiles = Q.all(), offset=offset, pages=pages, page=page)

@load
class galaxy(loadable):
    def execute(self, request, user, x, y, through):
        galaxy = Galaxy.load(x,y)
        if galaxy is None:
            return HttpResponseRedirect(reverse("exiles"))
        
        if through:
            exiles = galaxy.exiles
        else:
            Q = session.query(PlanetExiles)
            Q = Q.join(PlanetExiles.planet)
            Q = Q.filter(and_(Planet.x == galaxy.x, Planet.y == galaxy.y))
            Q = Q.order_by(desc(PlanetExiles.tick))
            exiles = Q.all()
        
        return render("exiles.tpl", request, galaxy = galaxy, through = through, exiles = exiles)

@load
class planet(loadable):
    def execute(self, request, user, x, y, z, through):
        planet = Planet.load(x,y,z)
        if planet is None:
            return HttpResponseRedirect(reverse("exiles"))
        
        if through:
            Q = session.query(PlanetExiles)
            Q = Q.filter(or_(and_(PlanetExiles.oldx == planet.x, PlanetExiles.oldy == planet.y, PlanetExiles.oldz == planet.z),
                             and_(PlanetExiles.newx == planet.x, PlanetExiles.newy == planet.y, PlanetExiles.newz == planet.z)))
            Q = Q.order_by(desc(PlanetExiles.tick))
            exiles = Q.all()
        else:
            exiles = planet.exiles
        
        return render("exiles.tpl", request, planet = planet, through = through, exiles = exiles)
