from datetime import datetime
from django.http import HttpResponseRedirect
from sqlalchemy.sql import asc, desc
from Core.paconf import PA
from Core.db import session
from Core.maps import Updates, Galaxy, Planet, PlanetHistory, Alliance, Intel
from Arthur.auth import render

def galaxy(request, x, y):
    now = datetime.now()
    d1 = datetime(now.year, now.month, now.day, now.hour)
    d2 = datetime(now.year, now.month, now.day)
    hours = (d1-d2).seconds/60/60
    tick = Updates.current_tick() - hours
    
    galaxy = Galaxy.load(x,y)
    if galaxy is None:
        return HttpResponseRedirect("/galaxies/")
    gh = galaxy.history(tick)
    
    Q = session.query(Planet, PlanetHistory, Intel.nick, Alliance.name)
    Q = Q.outerjoin(Planet.intel)
    Q = Q.outerjoin(Intel.alliance)
    Q = Q.outerjoin(Planet.history_loader)
    Q = Q.filter(PlanetHistory.tick == tick)
    Q = Q.filter(Planet.galaxy == galaxy)
    Q = Q.order_by(asc(Planet.z))
    return render("planets.tpl", request, planets=Q.all(), title=galaxy.name, intel=True, galaxy=galaxy, gh=gh)
