import datetime
from django.http import HttpResponse
from Core.config import Config
from Core.db import session
from Core.maps import Session

SESSION_KEY = "%sSESSID" % (Config.get("Alliance", "name")[:3].upper(),)
SUBMIT = "submit"
LOGOUT = "Logout"
LOGIN = "Login"
USER = "username"
PASS = "password"

class Authentication(object):
    def process_request(self, request):
        key = request.COOKIES.get(SESSION_KEY)
        if key:
            auth = Session.load(key, datetime.datetime.now())
            if auth is None:
                HttpResponse.delete_cookie(SESSION_KEY)
                return HttpResponse("login page session|None")
            if request.POST.get(SUBMIT) == LOGOUT:
                session.delete(auth)
                session.commit()
                HttpResponse.delete_cookie(SESSION_KEY)
                return HttpResponse("login page session|logout")
            request.session = auth
            return
        elif (request.POST.get(SUBMIT) == LOGIN and
              request.POST.get(USER) is not None and
              request.POST.get(PASS) is not None):
            user = User.load(name=request.POST.get(USER), passwd=request.POST.get(PASS))
            if user is None:
                HttpResponse.delete_cookie(SESSION_KEY)
                return HttpResponse("login page user|None")
            else:
                key = self.generate_key()
                auth = Session(key=key, expire=datetime.datetime.now()+datetime.timedelta(days=1))
                session.add(auth)
                session.commit()
                HttpResponse.set_cookie(SESSION_KEY, request.session.key)
                return
        else:
            return HttpResponse("login page session|fresh")
    
    def process_response(self, request, response):
        session.close()
        return response
    
    def process_exception(self, request, exception):
        session.close()
    
    def generate_key(self):
        return 1
