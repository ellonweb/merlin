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
 
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from sqlalchemy.sql import desc
from Core.db import session
from Core.maps import Updates, Planet, Request
from Arthur.loadable import loadable, load
from Core.paconf import PA
from Arthur.context import render
from Core.robocop import push

@load
class request(loadable):
    access = "member"
    def execute(self, request, user):
        requests = Request.load_active()
        userrequests = Request.load_foruser(user)
        

        return render("request.tpl", request, title="", intel=user.is_member(), requests=requests,userrequests=userrequests)
