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
 
from django.conf.urls.defaults import include, patterns, url
from Core.paconf import PA
from Core.db import session
from Core.maps import Updates, Planet, Request
from Core.robocop import push
from Arthur.context import render
from Arthur.loadable import loadable, load

urlpatterns = patterns('Arthur.scans.request',
    url(r'^(?P<x>\d+)[. :\-](?P<y>\d+)[. :\-](?P<z>\d+)/(?P<scantype>['+"".join([type.lower() for type in PA.options("scans")])+'])/$', 'request', name="request_planet"),
)

@load
class request(loadable):
    access = "half"
    def execute(self, request, user, x, y, z, scantype):
        from Arthur.scans.list import scans
        tick = Updates.current_tick()
        
        planet = Planet.load(x,y,z)
        if planet is None:
            return scans.execute(request, user, message="No planet with coords %s:%s:%s" %(x,y,z,))
            
        scantype = scantype.upper()
        dists = planet.intel.dists if planet.intel else 0
        requestscan = Request(target=planet, scantype=scantype, dists=dists)
        user.requests.append(requestscan)
        session.commit()
        
        push("request", user_name=user.name, x=x,y=y,z=z, scan=scantype, dists=dists,request_id=requestscan.id)
        
        return scans.execute(request, user, message="Requested %s-scan on %s:%s:%s"%(scantype,planet.x, planet.y, planet.z), planet=planet)
