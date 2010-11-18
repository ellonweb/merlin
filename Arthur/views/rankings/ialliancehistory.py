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
from sqlalchemy import and_
from sqlalchemy.orm import aliased
from sqlalchemy.sql import asc, desc, case, literal_column
from sqlalchemy.sql.functions import count, sum
from Core.config import Config
from Core.db import session
from Core.maps import Planet, PlanetHistory, Alliance, Intel
from Arthur.context import render
from Arthur.loadable import loadable, load

@load
class ialliancehistory(loadable):
    access = Config.get("Arthur", "intel")
    def execute(self, request, user, name):
        alliance = Alliance.load(name)
        if alliance is None:
            return HttpResponseRedirect(reverse("alliance_ranks"))
        
        ph = aliased(PlanetHistory)
        members = count().label("members")
        size = sum(ph.size).label("size")
        value = sum(ph.value).label("value")
        score = sum(ph.score).label("score")
        avg_size = size.op("/")(members).label("avg_size")
        avg_value = value.op("/")(members).label("avg_value")
        t10v = count(case(whens=((ph.value_rank <= 10 ,1),), else_=None)).label("t10v")
        t100v = count(case(whens=((ph.value_rank <= 100 ,1),), else_=None)).label("t100v")
        
        pho = aliased(PlanetHistory)
        sizeo = sum(pho.size).label("sizeo")
        valueo = sum(pho.value).label("valueo")
        scoreo = sum(pho.score).label("scoreo")
        
        Q = session.query(PlanetHistory.tick.label("tick"),
                          Alliance.id.label("id"),
                          literal_column("rank() OVER (PARTITION BY planet_history.tick ORDER BY sum(planet_history.size) DESC)").label("size_rank"),
                          literal_column("rank() OVER (PARTITION BY planet_history.tick ORDER BY sum(planet_history.value) DESC)").label("value_rank"),
                          )
        Q = Q.join(PlanetHistory.current)
        Q = Q.join(Planet.intel)
        Q = Q.join(Intel.alliance)
        Q = Q.group_by(PlanetHistory.tick, Alliance.id)
        ranks = Q.subquery()
        
        Q = session.query(ph.tick, members,
                          size, value,
                          avg_size, avg_value,
                          size-sizeo, value-valueo, score-scoreo,
                          t10v, t100v,
                          )
        Q = Q.join(ph.current)
        Q = Q.join(Planet.intel)
        Q = Q.join(Intel.alliance)
        Q = Q.outerjoin((pho, and_(ph.id==pho.id, ph.tick-1==pho.tick),))
        Q = Q.filter(Intel.alliance == alliance)
        Q = Q.group_by(ph.tick)
        
        Q = Q.from_self().add_columns(ranks.c.size_rank, ranks.c.value_rank)
        Q = Q.outerjoin((ranks, and_(ph.tick == ranks.c.tick, alliance.id == ranks.c.id),))
        Q = Q.order_by(desc(ph.tick))
        
        history = Q.all()
        
        members = history[0][1] if len(history) else 0
        
        return render("ialliancehistory.tpl", request, alliance=alliance, members=members, history=history)
