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
from sqlalchemy.sql.functions import sum
from Core.config import Config
from Core.db import session
from Core.maps import Cookie
from Core.loadable import loadable, route

class gac(loadable):
    """Displays stats about the Gross Alliance Cookies. Similar to the Gross Domestic Product, GAC covers how many cookies changed hands in a given week."""
    
    @route(access = "member")
    def execute(self, message, user, params):
        
        last_5_gac=self.get_last_5_gac()
        
        max_gac=self.get_max_gac()
        min_gac=self.get_min_gac()
        
        if (max_gac or min_gac) is None:
            message.reply("Apparently noone likes the cookies I baked! Why don't you feed some to your friends?")
            return
        
        reply = "Gross Alliance Cookies for %s for last 5 weeks (current first): %s"%(Config.get("Alliance","name"),', '.join(last_5_gac))
        reply+= " | Highest ever GAC: %s in week %s/%s."%(max_gac[0],max_gac[1],max_gac[2])
        reply+= " | Lowest ever GAC: %s in week %s/%s."%(min_gac[0],min_gac[1],min_gac[2])
        message.reply(reply)
    
    def get_max_gac(self):
        return self.get_minmax_gac(max=True)
    def get_min_gac(self):
        return self.get_minmax_gac(min=True)
    
    def base_query(self):
        return session.query(sum(Cookie.howmany).label("gac"), Cookie.week, Cookie.year).group_by(Cookie.year, Cookie.week)
    
    def get_minmax_gac(self,max=True,min=False):
        if min:
            order=asc
        elif max:
            order=desc
        return self.base_query().order_by(order("gac")).first()
    
    def get_last_5_gac(self):
        result = self.base_query().order_by(desc(Cookie.year), desc(Cookie.week))[:5]
        return map(lambda x: str(x[0]),result)
