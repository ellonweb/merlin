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

from django.conf.urls.defaults import include, patterns, url
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from Core.config import Config
from Core.db import session
from Core.maps import User
from Arthur.context import menu, render
from Arthur.loadable import loadable, load
name = Config.get("Alliance", "name")

urlpatterns = patterns('Arthur.dashboard',
    url(r'^dashboard/$', 'dashboard'),
    url(r'^user/(?P<username>\S+)/$', 'dashboard', name="dashboard"),
)

@menu(name, "Dashboard")
@load
class dashboard(loadable):
    access = "member"
    
    def execute(self, request, user, username="", dashuser=None):
        dashuser = dashuser or User.load(username or user.name, exact=False)
        if dashuser is None:
            return HttpResponseRedirect(reverse("memberlist"))
        
        gimps = dashuser.gimps
        mums = dashuser.mums
        ships = dashuser.fleets.all()
        phonefriend = user == dashuser or user in dashuser.phonefriends
        
        return render("dashboard.tpl", request, dashuser=dashuser, planet=dashuser.planet, gimps=gimps, mums=mums, ships=ships, phonefriend=phonefriend)
