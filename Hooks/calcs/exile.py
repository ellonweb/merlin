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
 
from sqlalchemy.sql import asc, desc
from sqlalchemy.sql.functions import count
from Core.db import session
from Core.maps import Galaxy, Planet
from Core.loadable import loadable, route

class exile(loadable):
    @route()
    def execute(self, message, user, params):
        
        Q = session.query(Planet.x, Planet.y, count().label('planets'))
        Q = Q.join(Planet.galaxy)
        Q = Q.filter(Planet.active == True)
        Q = Q.filter(Galaxy.private == False)
        Q = Q.filter(Planet.x < 200)
        Q = Q.group_by(Planet.x, Planet.y)
        Q = Q.order_by(desc(count()))
        subQ = Q.subquery()

        Q = session.query(subQ.c.planets, count().label('count'))
        Q = Q.group_by(subQ.c.planets)
        Q = Q.order_by(asc(subQ.c.planets))

        result = Q.all()

        if len(result) < 1:
            message.reply("There is no spoon")
            return

        gals=0
        bracket=0
        base_bracket_gals = 0
        max_planets=0

        for planets, galaxies in result:
            gals+=galaxies
        
        bracket=int(gals*.2)
        
        for planets, galaxies in result:
            bracket-=galaxies
            if bracket < 0:
                rest_gals=bracket+galaxies
                total_rest_gals=galaxies
                rest_planets=planets
                break
            max_planets=planets
            base_bracket_gals+=galaxies

        reply = "Total galaxies: %s"%(gals,)
        reply+= " | %s galaxies with a maximum of %s planets guaranteed to be in the exile bracket"%(base_bracket_gals,max_planets,)
        reply+= " | Also in the bracket: %s of %s galaxies with %s planets."%(rest_gals,total_rest_gals,rest_planets,)

        message.reply(reply)
