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
from Arthur.views.planet import planets

urlpatterns = patterns('Arthur.views.planet',
    url(r'^planets/$', 'planets.planets', name="planet_ranks"),
    url(r'^planets/(?P<page>\d+)/$', 'planets.planets'),
    url(r'^planets/(?P<sort>\w+)/$', 'planets.planets'),
    url(r'^planets/(?P<sort>\w+)/(?P<page>\d+)/$', 'planets.planets'),
    url(r'^planets/(?P<race>\w+)/(?P<sort>\w+)/$', 'planets.planets'),
    url(r'^planets/(?P<race>\w+)/(?P<sort>\w+)/(?P<page>\d+)/$', 'planets.planets', name="planets"),
    ## change iplanet to planet once implemented in line below
    url(r'^planet/(?P<x>\d+)[. :\-](?P<y>\d+)[. :\-](?P<z>\d+)/$', 'iplanet.planet', name="planet"),
    url(r'^planet/(?P<x>\d+)[. :\-](?P<y>\d+)[. :\-](?P<z>\d+)/intel/$', 'iplanet.planet', name="iplanet"),
    url(r'^planet/(?P<x>\d+)[. :\-](?P<y>\d+)[. :\-](?P<z>\d+)/(?:intel/)?fleets/$', 'iplanet.planet', {'fleets':True}, name="fplanet"),
)
