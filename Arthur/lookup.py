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
 
import re
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from Core.db import session
from Core.maps import Planet, Alliance, User, Intel
from Hooks.scans.parser import scanre, scangrpre, parse
from Arthur.loadable import loadable, load

@load
class lookup(loadable):
    coord = re.compile(r"(\d+)([. :\-])(\d+)(\2(\d+))?")
    def execute(self, request, user):
        lookup = (request.REQUEST.get("lookup") or "").strip()
        if not lookup:
            if user.is_member():
                return HttpResponseRedirect(reverse("dashboard", kwargs={"username":user.name}))
            return HttpResponseRedirect("/")
        
        scans = scanre.findall(lookup)
        groups = scangrpre.findall(lookup)
        if len(scans) or len(groups):
            for url in scans:
                parse(user.id, "scan", url).start()
            for url in groups:
                parse(user.id, "group", url).start()
            
            return HttpResponseRedirect(reverse("scans"))
        
        m = self.coord.match(lookup)
        
        if m is None:
            alliance = Alliance.load(lookup) if lookup else None
            if alliance:
                return HttpResponseRedirect(reverse("alliance_members", kwargs={"name":alliance.name}))
            
            elif not user.is_member():
                return HttpResponseRedirect(reverse("alliance_ranks"))
            
            else:
                member = User.load(lookup, exact=False, access="member") if lookup else None
                if member:
                    return HttpResponseRedirect(reverse("dashboard", kwargs={"username":member.name}))
                
                else:
                    Q = session.query(Planet)
                    Q = Q.join(Planet.intel)
                    Q = Q.filter(Planet.active == True)
                    Q = Q.filter(Intel.nick.ilike(lookup+"%"))
                    planet = Q.first()
                    if planet:
                        return HttpResponseRedirect(reverse("planet", kwargs={"x":planet.x, "y":planet.y, "z":planet.z}))
                    
                    else:
                        return HttpResponseRedirect(reverse("alliance_ranks"))
        
        elif m.group(5) is not None:
            return HttpResponseRedirect(reverse("planet", kwargs={"x":m.group(1), "y":m.group(3), "z":m.group(5)}))
        
        elif m.group(3) is not None:
            return HttpResponseRedirect(reverse("galaxy", kwargs={"x":m.group(1), "y":m.group(3)}))
        
