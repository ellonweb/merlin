# This file is part of Merlin/Arthur.
# Merlin/Arthur is the Copyright (C)2011 of Elliot Rosemarine.

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
from Core.config import Config

graphing = Config.get("Misc", "graphing") != "disabled"
caching  = Config.get("Misc", "graphing") == "cached"
if graphing:
    import matplotlib
    matplotlib.use('Agg')

urlpatterns = patterns('',
  url(r'^graphs/(?P<type>values|ranks)/', include(patterns('Arthur.views.graphs.graphs',
    url(r'^(?P<x>\d+)[. :\-](?P<y>\d+)[. :\-](?P<z>\d+)$', 'planet', name="planetG"),
    url(r'^(?P<x>\d+)[. :\-](?P<y>\d+)$', 'galaxy', name="galaxyG"),
    url(r'^(?P<name>[^/]+)$', 'alliance', name="allianceG"),
  ))),
) if graphing else ()

