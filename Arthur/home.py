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
 
from datetime import datetime
from Core.maps import Updates
from Arthur.auth import render

def index(request):
    planet = request.session.user.planet
    now = datetime.now()
    d1 = datetime(now.year, now.month, now.day, now.hour)
    d2 = datetime(now.year, now.month, now.day)
    hours = (d1-d2).seconds/60/60
    tick = Updates.current_tick() - hours
    ph = planet.history(tick)
    return render("index.tpl", request, planets=((planet, ph, None, None),), title="Your planet")
