from Arthur.auth import render

def index(request):
    planet = request.session.user.planet
    ph = planet.midnight()
    return render("index.tpl", request, planet=planet, ph=ph)
