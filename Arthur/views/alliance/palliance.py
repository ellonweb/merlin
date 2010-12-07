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
from sqlalchemy.sql import asc, desc
from Core.config import Config
from Core.paconf import PA
from Core.db import session
from Core.maps import Alliance, Planet, Alliance, Intel
from Arthur.context import render
from Arthur.loadable import loadable, load

@load
class alliance(loadable):
    access = Config.get("Arthur", "intel")
    def execute(self, request, user, name, page="1", sort="score", race="all"):
        page = int(page)
        offset = (page - 1)*50
        order =  {"score" : (asc(Planet.score_rank),),
                  "value" : (asc(Planet.value_rank),),
                  "size"  : (asc(Planet.size_rank),),
                  "xp"    : (asc(Planet.xp_rank),),
                  "ratio" : (desc(Planet.ratio),),
                  "race"  : (asc(Planet.race), asc(Planet.size_rank),),
                  "xyz"   : (asc(Planet.x), asc(Planet.y), asc(Planet.z),),
                  "score_growth" : (desc(Planet.score_growth),),
                  "value_growth" : (desc(Planet.value_growth),),
                  "size_growth"  : (desc(Planet.size_growth),),
                  "xp_growth"    : (desc(Planet.xp_growth),),
                  "score_growth_pc" : (desc(Planet.score_growth_pc),),
                  "value_growth_pc" : (desc(Planet.value_growth_pc),),
                  "size_growth_pc"  : (desc(Planet.size_growth_pc),),
                  "xp_growth_pc"    : (desc(Planet.xp_growth_pc),),
                  }
        if sort not in order.keys():
            sort = "score"
        order = order.get(sort)
        
        alliance = Alliance.load(name)
        if alliance is None:
            return HttpResponseRedirect(reverse("alliance_ranks"))
        
        Q = session.query(Planet, Intel.nick, Alliance.name)
        Q = Q.join(Planet.intel)
        Q = Q.join(Intel.alliance)
        Q = Q.filter(Planet.active == True)
        Q = Q.filter(Intel.alliance == alliance)
        
        if race.lower() in PA.options("races"):
            Q = Q.filter(Planet.race.ilike(race))
        else:
            race = "all"
        
        count = Q.count()
        pages = count/50 + int(count%50 > 0)
        pages = range(1, 1+pages)
        
        for o in order:
            Q = Q.order_by(o)
        Q = Q.limit(50).offset(offset)
        return render("palliance.tpl", request, alliance=alliance, planets=Q.all(), offset=offset, pages=pages, page=page, sort=sort, race=race)
