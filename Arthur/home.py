from django.template import RequestContext
from django.template.loader import render_to_string

def index(request):
    planet = request.session.user.planet
    request.response.write(render_to_string("index.tpl", {"planet": planet}, RequestContext(request)))
    return request.response
