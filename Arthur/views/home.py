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

from sqlalchemy import and_
from sqlalchemy.sql import asc, desc

from Core.config import Config
from Core.db import session
from Core.maps import Updates, Galaxy, Planet, Alliance
from Arthur.context import menu, render
from Arthur.errors import page_not_found
from Arthur.loadable import loadable, load, require_user

bot = Config.get("Connection","nick")
name = Config.get("Alliance", "name")

urlpatterns = patterns('Arthur.views.home',
    (r'^(?:home|logout)?/?$', 'home'),
    (r'^login/', 'login'),
    (r'^guide/$', 'guide'),
    (r'^links/(?P<link>[^/]+)/$', 'links'),
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


@menu("Home")
@load
class home(loadable):
    def execute(self, request, user):
        
        planet, galaxy = (user.planet, user.planet.galaxy,) if user.planet else (Planet(), Galaxy(),)
        
        planets = session.query(Planet).filter(Planet.active == True)
        galaxies = session.query(Galaxy).filter(Galaxy.active == True)
        alliances = session.query(Alliance).filter(Alliance.active == True)
        
        dup = lambda l,o,c=True: l+[o] if o in session and c and o not in l else l
        
        return render("index.tpl", request,
                     topplanets = dup(planets.order_by(asc(Planet.score_rank))[:20], 
                                      planet),
                 roidingplanets = dup(planets.filter(Planet.size_growth > 0).order_by(desc(Planet.size_growth))[:5],
                                      planet, planet.size_growth > 0),
                  roidedplanets = dup(planets.filter(Planet.size_growth < 0).order_by(asc(Planet.size_growth))[:5],
                                      planet, planet.size_growth < 0),
                      xpplanets = dup(planets.filter(Planet.xp_growth > 0).order_by(desc(Planet.xp_growth))[:5],
                                      planet, planet.xp_growth > 0),
                  bashedplanets = dup(planets.filter(Planet.value_growth < 0).order_by(asc(Planet.value_growth))[:5],
                                      planet, planet.value_growth < 0),
                
                    topgalaxies = dup(galaxies.order_by(asc(Galaxy.score_rank))[:10],
                                      galaxy),
                roidinggalaxies = dup(galaxies.filter(Galaxy.size_growth > 0).order_by(desc(Galaxy.size_growth))[:5],
                                      galaxy, galaxy.size_growth > 0),
                 roidedgalaxies = dup(galaxies.filter(Galaxy.size_growth < 0).order_by(asc(Galaxy.size_growth))[:5],
                                      galaxy, galaxy.size_growth < 0),
                     xpgalaxies = dup(galaxies.filter(Galaxy.xp_growth > 0).order_by(desc(Galaxy.xp_growth))[:5],
                                      galaxy, galaxy.xp_growth > 0),
                 bashedgalaxies = dup(galaxies.filter(Galaxy.value_growth < 0).order_by(asc(Galaxy.value_growth))[:5],
                                      galaxy, galaxy.value_growth < 0),
                
                   topalliances =     alliances.order_by(asc(Alliance.score_rank))[:8],
                            )

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
