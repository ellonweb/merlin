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
from Core.config import Config
from Core.paconf import PA
from Core.maps import Galaxy, Scan
from Arthur.context import render
from Arthur.loadable import loadable, load

@load
class galaxy(loadable):
    access = Config.get("Arthur", "scans")
    
    def execute(self, request, user, x, y):
        galaxy = Galaxy.load(x,y)
        if galaxy is None:
            return HttpResponseRedirect(reverse("galaxy_ranks"))
        
        group = []
        scans = []
        for planet in galaxy.planets:
            if not planet.active:
                continue
            group.append((planet, [],))
            if planet.scan("P"):
                group[-1][1].append(planet.scan("P"))
                scans.append(planet.scan("P"))
            
            if planet.scan("D"):
                group[-1][1].append(planet.scan("D"))
                scans.append(planet.scan("D"))
            
            if planet.scan("A") or planet.scan("U"):
                group[-1][1].append(planet.scan("A") or planet.scan("U"))
                scans.append(planet.scan("A") or planet.scan("U"))
        
        return render("scans/galaxy.tpl", request, galaxy=galaxy, group=group, scans=scans)

@load
class types(loadable):
    access = Config.get("Arthur", "scans")
    
    def execute(self, request, user, x, y, types):
        types = types.upper()
        
        galaxy = Galaxy.load(x,y)
        if galaxy is None:
            return HttpResponseRedirect(reverse("galaxy_ranks"))
        
        group = []
        scans = []
        for planet in galaxy.planets:
            if not planet.active:
                continue
            group.append((planet, [],))
            
            for type in Scan._scan_types:
                if type in types:
                    group[-1][1].append(planet.scan(type))
                    scans.append(planet.scan(type))
        
        return render("scans/galaxy.tpl", request, galaxy=galaxy, group=group, scans=scans)
