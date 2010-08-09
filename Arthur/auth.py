# This file is part of Merlin/Arthur.
# Merlin/Arthur is the Copyright (C)2009,2010 of Elliot Rosemarine.

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

from Core.config import Config
from Core.db import session
from Core.maps import User, Session
from Arthur.context import render
from Arthur.errors import server_error, exceptions

SESSION_KEY = "SESSION"
LOGOUT = "/logout/"
USER = "username"
PASS = "password"

class authentication(object):
    def process_request(self, request):
        try:
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
            elif (request.REQUEST.get(USER) and request.REQUEST.get(PASS)):
                user = User.load(name=request.REQUEST.get(USER), passwd=request.REQUEST.get(PASS))
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
        except Exception as exc:
            exceptions().process_exception(request, exc)
            return server_error(request)
    
    def process_response(self, request, response):
        if hasattr(request, "_COOKIE"):
            if request._COOKIE == None:
                response.delete_cookie(SESSION_KEY)
            else:
                response.set_cookie(SESSION_KEY, request._COOKIE)
        return response
    
    def login_page(self, request, msg):
        return render("login.tpl", request, msg=msg)
    
    def generate_key(self, user):
        return User.hasher(user.name+user.passwd+str(datetime.datetime.now())+str(random.randrange(1,1000000000)))
