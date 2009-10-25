from Arthur.auth import render

def index(request):
    planet = request.session.user.planet
    return render("index.tpl", request, planet=planet)
