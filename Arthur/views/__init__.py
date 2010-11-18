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
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from Core.config import Config
from Core.maps import Updates
from Arthur.context import menu, render
from Arthur.errors import page_not_found
from Arthur.loadable import loadable, load, require_user
bot = Config.get("Connection","nick")
name = Config.get("Alliance", "name")

urlpatterns = patterns('Arthur.views',
    (r'^login/', 'login'),
    (r'^guide/$', 'guide'),
    (r'^links/(?P<link>[^/]+)/$', 'links'),
    (r'', include('Arthur.views.overview')),
    (r'', include('Arthur.views.lookup')),
    (r'', include('Arthur.views.dashboard')),
    (r'', include('Arthur.views.members')),
    (r'', include('Arthur.views.rankings')),
    (r'', include('Arthur.views.search')),
    (r'', include('Arthur.views.attack')),
    (r'', include('Arthur.views.scans')),
)

@load
@require_user
class login(loadable):
    def execute(self, request, user):
        from Arthur.views.dashboard import dashboard
        if user.is_member():
            return dashboard.execute(request, user, dashuser=user)
        else:
            return home.execute(request, user)

from Arthur.views.overview import home

@menu(name,          "Intel",       suffix = name)
@menu("Planetarion", "BCalc",       suffix = "bcalc")
@menu("Planetarion", "Forums",      suffix = "forums")
@menu("Planetarion", "Game",        suffix = "game")
@load
@require_user
class links(loadable):
    def execute(self, request, user, link):
        link = {
                "game"        : "http://game.planetarion.com",
                "forums"      : "http://pirate.planetarion.com",
                "sandmans"    : "http://sandmans.co.uk",
                "bcalc"       : "http://game.planetarion.com/bcalc.pl",
                name          : reverse("alliance_members", kwargs={"name":name}),
               }.get(link)
        if link is None:
            return page_not_found(request)
        return HttpResponseRedirect(link)

@menu(bot, "Guide to %s"%(Config.get("Connection","nick"),))
@load
@require_user
class guide(loadable):
    def execute(self, request, user):
        return render("guide.tpl", request, bot=Config.get("Connection","nick"), alliance=name)

from Arthur.views import dashboard
from Arthur.views import members
from Arthur.views import rankings
from Arthur.views import search
from Arthur.views import attack
from Arthur.views import scans
