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
from django.conf.urls.defaults import include, patterns, url
from django.http import HttpResponseRedirect
from Core.maps import Alliance
from Arthur.loadable import loadable, load

urlpatterns = patterns('Arthur.lookup',
    url(r'^lookup/$', 'lookup'),
)

@load
class lookup(loadable):
    coord = re.compile(r"(\d+)([. :\-])(\d+)(\2(\d+))?")
    def execute(self, request, user):
        lookup = request.REQUEST.get("lookup") or ""
        m = self.coord.match(lookup)
        
        if m is None:
            alliance = Alliance.load(lookup) if lookup else None
            if alliance:
                return HttpResponseRedirect("/alliance/%s/" %(alliance.name,))
            else:
                return HttpResponseRedirect("/alliances/")
        
        elif m.group(5) is not None:
            return HttpResponseRedirect("/planet/%s:%s:%s/" %m.group(1,3,5))
        
        elif m.group(3) is not None:
            return HttpResponseRedirect("/galaxy/%s:%s/" %m.group(1,3))
        
        return HttpResponseRedirect("/home/")
