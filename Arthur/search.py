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
 
from django.http import HttpResponseRedirect
from sqlalchemy import or_
from sqlalchemy.sql import asc, desc

from Core.config import Config
from Core.paconf import PA
from Core.db import session
from Core.maps import Galaxy, Planet, Alliance, Intel
from Arthur.context import menu, render
from Arthur.loadable import loadable, load

@menu("Search")
@load
class search(loadable):
    def execute(self, request, user, params):
        
        Q = session.query(Planet, Intel.nick, Alliance.name)
        Q = Q.outerjoin(Planet.intel)
        Q = Q.outerjoin(Intel.alliance)
        Q = Q.join(Planet.galaxy)
        Q = Q.filter(Planet.active == True)
        
        page = 1
        
        filters = {
                    "score" : Planet.score,
                    "value" : Planet.value,
                    "size" : Planet.size,
                    "xp" : Planet.xp,
                    "galscore" : Galaxy.score,
                    "galvalue" : Galaxy.value,
                    "galsize" : Galaxy.size,
                    "galxp" : Galaxy.xp,
                    "idle" : Planet.idle,
                    "x" : Planet.x,
                    "y" : Planet.y,
                    "planets" : Galaxy.members,
                    }
        
        rankfilts = {
                    "rank" : Planet.score_rank,
                    "valuerank" : Planet.value_rank,
                    "sizerank" : Planet.size_rank,
                    "xprank" : Planet.xp_rank,
                    "galrank" : Galaxy.score_rank,
                    "galvaluerank" : Galaxy.value_rank,
                    "galsizerank" : Galaxy.size_rank,
                    "galxprank" : Galaxy.xp_rank,
                    }
        
        orders = {
                    "score_growth" : Planet.score_growth,
                    "value_growth" : Planet.value_growth,
                    "size_growth"  : Planet.size_growth,
                    "xp_growth"    : Planet.xp_growth,
                    "score_growth_pc" : Planet.score_growth_pc,
                    "value_growth_pc" : Planet.value_growth_pc,
                    "size_growth_pc"  : Planet.size_growth_pc,
                    "xp_growth_pc"    : Planet.xp_growth_pc,
                    "galscore_growth" : Galaxy.score_growth,
                    "galvalue_growth" : Galaxy.value_growth,
                    "galsize_growth"  : Galaxy.size_growth,
                    "galxp_growth"    : Galaxy.xp_growth,
                    "galscore_growth_pc" : Galaxy.score_growth_pc,
                    "galvalue_growth_pc" : Galaxy.value_growth_pc,
                    "galsize_growth_pc"  : Galaxy.size_growth_pc,
                    "galxp_growth_pc"    : Galaxy.xp_growth_pc,
                    }
        
        wordfilts = {
                    "ruler" : Planet.rulername,
                    "planet" : Planet.planetname,
                    "galaxy" : Galaxy.name,
                    }
        
        for param in params.lower().split("/"):
            if ":" not in param:
                continue
            arg, val = param.split(":",1)
            if arg in filters:
                if "|" not in val and val.isdigit():
                    Q = Q.filter(filters[arg] == val)
                elif val[-1] == "|" and val[:-1].isdigit():
                    Q = Q.filter(filters[arg] >= val[:-1])
                elif val[0] == "|" and val[1:].isdigit():
                    Q = Q.filter(filters[arg] <= val[1:])
                else:
                    one, two = val.split("|",1)
                    if one.isdigit() and two.isdigit():
                        Q = Q.filter(filters[arg].between(min(one,two), max(one,two)))
            if arg in rankfilts:
                if "|" not in val and val.isdigit():
                    Q = Q.filter(rankfilts[arg] == val)
                elif val[-1] == "|" and val[:-1].isdigit():
                    Q = Q.filter(rankfilts[arg] <= val[:-1])
                elif val[0] == "|" and val[1:].isdigit():
                    Q = Q.filter(rankfilts[arg] >= val[1:])
                else:
                    one, two = val.split("|",1)
                    if one.isdigit() and two.isdigit():
                        Q = Q.filter(rankfilts[arg].between(min(one,two), max(one,two)))
            if arg in wordfilts:
                Q = Q.filter(wordfilts[arg].ilike("%"+val+"%"))
            if arg == "race":
                races = []
                for race in val.split("|"):
                    if race in PA.options("races") and race not in races:
                        races.append(Planet.race.ilike(race))
                if len(races):
                    Q = Q.filter(or_(*races))
            if arg == "order":
                for sort in val.split("|"):
                    if sort[0] == "^":
                        f = asc
                    elif sort[0] == "_":
                        f = desc
                    else:
                        continue
                    if sort[1:] in filters:
                        Q = Q.order_by(f(filters[sort[1:]]))
                    elif sort[1:] in rankfilts:
                        Q = Q.order_by(f(rankfilts[sort[1:]]))
                    elif sort[1:] in orders:
                        Q = Q.order_by(f(orders[sort[1:]]))
                    else:
                        continue
            if arg == "page" and val.isdigit():
                page = int(val)
            
        Q = Q.limit(50).offset((page - 1)*50)
        
        return render("planets.tpl", request, planets=Q.all())
