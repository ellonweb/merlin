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
from Arthur.views.attack import attack

urlpatterns = patterns('Arthur.views.attack',
    url(r'^attack/$', 'attack.attack', name="attacks"),
    url(r'^attack/(?P<id>\d+)/$', 'attack.view', name="attack"),
    url(r'^(?:attack/)?(?:attack/(?P<id>\d+)/)?book/(?P<x>\d+)[. :\-](?P<y>\d+)[. :\-](?P<z>\d+)/(?P<when>\d+)/$', 'book.book', name="book"),
    url(r'^(?:attack/)?(?:attack/(?P<id>\d+)/)?unbook/(?P<x>\d+)[. :\-](?P<y>\d+)[. :\-](?P<z>\d+)/(?:(?P<when>\d+)/)?$', 'book.unbook', name="unbook"),
)
