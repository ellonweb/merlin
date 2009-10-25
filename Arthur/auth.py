import datetime
import random
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from Core.config import Config
from Core.db import session
from Core.maps import User, Session, Slogan

SESSION_KEY = "%sSESSID" % (Config.get("Alliance", "name")[:3].upper(),)
SUBMIT = "submit"
LOGOUT = "Logout"
LOGIN = "Login"
USER = "username"
PASS = "password"

class Authentication(object):
    def process_request(self, request):
        request.session = None
        request.response = HttpResponse()
        key = request.COOKIES.get(SESSION_KEY)
        if key:
            auth = Session.load(key, datetime.datetime.now())
            if auth is None:
                request.response.delete_cookie(SESSION_KEY)
                request.response.write(render_to_string("login.tpl", {"msg": "Your session has expired, please login again."}, RequestContext(request)))
                return request.response
            if request.REQUEST.get(SUBMIT) == LOGOUT:
                session.delete(auth)
                session.commit()
                request.response.delete_cookie(SESSION_KEY)
                request.response.write(render_to_string("login.tpl", {"msg": "Logged out."}, RequestContext(request)))
                return request.response
            request.session = auth
            return
        elif (request.REQUEST.get(USER) is not None and request.REQUEST.get(PASS) is not None):
            user = User.load(name=request.REQUEST.get(USER), passwd=request.REQUEST.get(PASS))
            if user is None:
                request.response.delete_cookie(SESSION_KEY)
                request.response.write(render_to_string("login.tpl", {"msg": "Invalid user."}, RequestContext(request)))
                return request.response
            else:
                key = self.generate_key(user)
                auth = Session(key=key, expire=datetime.datetime.now()+datetime.timedelta(days=1), user=user)
                session.query(Session).filter(Session.user == user).delete()
                session.add(auth)
                session.commit()
                request.session = auth
                request.response.set_cookie(SESSION_KEY, request.session.key)
                return
        else:
            request.response.write(render_to_string("login.tpl", {"msg": "Hi! Please login below:"}, RequestContext(request)))
            return request.response
    
    def process_response(self, request, response):
        session.close()
        return request.response
    
    def process_exception(self, request, exception):
        session.close()
    
    def generate_key(self, user):
        return User.hasher(user.name+user.passwd+str(datetime.datetime.now())+str(random.randrange(1,1000000000)))

def Context(request):
    context = {"alliance": Config.get("Alliance", "name")}
    slogan, count = Slogan.search("")
    if slogan is not None:
        context["slogan"] = str(slogan)
    if request.session is not None:
        context["user"] = request.session.user.name
    return context
