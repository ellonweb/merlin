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
 
from datetime import timedelta
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from sqlalchemy import and_
from sqlalchemy.orm import aliased
from sqlalchemy.sql import desc
from Core.paconf import PA
from Core.db import session
from Core.maps import Updates, Alliance, AllianceHistory
from Arthur.context import render
from Arthur.loadable import loadable, load

@load
class alliance(loadable):
    def execute(self, request, user, name, h=False, ticks=None):
        alliance = Alliance.load(name)
        if alliance is None:
            return HttpResponseRedirect(reverse("alliance_ranks"))
        
        ticks = int(ticks or 0) if h else 12
        
        history = aliased(AllianceHistory)
        next = aliased(AllianceHistory)
        membersdiff = history.members - next.members
        sizediff_avg = history.size_avg - next.size_avg
        scorediff_avg = history.score_avg - next.score_avg
        pointsdiff_avg = history.points_avg - next.points_avg
        sizediff = history.size - next.size
        sizediffvalue = sizediff * PA.getint("numbers", "roid_value")
        scorediff = history.score - next.score
        scorediffwsizevalue = scorediff - sizediffvalue
        pointsdiff = history.points - next.points
        Q = session.query(history, Updates.timestamp - timedelta(minutes=1),
                            next.score_rank, membersdiff,
                            sizediff_avg, scorediff_avg, pointsdiff_avg,
                            sizediff, sizediffvalue,
                            scorediff, scorediffwsizevalue,
                            pointsdiff
                            )
        Q = Q.join(Updates)
        Q = Q.outerjoin((next, and_(history.id==next.id, history.tick-1==next.tick)))
        Q = Q.filter(history.current == alliance)
        Q = Q.order_by(desc(history.tick))
        
        return render(["alliance.tpl","halliance.tpl"][h],
                        request,
                        alliance = alliance,
                        history = Q[:ticks] if ticks else Q.all(),
                        ticks = ticks,
                      )
