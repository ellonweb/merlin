# This file is part of Merlin.
# Merlin is the Copyright (C)2008,2009,2010 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.

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
from Core.maps import Updates
from Core.loadable import loadable, route

class launch(loadable):
    """Calculate launch tick, launch time, prelaunch tick and prelaunch modifier for a given ship class or eta, and land tick."""
    usage = " <class|eta> <land_tick>"
    class_eta = {"fi": 8,
                 "co": 8,
                 "fr": 9,
                 "de": 9,
                 "cr": 10,
                 "bs": 10}
    
    @route(r"(\S+)\s+(\d+)")
    def execute(self, message, user, params):
        
        eta, land_tick = params.groups()
        land_tick = int(land_tick)

        if eta.lower() in self.class_eta.keys():
             eta = self.class_eta[eta.lower()]
        else:
            try:
                eta = int(eta)
            except ValueError:
                message.alert("Invalid class or eta '%s'" % (eta,))
                return

        current_tick=Updates.current_tick()

        current_time = datetime.datetime.utcnow()
        launch_tick = land_tick - eta
        launch_time = current_time + datetime.timedelta(hours=(launch_tick-current_tick))
        prelaunch_tick = land_tick - eta + 1
        prelaunch_mod = launch_tick - current_tick

        message.reply("eta %d landing pt %d (currently %d) must launch at pt %d (%s), or with prelaunch tick %d (currently %+d)" % (eta, land_tick, current_tick, launch_tick, (launch_time.strftime("%m-%d %H:55")), prelaunch_tick, prelaunch_mod))
