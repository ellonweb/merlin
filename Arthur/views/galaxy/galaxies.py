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
 
from sqlalchemy.sql import asc, desc
from Core.db import session
from Core.maps import Galaxy
from Arthur.context import menu, render
from Arthur.loadable import loadable, load

@menu("Rankings", "Galaxies")
@load
class galaxies(loadable):
    def execute(self, request, user, page="1", sort="score"):
        page = int(page)
        offset = (page - 1)*50
        order =  {"score" : (asc(Galaxy.score_rank),),
                  "value" : (asc(Galaxy.value_rank),),
                  "size"  : (asc(Galaxy.size_rank),),
                  "planets" : (desc(Galaxy.members),),
                  "ratio" : (desc(Galaxy.ratio),),
                  "xp"    : (asc(Galaxy.xp_rank),),
                  "score_growth" : (desc(Galaxy.score_growth),),
                  "value_growth" : (desc(Galaxy.value_growth),),
                  "size_growth"  : (desc(Galaxy.size_growth),),
                  "xp_growth"    : (desc(Galaxy.xp_growth),),
                  "score_growth_pc" : (desc(Galaxy.score_growth_pc),),
                  "value_growth_pc" : (desc(Galaxy.value_growth_pc),),
                  "size_growth_pc"  : (desc(Galaxy.size_growth_pc),),
                  "xp_growth_pc"    : (desc(Galaxy.xp_growth_pc),),
                  }
        if sort not in order.keys():
            sort = "score"
        order = order.get(sort)
        
        Q = session.query(Galaxy)
        Q = Q.filter(Galaxy.active == True)
        
        count = Q.count()
        pages = count/50 + int(count%50 > 0)
        pages = range(1, 1+pages)
        
        for o in order:
            Q = Q.order_by(o)
        Q = Q.limit(50).offset(offset)
        return render("galaxies.tpl", request, galaxies=Q.all(), offset=offset, pages=pages, page=page, sort=sort)
