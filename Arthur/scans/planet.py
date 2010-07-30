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
from sqlalchemy.sql import asc, desc
from Core.paconf import PA
from Core.db import session
from Core.maps import Updates, Planet, Scan
from Arthur.context import render
from Arthur.loadable import loadable, load

@load
class planet(loadable):
    access = "half"
    
    def execute(self, request, user, x, y, z):
        tick = Updates.midnight_tick()
        
        planet = Planet.load(x,y,z)
        if planet is None:
            return HttpResponseRedirect(reverse("planet_ranks"))
        ph = planet.history(tick)
        
        Q = session.query(Scan)
        Q = Q.filter(Scan.planet == planet)
        Q = Q.order_by(desc(Scan.tick), asc(Scan.scantype))
        result = Q.all()
        
        group = []
        for scan in result:
            if len(group) < 1 or group[-1][0] != scan.tick:
                group.append((scan.tick, [scan],))
            else:
                group[-1][1].append(scan)
        
        return render("scans/planet.tpl", request, planet=planet, ph=ph, group=group)

@load
class id(loadable):
    access = "half"
    
    def execute(self, request, user, tick, id):
        Q = session.query(Scan)
        Q = Q.filter(Scan.tick == tick)
        Q = Q.filter(Scan.pa_id.ilike("%"+id+"%"))
        Q = Q.order_by(desc(Scan.id))
        scan = Q.first()
        if scan is None:
            return HttpResponseRedirect(reverse("scans"))
        
        return render("scans/base.tpl", request, scan=scan)

@load
class scan(loadable):
    access = "half"
    
    def execute(self, request, user, x, y, z, type):
        planet = Planet.load(x,y,z)
        if planet is None:
            return HttpResponseRedirect(reverse("planet_ranks"))
        
        scan = planet.scan(type)
        if scan is None:
            return HttpResponseRedirect(reverse("planet_scans", kwargs={"x":planet.x, "y":planet.y, "z":planet.z}))
        
        return render("scans/base.tpl", request, scan=scan)

@load
class types(loadable):
    access = "half"
    
    def execute(self, request, user, x, y, z, types):
        types = types.upper()
        
        planet = Planet.load(x,y,z)
        if planet is None:
            return HttpResponseRedirect(reverse("planet_ranks"))
        
        group = [(planet, [],)]
        scans = []
        for type in Scan._scan_types:
            if type in types:
                group[-1][1].append(planet.scan(type))
                scans.append(planet.scan(type))
        
        return render("scans/planet_types.tpl", request, planet=planet, group=group, scans=scans)
