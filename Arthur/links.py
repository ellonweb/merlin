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
from django.http import HttpResponseRedirect
from Arthur.context import menu
from Arthur.loadable import loadable

urlpatterns = patterns('Arthur.links',
    url(r'^game/$', 'game'),
    url(r'^forums/$', 'forums'),
    url(r'^sandmans/$', 'sandmans'),
    url(r'^bcalc/$', 'bcalc'),
)

@menu("Planetarion", "Game")
class game(loadable):
    def execute(self, request, user):
        return HttpResponseRedirect("http://game.planetarion.com")

@menu("Planetarion", "Forums")
class forums(loadable):
    def execute(self, request, user):
        return HttpResponseRedirect("http://pirate.planetarion.com")

@menu("Planetarion", "Sandmans")
class sandmans(loadable):
    def execute(self, request, user):
        return HttpResponseRedirect("http://sandmans.co.uk")

@menu("Planetarion", "BCalc")
class bcalc(loadable):
    def execute(self, request, user):
        return HttpResponseRedirect("http://game.planetarion.com/bcalc.pl")
