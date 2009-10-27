from datetime import datetime
from Core.maps import Updates
from Arthur.auth import render

def index(request):
    planet = request.session.user.planet
    now = datetime.now()
    d1 = datetime(now.year, now.month, now.day, now.hour)
    d2 = datetime(now.year, now.month, now.day)
    hours = (d1-d2).seconds/60/60
    tick = Updates.current_tick() - hours
    ph = planet.history(tick)
    return render("index.tpl", request, planet=planet, ph=ph)
