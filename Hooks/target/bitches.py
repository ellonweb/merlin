# This file is part of Merlin.
# Merlin is the Copyright (C)2008-2009 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.

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
 
import re
from sqlalchemy.sql.functions import count
from Core.config import Config
from Core.db import session
from Core.maps import Updates, Galaxy, Planet, Alliance, Intel, Target
from Core.loadable import loadable

@loadable.module("half")
class bitches(loadable):
    """List of booked targets by galaxy and alliance"""
    usage = " [minimum eta]"
    paramre = re.compile(r"(?:\s(\d+))?")
    
    def execute(self, message, user, params):
        
        tick = Updates.current_tick() + int(params.group(1) or 1)
        replies = []
        
        Q = session.query(Galaxy.x, Galaxy.y, count())
        Q = Q.join(Target.planet)
        Q = Q.join(Planet.galaxy)
        Q = Q.filter(Planet.active == True)
        Q = Q.filter(Target.tick >= tick)
        Q = Q.group_by(Galaxy.x, Galaxy.y)
        result = Q.all()
        prev = []
        for x, y, bitches in result:
            prev.append("%s:%s(%s)"%(x,y,bitches))
        replies.append("Active bookings: " + ", ".join(prev))
        
        Q = session.query(Alliance.name, count())
        Q = Q.join(Target.planet)
        Q = Q.outerjoin(Planet.intel)
        Q = Q.outerjoin(Intel.alliance)
        Q = Q.filter(Planet.active == True)
        Q = Q.filter(Target.tick >= tick)
        Q = Q.group_by(Alliance.name)
        result = Q.all()
        prev = []
        for name, bitches in result:
            prev.append("%s (%s)"%(name or "Unknown", bitches))
        replies.append("Active bitches: " + ", ".join(prev))
        
        if len(replies) < 1:
            replies.append("No active bookings. This makes %s sad. Please don't make %s sad." %((Config.get("Connection","nick"),)*2))
        message.reply("\n".join(replies))
