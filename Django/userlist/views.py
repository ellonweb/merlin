# Create your views here.
from django.http import HttpResponse
from Core.modules import M

def index(request):
    session = M.DB.Session()
    Q = session.query(M.DB.Maps.User)
    users = Q.all()
    return HttpResponse(str(users))
