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
 
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from sqlalchemy import or_
from sqlalchemy.sql import asc, desc
from Core.paconf import PA
from Core.db import session
from Core.maps import Updates, Galaxy, GalaxyHistory, Planet, Alliance, Intel
from Arthur.context import render
from Arthur.loadable import loadable, load

@load
class galaxy(loadable):
    def execute(self, request, user, x, y, h=False, hs=False, ticks=None):
        galaxy = Galaxy.load(x,y)
        if galaxy is None:
            return HttpResponseRedirect(reverse("galaxy_ranks"))
        
        ticks = int(ticks or 0) if (h or hs) else 12
        
        if not (h or hs):
            Q = session.query(Planet, Intel.nick, Alliance.name)
            Q = Q.outerjoin(Planet.intel)
            Q = Q.outerjoin(Intel.alliance)
            Q = Q.filter(Planet.active == True)
            Q = Q.filter(Planet.galaxy == galaxy)
            Q = Q.order_by(asc(Planet.z))
            planets = Q.all()
            exiles = galaxy.exiles[:10]
        else:
            planets, exiles = None, None
        
        if not hs:
            sizediffvalue = GalaxyHistory.rdiff * PA.getint("numbers", "roid_value")
            valuediffwsizevalue = GalaxyHistory.vdiff - sizediffvalue
            resvalue = valuediffwsizevalue * PA.getint("numbers", "res_value")
            shipvalue = valuediffwsizevalue * PA.getint("numbers", "ship_value")
            xpvalue = GalaxyHistory.xdiff * PA.getint("numbers", "xp_value")
            Q = session.query(GalaxyHistory,
                                sizediffvalue,
                                valuediffwsizevalue,
                                resvalue, shipvalue,
                                xpvalue,
                                )
            Q = Q.filter(GalaxyHistory.current == galaxy)
            Q = Q.order_by(desc(GalaxyHistory.tick))
            history = Q[:ticks] if ticks else Q.all()
        else:
            history = None
        
        if not h:
            Q = session.query(GalaxyHistory)
            Q = Q.filter(or_(GalaxyHistory.hour == 23, GalaxyHistory.tick == Updates.current_tick()))
            Q = Q.filter(GalaxyHistory.current == galaxy)
            Q = Q.order_by(desc(GalaxyHistory.tick))
            hsummary = Q.all() if hs else Q[:14]
        else:
            hsummary = None
        
        return render(["galaxy.tpl",["hgalaxy.tpl","hsgalaxy.tpl"][hs]][h or hs],
                        request,
                        galaxy = galaxy,
                        planets = planets,
                        exiles = exiles,
                        history = history,
                        hsummary = hsummary,
                        ticks = ticks,
                      )
