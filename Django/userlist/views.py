# Create your views here.
from django.http import HttpResponse
import Core.db as DB

def index(request):
    session = DB.Session()
    Q = session.query(DB.Maps.User.name)
    users = Q.all()
    session.close()
    return HttpResponse(str(users))
