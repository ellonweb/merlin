# This file is part of Merlin.
# Merlin is the Copyright (C)2008-2009 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.

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
 
# Request a scan

import re
from Core.config import Config
from Core.paconf import PA
from Core.db import session
from Core.maps import Planet, Request
from Core.loadable import loadable

@loadable.module("member")
class request(loadable):
    """Request a scan"""
    usage = " <scantype> <x.y.z> [dists] | cancel <id>"
    paramre = (re.compile(r"\s+(cancel)\s+(\d+)", re.I),
               re.compile(r"\s+("+"|".join(PA.options("scans"))+r")\w*\s+"+loadable.planet_coordre.pattern+r"(?:\s+(\d+))?", re.I),
               )
    
    @loadable.require_user
    def execute(self, message, user, params):
        
        if params.group(1).lower() == "cancel":
            request = Request.load(params.group(2))
            return
        
        planet = Planet.load(*params.group(2,4,6))
        if planet is None:
            message.alert("No planet with coords %s:%s:%s" % params.group(2,4,6))
            return
        
        scan = params.group(1).upper()
        
        request = Request(target=planet, scantype=scan)
        request.dists = int(params.group(7) or 0)
        user.requests.append(request)
        session.commit()
        
        dists_intel = planet.intel.dists if planet.intel else 0
        dists_request = request.dists
        
        message.reply("Requested a %s Scan of %s:%s:%s. !request cancel %s to cancel the request." % (PA.get(scan, "name"), planet.x, planet.y, planet.z, request.id,))
        self.request(message, request.id, user.name, scan, planet.x, planet.y, planet.z, dists_intel, dists_request)
        return
    
    # @loadable.runcop
    # def robocop(self, message, params):
        # id = int(params.group(1))
        # name = params.group(2)
        # scan = params.group(3).upper()
        # x,y,z = params.group(4,5,6)
        # dists_intel, dists_request = params.group(7,8)
        # self.request(message, id, name, scan, x, y, z, dists_intel, dists_request)
    
    def request(self, message, id, name, scan, x,y,z, dists_intel, dists_request):
        scannerchan = Config.get("Channels", "scans") if "scans" in Config.options("Channels") else Config.get("Channels", "home")
        message.privmsg("[%s] %s requested a %s Scan of %s:%s:%s Dists(i:%s/r:%s) " % (id, name, PA.get(scan, "name"), x,y,z, dists_intel, dists_request,) + Config.get("URL", "reqscan") % (PA.get(scan, "type"),x,y,z,), scannerchan)
