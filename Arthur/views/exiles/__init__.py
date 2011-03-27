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
from Arthur.views.exiles import exiles

urlpatterns = patterns('Arthur.views.exiles',
    url(r'^exiles/$', 'exiles.exiles', name="exiles"),
    url(r'^exiles/through/(?P<x>\d+)[. :\-](?P<y>\d+)/$', 'exiles.galaxy', {'through':True}, name="galaxy_exiles"),
    url(r'^exiles/of/(?P<x>\d+)[. :\-](?P<y>\d+)[. :\-](?P<z>\d+)/$', 'exiles.planet', {'through':False}, name="planet_exiles"),
)
