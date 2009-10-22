import datetime
import random
from django.http import HttpResponse
from Core.config import Config
from Core.db import session
from Core.maps import User, Session

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
                HttpResponse().delete_cookie(SESSION_KEY)
                return HttpResponse("login page session|None")
            if request.REQUEST.get(SUBMIT) == LOGOUT:
                session.delete(auth)
                session.commit()
                HttpResponse().delete_cookie(SESSION_KEY)
                return HttpResponse("login page session|logout")
            request.session = auth
            return
        elif (request.REQUEST.get(USER) is not None and request.REQUEST.get(PASS) is not None):
            user = User.load(name=request.REQUEST.get(USER), passwd=request.REQUEST.get(PASS))
            if user is None:
                HttpResponse().delete_cookie(SESSION_KEY)
                return HttpResponse("login page user|None")
            else:
                key = self.generate_key(user)
                auth = Session(key=key, expire=datetime.datetime.now()+datetime.timedelta(days=1))
                session.add(auth)
                session.commit()
                HttpResponse().set_cookie(SESSION_KEY, request.session.key)
                return
        else:
            return HttpResponse("login page session|fresh")
    
    def process_response(self, request, response):
        session.close()
        return response
    
    def process_exception(self, request, exception):
        session.close()
    
    def generate_key(self, user):
        return User.hasher(user.name+user.passwd+str(datetime.datetime.now())+str(random.randrange(1,1000000000)))
