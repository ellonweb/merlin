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
from Core.config import Config
from Core.db import session
from Core.maps import Updates, Planet, Scan, Request
from Arthur.context import menu, render
from Arthur.loadable import loadable, load

@menu("Scans")
@load
class scans(loadable):
    access = Config.get("Arthur", "scans")
    
    def execute(self, request, user, message=None, planet=None):
        tick = Updates.current_tick()
        
        Q = session.query(Request)
        Q = Q.filter(Request.user == user)
        Q = Q.filter(Request.tick > tick - 5)
        Q = Q.filter(Request.active == True)
        Q = Q.order_by(asc(Request.id))
        open = Q.all()
        
        Q = session.query(Scan)
        Q = Q.join(Request.scan)
        Q = Q.filter(Request.user == user)
        Q = Q.filter(Request.tick > tick - 24)
        Q = Q.filter(Request.scan != None)
        Q = Q.order_by(desc(Request.id))
        completed = Q.all()
        
        Q = session.query(Scan)
        Q = Q.filter(Scan.scanner == user)
        Q = Q.order_by(desc(Scan.id))
        scans = Q[:25]
        
        return render("scans/scans.tpl", request, types=Request._requestable, open=open, completed=completed, scans=scans, message=message, planet=planet)

@load
class group(loadable):
    access = Config.get("Arthur", "scans")
    
    def execute(self, request, user, id):
        Q = session.query(Planet, Scan)
        Q = Q.join(Scan.planet)
        Q = Q.filter(Scan.group_id.ilike("%"+id+"%"))
        Q = Q.order_by(asc(Planet.x), asc(Planet.y), asc(Planet.z), asc(Scan.scantype), asc(Scan.tick))
        result = Q.all()
        if len(result) == 0:
            return HttpResponseRedirect(reverse("scans"))
        
        group = []
        scans = []
        for planet, scan in result:
            if len(group) < 1 or group[-1][0] is not planet:
                group.append((planet, [scan],))
            else:
                group[-1][1].append(scan)
            scans.append(scan)
        
        return render("scans/group.tpl", request, group=group, scans=scans)

@load
class tick(loadable):
    access = Config.get("Arthur", "scans")
    
    def execute(self, request, user, tick):
        Q = session.query(Planet, Scan)
        Q = Q.join(Scan.planet)
        Q = Q.filter(Scan.tick == tick)
        Q = Q.order_by(asc(Planet.x), asc(Planet.y), asc(Planet.z), asc(Scan.scantype), asc(Scan.tick))
        result = Q.all()
        
        group = []
        for planet, scan in result:
            if len(group) < 1 or group[-1][0] is not planet:
                group.append((planet, [scan],))
            else:
                group[-1][1].append(scan)
        
        return render("scans/tick.tpl", request, tick=tick, group=group)
