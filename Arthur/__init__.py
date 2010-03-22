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
from Core.config import Config
from Core.maps import Updates
from Arthur.context import menu, render
from Arthur.loadable import loadable

handler404 = 'Arthur.errors.page_not_found'
handler500 = 'Arthur.errors.server_error'

urlpatterns = patterns('',
    (r'^(?:home/)?$', 'Arthur.home'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Code/git/merlin/Arthur/static/'}),
    (r'^guide/$', 'Arthur.guide'),
    (r'', include('Arthur.rankings')),
)

@menu("Home")
class home(loadable):
    def execute(self, request, user):
        if user.planet is not None:
            tick = Updates.midnight_tick()
            planets = (user.planet, user.planet.history(tick), None, None),
        else:
            planets = ()
        return render("index.tpl", request, planets=planets, title="Your planet")

@menu("Guide to %s"%(Config.get("Connection","nick"),))
class guide(loadable):
    def execute(self, request, user):
        return render("guide.tpl", request, bot=Config.get("Connection","nick"), alliance=Config.get("Alliance", "name"))

from Arthur import rankings
