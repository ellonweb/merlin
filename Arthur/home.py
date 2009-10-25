from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    planet = request.session.user.planet
    return render_to_response("index.tpl", {"planet": planet}, RequestContext(request))
