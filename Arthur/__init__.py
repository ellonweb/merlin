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

handler404 = 'Arthur.errors.page_not_found'
handler500 = 'Arthur.errors.server_error'

urlpatterns = patterns('',
    (r'^login/', 'Arthur.login'),
    (r'^(?:home|logout)?/?$', 'Arthur.overview.home'),
    (r'', include('Arthur.dashboard')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'F:/Code/Git/merlin/Arthur/static/'}),
    (r'^guide/$', 'Arthur.guide'),
    (r'^links/(?P<link>[^/]+)/$', 'Arthur.links'),
    (r'^lookup/$', 'Arthur.lookup.lookup'),
    (r'', include('Arthur.alliance')),
    (r'', include('Arthur.rankings')),
    (r'', include('Arthur.attack')),
    (r'^scans/', include('Arthur.scans')),
    (r'^(?:scans/)?request/', include('Arthur.scans.request')),
    (r'^search/$', 'Arthur.search.search'),
    (r'^search/(?P<params>.*)/$', 'Arthur.search.search'),
)

@load
@require_user
class login(loadable):
    def execute(self, request, user):
        from Arthur.dashboard import dashboard
        if user.is_member():
            return dashboard.execute(request, user, dashuser=user)
        else:
            return home.execute(request, user)

from Arthur.overview import home

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

from Arthur import dashboard
from Arthur import alliance
from Arthur import rankings
from Arthur import search
from Arthur import attack
from Arthur import scans
