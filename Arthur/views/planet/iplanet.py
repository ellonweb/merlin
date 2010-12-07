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
from Core.db import session
from Core.maps import Updates, Planet, Alliance, Intel, FleetScan
from Arthur.context import render
from Arthur.loadable import loadable, load

@load
class planet(loadable):
    access = "member"
    def execute(self, request, user, x, y, z, fleets=False):
        week = Updates.week_tick()
        
        planet = Planet.load(x,y,z)
        if planet is None:
            return HttpResponseRedirect(reverse("planet_ranks"))
        
        Q = session.query(FleetScan, Planet, Alliance)
        Q = Q.join(FleetScan.target)
        Q = Q.outerjoin(Planet.intel).outerjoin(Intel.alliance)
        Q = Q.filter(FleetScan.owner == planet)
        Q = Q.order_by(desc(FleetScan.landing_tick))
        if not fleets:
            Q = Q.filter(FleetScan.landing_tick >= week)
        outgoing = Q.all()
        
        Q = session.query(FleetScan, Planet, Alliance)
        Q = Q.join(FleetScan.owner)
        Q = Q.outerjoin(Planet.intel).outerjoin(Intel.alliance)
        Q = Q.filter(FleetScan.target == planet)
        Q = Q.order_by(desc(FleetScan.landing_tick))
        if not fleets:
            Q = Q.filter(FleetScan.landing_tick >= week)
        incoming = Q.all()
        
        scan = planet.scan("A") or planet.scan("U")
        
        return render("iplanet.tpl", request, planet=planet, scan=scan, outgoing=outgoing, incoming=incoming)
