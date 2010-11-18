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
from django.http import HttpResponseRedirect
from sqlalchemy import or_
from sqlalchemy.sql import asc, desc

from Core.config import Config
from Core.paconf import PA
from Core.db import session
from Core.maps import Galaxy, Planet, Alliance, Intel
from Arthur.context import menu, render
from Arthur.loadable import loadable, load

urlpatterns = patterns('Arthur.views.search',
    (r'^search/$', 'search'),
    (r'^search/(?P<params>.*)/$', 'search'),
)

@menu("Search")
@load
class search(loadable):
    def execute(self, request, user, params=""):
        
        Q = session.query(Planet, Intel.nick, Alliance.name)
        Q = Q.outerjoin(Planet.intel)
        Q = Q.outerjoin(Intel.alliance)
        Q = Q.join(Planet.galaxy)
        Q = Q.filter(Planet.active == True)
        
        query = False
        
        page = 1
        
        search = {
                    "ruler" : "", "planet" : "", "galaxy" : "", "nick" : "", "alliance" : "",
                    "ter" : 'checked="checked"', "cat" : 'checked="checked"', "xan" : 'checked="checked"', "zik" : 'checked="checked"', "etd" : 'checked="checked"',
                    "sizemin" : "", "sizemax" : "", "valuemin" : "", "valuemax" : "", "scoremin" : "", "scoremax" : "", "x" : "",
                    "galsizemin" : "", "galsizemax" : "", "galvaluemin" : "", "galvaluemax" : "", "galscoremin" : "", "galscoremax" : "", "planets" : "",
                    "bash" : "" if params else 'checked="checked"',
                    "rankmin" : "", "rankmax" : "", "galrankmin" : "", "galrankmax" : "",
                    "ratiomin" : "", "ratiomax" : "", "galratiomin" : "", "galratiomax" : "",
                    "order1" : "", "order1o" : "", "order2" : "", "order2o" : "",
                 }
        
        intfilts = {
                    "score" : Planet.score,
                    "value" : Planet.value,
                    "size" : Planet.size,
                    "xp" : Planet.xp,
                    "galscore" : Galaxy.score,
                    "galvalue" : Galaxy.value,
                    "galsize" : Galaxy.size,
                    "galxp" : Galaxy.xp,
#                    "idle" : Planet.idle,
                    "x" : Planet.x,
                    "y" : Planet.y,
                    "planets" : Galaxy.members,
                    "totalroundroids" : Planet.totalroundroids,
                    "totallostroids" : Planet.totallostroids,
                    "ticksroiding" : Planet.ticksroiding,
                    "ticksroided" : Planet.ticksroided,
                    "tickroids" : Planet.tickroids,
                    }
        
        floatfilts = {
                    "ratio" : Planet.ratio,
                    "galratio" : Galaxy.ratio,
                    "avroids" : Planet.avroids,
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
        
        filters = {}
        filters.update(intfilts)
        filters.update(floatfilts)
        filters.update(rankfilts)
        
        order = {
                    "xyz"   : (Planet.x, Planet.y, Planet.z,),
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
        
        order.update(filters)
        orders = []
        
        wordfilts = {
                    "ruler" : Planet.rulername,
                    "planet" : Planet.planetname,
                    "galaxy" : Galaxy.name,
                    }
        
        if request.REQUEST.get("search"):
            r = request.REQUEST
            search = "/search/"
            
            for word in wordfilts.keys() + ["nick", "alliance"]:
                filt = (r.get(word) or "").strip()
                if not filt:
                    continue
                search += "%s:%s/" %(word,filt,)
            
            for filt in filters.keys():
                one = (r.get("min"+filt) or "").strip()
                two = (r.get("max"+filt) or "").strip()
                if not one and not two:
                    continue
                
                if one and one == two:
                    search += "%s:%s/" %(filt,one,)
                elif one and not two:
                    search += "%s:%s|/" %(filt,one,)
                elif two and not one:
                    search += "%s:|%s/" %(filt,two,)
                elif one and two:
                    search += "%s:%s|%s/" %(filt,one,two,)
            
            races = []
            for race in PA.options("races"):
                if (r.get(race) or "").strip():
                    races.append(race)
            if len(races) != len(PA.options("races")):
                search += "race:%s/" %("|".join(races),)
            
            if (r.get("bash") or "").strip():
                search += "bash/"
            
            o1 = (r.get("order1") or "").strip()
            o1o = (r.get("order1o") or "").strip()
            o2 = (r.get("order2") or "").strip()
            o2o = (r.get("order2o") or "").strip()
            if o1 not in order:
                o1, o1o = o2, o2o
            if o1 in order and (o1 == o2 or o2 not in order):
                if o1 == "score" and o1o == "desc":
                    pass
                else:
                    o1o = "^" if o1o == "asc" else "_"
                    search += "order:%s%s/" %(o1o,o1,)
            elif o1 in order and o2 in order:
                o1o = "^" if o1o == "asc" else "_"
                o2o = "^" if o2o == "asc" else "_"
                search += "order:%s%s|%s%s/" %(o1o,o1,o2o,o2,)
            
            return HttpResponseRedirect(search)
        
        for param in params.lower().split("/"):
            if param == "bash" and user.planet is not None:
                Q = Q.filter(or_(Planet.value.op(">")(user.planet.value*PA.getfloat("bash","value")),
                                 Planet.score.op(">")(user.planet.score*PA.getfloat("bash","score"))))
                search[param] = 'checked="checked"'
                continue
            
            if ":" not in param:
                continue
            arg, val = param.split(":",1)
            
            if arg in filters:
                one, two = "", ""
                if "|" not in val:
                    one, two = val, val
                elif val[-1] == "|":
                    one, two = val[:-1], ""
                elif val[0] == "|":
                    one, two = "", val[1:]
                elif "|" in val:
                    one, two = val.split("|",1)
                else:
                    continue
                
                try:
                    if one:
                        one = float(one) if arg in floatfilts else int(one)
                    if two:
                        two = float(two) if arg in floatfilts else int(two)
                except ValueError:
                    continue
                
                if one and one == two:
                    Q = Q.filter(filters[arg] == one)
                elif one and not two:
                    Q = Q.filter(filters[arg] <= one) if arg in rankfilts else Q.filter(filters[arg] >= one)
                elif two and not one:
                    Q = Q.filter(filters[arg] >= two) if arg in rankfilts else Q.filter(filters[arg] <= two)
                elif one and two:
                    Q = Q.filter(filters[arg].between(min(one,two), max(one,two)))
                else:
                    continue
                
                search[arg+"min"], search[arg+"max"] = one, two
                query = True
            
            elif arg in wordfilts:
                Q = Q.filter(wordfilts[arg].ilike("%"+val+"%"))
                search[arg] = val
                query = True
            
            elif arg == "nick" and getattr(user, "is_" + Config.get("Arthur", "intel"))():
                Q = Q.filter(Intel.nick.ilike("%"+val+"%"))
                search["nick"] = val
                query = True
            
            elif arg == "alliance" and getattr(user, "is_" + Config.get("Arthur", "intel"))():
                if val[0] == "!":
                    val = val[1:]
                    inv = True
                else:
                    inv = False
                alliance = Alliance.load(val)
                if alliance:
                    Q = Q.filter(Intel.alliance == alliance) if not inv else Q.filter(Intel.alliance != alliance)
                    search["alliance"] = ["","!"][inv] + alliance.name
                    query = True
            
            elif arg == "race":
                races = []
                for race in val.split("|"):
                    if race in PA.options("races") and race not in races:
                        races.append(Planet.race.ilike(race))
                        search[race] = True
                if len(races):
                    Q = Q.filter(or_(*races))
                    for race in PA.options("races"):
                        search[race] = 'checked="checked"' if search[race] is True else ""
                    query = True
            
            elif arg == "order":
                for sort in val.split("|"):
                    if sort[0] == "^":
                        f = asc
                    elif sort[0] == "_":
                        f = desc
                    else:
                        continue
                    if sort[1:] in order:
                        orders.append((f, sort[1:],))
                        query = True
            
            elif arg == "page" and val.isdigit():
                page = int(val)
        
        if len(orders) < 1:
            orders.append((desc, "score",))
        if len(orders) < 2:
            orders.append((desc, "score",))
        search["order1"] = orders[0][1]
        search["order1o"] = orders[0][0].__name__
        search["order2"] = orders[1][1]
        search["order2o"] = orders[1][0].__name__
        for d, os in orders:
            if type(order[os]) is tuple:
                for o in order[os]:
                    Q = Q.order_by(d(o))
            else:
                Q = Q.order_by(d(order[os]))
        
        showsort = True if search["order1"] not in ("xyz","size","value","score","ratio","xp",
                                                    "size_growth","value_growth","score_growth",
                                                    "size_growth_pc","value_growth_pc","score_growth_pc",) else False
        
        count = Q.count()
        pages = count/50 + int(count%50 > 0)
        pages = range(1, 1+pages)
        
        offset = (page - 1)*50
        Q = Q.limit(50).offset(offset)
        
        results = Q.all() if query else None
        
        return render("search.tpl", request, planets=results, sort=search["order1"],
                                showsort=showsort, s=search, params=params,
                                offset=offset, pages=pages, page=page)
