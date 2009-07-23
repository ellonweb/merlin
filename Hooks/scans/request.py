# This file is part of Merlin.
 
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
 
# This work is Copyright (C)2008 of Robin K. Hansen, Elliot Rosemarine.
# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

# Request a scan

import re
from .variables import access, channels
from .Core.modules import M
loadable = M.loadable.loadable
from Hooks.scans import scans, requesturl

class request(loadable):
    """Request a scan"""
    
    def __init__(self):
        loadable.__init__(self)
        self.paramre = re.compile(r"\s("+"|".join(scans.keys())+r")\w*\s"+self.planet_coordre.pattern+r"(?:\s(\d+))?", re.I)
        self.robore = re.compile(r"\s(\d+)\s(\S+)\s("+"|".join(scans.keys())+r")\s"+self.planet_coordre.pattern+r"(\d+)(\d+)", re.I)
        self.usage += " scantype x.y.z [dists]"
    
    @loadable.run_with_access(access['member'])
    def execute(self, message, user, params):
        
        planet = M.DB.Maps.Planet.load(*params.group(2,3,4))
        if planet is None:
            message.alert("No planet with coords %s:%s:%s" % params.group(2,3,4))
            return
        
        scan = params.group(1).upper()
        
        session = M.DB.Session()
        session.add(user)
        
        request = M.DB.Maps.Request(target=planet, scantype=scan)
        request.dists = int(params.group(5) or 0)
        user.requests.append(request)
        session.commit()
        
        session.add(planet)
        dists_intel = planet.intel.dists if planet.intel else 0
        dists_request = request.dists
        session.close()
        
        message.reply("Requested a %s Scan of %s:%s:%s. !cancelscan %s to cancel the request." % (scans[scan]['name'], planet.x, planet.y, planet.z, request.id,))
        self.request(message, request.id, user.name, scan, planet.x, planet.y, planet.z, dists_intel, dists_request)
        return
    
    @loadable.runcop
    def robocop(self, message, params):
        id = int(params.group(1))
        name = params.group(2)
        scan = params.group(3).upper()
        x,y,z = params.group(4,5,6)
        dists_intel, dists_request = params.group(7,8)
        self.request(message, id, name, scan, x, y, z, dists_intel, dists_request)
    
    def request(self, message, id, name, scan, x,y,z, dists_intel, dists_request):
        message.privmsg("[%s] %s requested a %s Scan of %s:%s:%s Dists(i:%s/r:%s) " % (id, name, scans[scan]['name'], x,y,z, dists_intel, dists_request,) + requesturl % (scans[scan]['type'],x,y,z,), channels.get('scan', channels['private']))
