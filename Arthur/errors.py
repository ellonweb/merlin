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
 
import time

from django.http import HttpResponseNotFound, HttpResponseServerError

from Core.string import arthurlog
from Core.db import session
from Arthur.context import render

class db(object):
    def process_request(self, request):
        session.remove()
    
    def process_response(self, request, response):
        session.remove()
        return response
    
    def process_exception(self, request, exception):
        session.remove()

def page_not_found(request):
    return HttpResponseNotFound(render("error.tpl", request, msg="Page not found"))

def server_error(request):
    return HttpResponseServerError(render("error.tpl", request, msg="Server error, please report the error to an admin as soon as possible"))

class exceptions(object):
    def process_exception(self, request, exception):
        arthurlog("%s - Arthur Error: %s\n" % (time.asctime(),str(exception),))
        return server_error(request)
