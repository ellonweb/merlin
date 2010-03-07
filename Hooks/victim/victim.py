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
 
import re
from sqlalchemy import cast, Float, func, Integer, or_
from sqlalchemy.sql import desc
from Core.db import session
from Core.maps import Planet, Alliance, Intel
from Core.loadable import loadable, route, require_planet
from Core.paconf import PA

class victim(loadable):
    """Target search, ordered by maxcap"""
    usage = " [alliance] [race] [<|>][size] [<|>][value] [bash] (must include at least one search criteria, order doesn't matter)"
    alliancere=re.compile(r"(\S+)")
    rangere=re.compile(r"(<|>)?(\d+)")
    bashre=re.compile(r"(bash)",re.I)
    clusterre=re.compile(r"c(\d+)",re.I)
    
    @route(r"(.+)", access = "member")
    @require_planet
    def execute(self, message, user, params):
        
        alliance=Alliance()
        race=None
        size_mod=None
        size=None
        value_mod=None
        value=None
        bash=False
        attacker=user.planet
        cluster=None

        params=params.group(1).split()

        for p in params:
            m=self.bashre.match(p)
            if m and not bash:
                bash=True
                continue
            m=self.clusterre.match(p)
            if m and not cluster:
                cluster=int(m.group(1))
            m=self.racere.match(p)
            if m and not race:
                race=m.group(1)
                continue
            m=self.rangere.match(p)
            if m and not size and int(m.group(2)) < 32768:
                size_mod=m.group(1) or '>'
                size=m.group(2)
                continue
            m=self.rangere.match(p)
            if m and not value:
                value_mod=m.group(1) or '<'
                value=m.group(2)
                continue
            m=self.alliancere.match(p)
            if m and not alliance.name and not self.clusterre.match(p):
                alliance = Alliance(name="Unknown") if m.group(1).lower() == "unknown" else Alliance.load(m.group(1))
                if alliance is None:
                    message.reply("No alliance matching '%s' found" % (m.group(1),))
                    return
                continue

        maxcap = PA.getfloat("roids","maxcap")
        mincap = PA.getfloat("roids","mincap")
        modifier = (cast(Planet.value,Float).op("/")(float(attacker.value))).op("^")(0.5)
        caprate = func.float8larger(mincap,func.float8smaller(modifier.op("*")(maxcap),maxcap))
        maxcap = cast(func.floor(cast(Planet.size,Float).op("*")(caprate)),Integer)
        
        Q = session.query(Planet, Intel, maxcap.label("maxcap"))
        if alliance.id:
            Q = Q.join(Planet.intel)
            Q = Q.filter(Intel.alliance == alliance)
        else:
            Q = Q.outerjoin(Planet.intel)
            if alliance.name:
                Q = Q.filter(Intel.alliance == None)
        Q = Q.filter(Planet.active == True)
        if race:
            Q = Q.filter(Planet.race.ilike(race))
        if size:
            Q = Q.filter(Planet.size.op(size_mod)(size))
        if value:
            Q = Q.filter(Planet.value.op(value_mod)(value))
        if bash:
            Q = Q.filter(or_(Planet.value.op(">")(attacker.value*PA.getfloat("bash","value")),
                             Planet.score.op(">")(attacker.score*PA.getfloat("bash","score"))))
        if cluster:
            Q = Q.filter(Planet.x == cluster)
        Q = Q.order_by(desc("maxcap"))
        Q = Q.order_by(desc(Planet.size))
        Q = Q.order_by(desc(Planet.value))
        result = Q[:6]
        
        if len(result) < 1:
            reply="No"
            if race:
                reply+=" %s"%(race,)
            reply+=" planets"
            if alliance.name:
                reply+=" in intel matching Alliance: %s"%(alliance.name,)
            else:
                reply+=" matching"
            if size:
                reply+=" Size %s %s" % (size_mod,size)
            if value:
                reply+=" Value %s %s" % (value_mod,value)
            message.reply(reply)
            return
        
        replies = []
        for planet, intel, maxcap in result[:5]:
            reply="%s:%s:%s (%s)" % (planet.x,planet.y,planet.z,planet.race)
            reply+=" Value: %s Size: %s MaxCap: %s" % (planet.value,planet.size, maxcap)
            if intel:
                if intel.nick:
                    reply+=" Nick: %s" % (intel.nick,)
                if not alliance.name and intel.alliance:
                    reply+=" Alliance: %s" % (intel.alliance.name,)
            replies.append(reply)
        if len(result) > 5:
            replies[-1]+=" (Too many results to list, please refine your search)"
        message.reply("\n".join(replies))
