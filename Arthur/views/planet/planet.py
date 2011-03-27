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
 
from datetime import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from sqlalchemy.sql import desc
from sqlalchemy.sql.functions import count
from Core.paconf import PA
from Core.db import session
from Core.maps import Planet, PlanetHistory, PlanetIdles, PlanetValueDrops, PlanetLandings, PlanetLandedOn
from Arthur.context import render
from Arthur.loadable import loadable, load

@load
class planet(loadable):
    def execute(self, request, user, x, y, z, h=False, ticks=None):
        planet = Planet.load(x,y,z)
        if planet is None:
            return HttpResponseRedirect(reverse("planet_ranks"))
        
        ticks = int(ticks or 0) if h else 12
        
        sizediffvalue = PlanetHistory.rdiff * PA.getint("numbers", "roid_value")
        valuediffwsizevalue = PlanetHistory.vdiff - sizediffvalue
        resvalue = valuediffwsizevalue * PA.getint("numbers", "res_value")
        shipvalue = valuediffwsizevalue * PA.getint("numbers", "ship_value")
        xpvalue = PlanetHistory.xdiff * PA.getint("numbers", "xp_value")
        Q = session.query(PlanetHistory,
                            sizediffvalue,
                            valuediffwsizevalue,
                            resvalue, shipvalue,
                            xpvalue,
                            )
        Q = Q.filter(PlanetHistory.current == planet)
        Q = Q.order_by(desc(PlanetHistory.tick))
        
        if not h:
            landings = session.query(PlanetLandings.hour, count()).filter(PlanetLandings.planet==planet).group_by(PlanetLandings.hour).all()
            landed = session.query(PlanetLandedOn.hour, count()).filter(PlanetLandedOn.planet==planet).group_by(PlanetLandedOn.hour).all()
            vdrops = session.query(PlanetValueDrops.hour, count()).filter(PlanetValueDrops.planet==planet).group_by(PlanetValueDrops.hour).all()
            idles = session.query(PlanetIdles.hour, count()).filter(PlanetIdles.planet==planet).group_by(PlanetIdles.hour).all()
            hourstats = {
                            'landings' : dict(landings), 'landingsT' : sum([c for hour,c in landings]),
                            'landed'   : dict(landed),   'landedT'   : sum([c for hour,c in landed]),
                            'vdrops'   : dict(vdrops),   'vdropsT'   : sum([c for hour,c in vdrops]),
                            'idles'    : dict(idles),    'idlesT'    : sum([c for hour,c in idles]),
                            }
        else:
            hourstats = None
        
        return render(["planet.tpl","hplanet.tpl"][h],
                        request,
                        planet = planet,
                        history = Q[:ticks] if ticks else Q.all(),
                        hour = datetime.utcnow().hour, hourstats = hourstats,
                        ticks = ticks,
                      )
