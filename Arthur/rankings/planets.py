from datetime import datetime
from sqlalchemy.sql import asc, desc
from Core.paconf import PA
from Core.db import session
from Core.maps import Updates, Planet, PlanetHistory, Alliance, Intel
from Arthur.auth import render

def planets(request, page="1", sort="score", race="all"):
    page = int(page)
    offset = (page - 1)*50
    order =  {"score" : (asc(Planet.score_rank),),
              "value" : (asc(Planet.value_rank),),
              "size"  : (asc(Planet.size_rank),),
              "xp"    : (asc(Planet.xp_rank),),
              "race"  : (asc(Planet.race), asc(Planet.size_rank),),
              }
    if sort not in order.keys():
        sort = "score"
    order = order.get(sort)
    
    now = datetime.now()
    d1 = datetime(now.year, now.month, now.day, now.hour)
    d2 = datetime(now.year, now.month, now.day)
    hours = (d1-d2).seconds/60/60
    tick = Updates.current_tick() - hours
    
    Q = session.query(Planet, PlanetHistory, Intel.nick, Alliance.name)
    Q = Q.outerjoin(Planet.intel)
    Q = Q.outerjoin(Intel.alliance)
    Q = Q.outerjoin(Planet.history_loader)
    Q = Q.filter(PlanetHistory.tick == tick)
    
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
    return render("planets.tpl", request, planets=Q.all(), title="Planet listing", intel=True, offset=offset, pages=pages, page=page, sort=sort, race=race)
