# This file is part of Merlin/Arthur.
# Merlin/Arthur is the Copyright (C)2009 of Elliot Rosemarine.

# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
 
import datetime
import random
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from Core.config import Config
from Core.db import session
from Core.maps import User, Session, Slogan

SESSION_KEY = "%sSESSID" % (Config.get("Alliance", "name")[:3].upper(),)
LOGOUT = "/logout/"
USER = "username"
PASS = "password"

class authentication(object):
    def process_request(self, request):
        if request.path[:8] == "/static/":
            return
        request.session = None
        key = request.COOKIES.get(SESSION_KEY)
        if key:
            auth = Session.load(key, datetime.datetime.now())
            if auth is None:
                request._COOKIE = None
                return self.login_page(request, "Your session has expired, please login again.")
            if request.path == LOGOUT:
                session.delete(auth)
                session.commit()
                request._COOKIE = None
                return self.login_page(request, "Logged out.")
            request.session = auth
            return
        elif (request.REQUEST.get(USER) is not None and request.REQUEST.get(PASS) is not None):
            user = User.load(name=request.REQUEST.get(USER), passwd=request.REQUEST.get(PASS), access="member")
            if user is None:
                request._COOKIE = None
                return self.login_page(request, "Invalid user.")
            else:
                key = self.generate_key(user)
                auth = Session(key=key, expire=datetime.datetime.now()+datetime.timedelta(days=1), user=user)
                session.query(Session).filter(Session.user == user).delete()
                session.add(auth)
                session.commit()
                request.session = auth
                request._COOKIE = key
                return
        else:
            return self.login_page(request, "Hi! Please login below:")
    
    def process_response(self, request, response):
        session.close()
        if hasattr(request, "_COOKIE"):
            if request._COOKIE == None:
                response.delete_cookie(SESSION_KEY)
            else:
                response.set_cookie(SESSION_KEY, request._COOKIE)
        return response
    
    def process_exception(self, request, exception):
        session.close()
    
    def login_page(self, request, msg):
        return render("login.tpl", request, msg=msg)
    
    def generate_key(self, user):
        return User.hasher(user.name+user.passwd+str(datetime.datetime.now())+str(random.randrange(1,1000000000)))

class _menu(object):
    heads = []
    content = {}
    
    def __call__(self, head, sub=None):
        
        def wrapper(hook):
            url = "/" + hook.__name__ + "/"
            
            if head not in self.heads:
                self.heads.append(head)
                self.content[head] = {"hook":hook, "url":url, "subs":[], "content":{}}
            if sub is not None:
                self.content[head]["subs"].append(sub)
                self.content[head]["content"][sub] = {"hook":hook, "url":url}
            
            return hook
        return wrapper
    
    def generate(self, user):
        menu = []
        for head in self.heads:
            #if self.content[head]["hook"].has_access(user):
                menu.append([head, self.content[head]["url"], []])
                
                for sub in self.content[head]["subs"]:
                    #if self.content[head]["content"][sub]["hook"].has_access(user):
                        menu[-1][2].append([sub, self.content[head]["content"][sub]["url"]])
        
        menu.append(["Logout", "/logout/", []])
        return menu

menu = _menu()

def context(request):
    context = {"slogan": Config.get("Alliance", "name")}
    if request.session is not None:
        slogan, count = Slogan.search("")
        if slogan is not None:
            context["slogan"] = str(slogan)
        context["user"] = request.session.user.name
        context["menu"] = menu.generate(request.session.user)
    return context

def render(tpl, request, **context):
    return render_to_response(tpl, context, RequestContext(request))
