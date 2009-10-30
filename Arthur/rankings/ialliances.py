from sqlalchemy.sql import asc, desc
from sqlalchemy.sql.functions import count, sum
from Core.db import session
from Core.maps import Planet, Alliance, Intel
from Arthur.auth import render

def ialliances(request, page="1", sort="score"):
    page = int(page)
    offset = (page - 1)*50
    order =  {"score" : (desc("score"),),
              "value" : (desc("value"),),
              "size"  : (desc("size"),),
              "xp"    : (desc("xp"),),
              } 
    if sort not in order.keys():
        sort = "score"
    order = order.get(sort)
    
    Q = session.query(sum(Planet.value).label("value"), sum(Planet.score).label("score"),
                      sum(Planet.size).label("size"), sum(Planet.xp).label("xp"),
                      count(), Alliance.name)
    Q = Q.join(Planet.intel)
    Q = Q.join(Intel.alliance)
    Q = Q.filter(Planet.active == True)
    Q = Q.group_by(Alliance.id)
    
    count = Q.count()
    pages = count/50 + int(count%50 > 0)
    pages = range(1, 1+pages)
    
    for o in order:
        Q = Q.order_by(o)
    Q = Q.limit(50).offset(offset)
    return render("ialliances.tpl", request, alliances=Q.all(), title="Alliance listing (intel)", offset=offset, pages=pages, page=page, sort=sort)
