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
        request.response = HttpResponse()
        key = request.COOKIES.get(SESSION_KEY)
        if key:
            auth = Session.load(key, datetime.datetime.now())
            if auth is None:
                request.response.delete_cookie(SESSION_KEY)
                request.response.write("login page session|None")
                return request.response
            if request.REQUEST.get(SUBMIT) == LOGOUT:
                session.delete(auth)
                session.commit()
                request.response.delete_cookie(SESSION_KEY)
                request.response.write("login page session|logout")
                return request.response
            request.session = auth
            return
        elif (request.REQUEST.get(USER) is not None and request.REQUEST.get(PASS) is not None):
            user = User.load(name=request.REQUEST.get(USER), passwd=request.REQUEST.get(PASS))
            if user is None:
                request.response.delete_cookie(SESSION_KEY)
                request.response.write("login page user|None")
                return request.response
            else:
                key = self.generate_key(user)
                auth = Session(key=key, expire=datetime.datetime.now()+datetime.timedelta(days=1), user=user)
                session.add(auth)
                session.commit()
                request.session = auth
                request.response.set_cookie(SESSION_KEY, request.session.key)
                return
        else:
            request.response.write("login page session|fresh")
            return request.response
    
    def process_response(self, request, response):
        session.close()
        return request.response
    
    def process_exception(self, request, exception):
        session.close()
    
    def generate_key(self, user):
        return User.hasher(user.name+user.passwd+str(datetime.datetime.now())+str(random.randrange(1,1000000000)))
