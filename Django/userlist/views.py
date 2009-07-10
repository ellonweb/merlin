# Create your views here.
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import Core.db as DB

@login_required
def index(request):
    #user = 
    session = DB.Session()
    Q = session.query(DB.Maps.User)
    users = Q.all()
    return HttpResponse(str(users))
