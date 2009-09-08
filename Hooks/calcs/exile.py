# This file is part of Merlin.
 
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
 
# This work is Copyright (C)2008 of Robin K. Hansen, Elliot Rosemarine.
# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

from .Core.modules import M
loadable = M.loadable.loadable

class exile(loadable):
    """Calculate how long it will take to repay a value loss capping roids."""
    
    def __init__(self):
        loadable.__init__(self)
    
    @loadable.run
    def execute(self, message, user, params):
        
        session = M.DB.Session()
        Q = session.query(M.DB.Maps.Planet.id, M.DB.SQL.f.count().label('planets'))
        Q = Q.filter(M.DB.Maps.Planet.x < 200)
        Q = Q.group_by(M.DB.Maps.Planet.x, M.DB.Maps.Planet.y)
        Q = Q.order_by(M.DB.SQL.desc(M.DB.SQL.f.count()))
        subQ = Q.subquery()

        Q = session.query(subQ.c.planets, M.DB.SQL.f.count().label('count'))
        Q = Q.group_by(subQ.c.planets)
        Q = Q.order_by(M.DB.SQL.asc(subQ.c.planets))

        result = Q.all()
        session.close()

        if len(result) < 1:
            message.reply("There is no spoon")
            return

        gals=0
        bracket=0
        max_planets=0

        for planets, count in result:
            gals+=count
        bracket=int(gals*.2)
        for planets, count in result:
            bracket-=count
            if bracket < 0:
                rest_gals=bracket+count
                total_rest_gals=count
                rest_planets=planets
                break
            max_planets=planets

        reply="Total galaxies: %s Maximum planets to guarantee a galaxy is in the exile bracket: %s" % (gals,max_planets)
        reply+=" | Also in the bracket: %s of %s galaxies with %s planets."%(rest_gals,total_rest_gals,rest_planets)

        message.reply(reply)
