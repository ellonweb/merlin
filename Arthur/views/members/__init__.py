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
from Arthur.views.members import members, equeens

urlpatterns = patterns('Arthur.views.members',
    url(r'^members/$', 'members.members', name="memberlist"),
    url(r'^members/(?P<sort>\w+)/$', 'members.members', name="members"),
    url(r'^galmates/$', 'members.galmates'),
    url(r'^galmates/(?P<sort>\w+)/$', 'members.galmates', name="galmates"),
    url(r'^channels/$', 'members.channels'),
    url(r'^channels/(?P<sort>\w+)/$', 'members.channels', name="channels"),
    url(r'^equeens/$', 'equeens.equeens'),
)
