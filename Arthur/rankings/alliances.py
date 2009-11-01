from datetime import datetime
from sqlalchemy.sql import asc, desc
from Core.db import session
from Core.maps import Updates, Alliance, AllianceHistory
from Arthur.auth import render

def alliances(request, page="1", sort="score"):
    page = int(page)
    offset = (page - 1)*50
    order =  {"score" : (asc(Alliance.score_rank),),
              "size"  : (asc(Alliance.size_rank),),
              "avg_score" : (asc(Alliance.score_avg_rank),),
              "avg_size"  : (asc(Alliance.size_avg_rank),),
              "members"   : (asc(Alliance.members_rank),),
              } 
    if sort not in order.keys():
        sort = "score"
    order = order.get(sort)
    
    now = datetime.now()
    d1 = datetime(now.year, now.month, now.day, now.hour)
    d2 = datetime(now.year, now.month, now.day)
    hours = (d1-d2).seconds/60/60
    tick = Updates.current_tick() - hours
    
    Q = session.query(Alliance, AllianceHistory)
    Q = Q.outerjoin(Alliance.history_loader)
    Q = Q.filter(Alliance.active == True)
    Q = Q.filter(AllianceHistory.tick == tick)
    
    count = Q.count()
    pages = count/50 + int(count%50 > 0)
    pages = range(1, 1+pages)
    
    for o in order:
        Q = Q.order_by(o)
    Q = Q.limit(50).offset(offset)
    return render("alliances.tpl", request, alliances=Q.all(), title="Alliance listing", offset=offset, pages=pages, page=page, sort=sort)
