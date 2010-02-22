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
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from sqlalchemy.sql import desc
from Core.db import session
from Core.maps import Updates, Planet, Alliance, Intel, FleetScan
from Core.loadable import loadable, route
from Core.config import Config
from Core.paconf import PA

class cunts(loadable):
    """Target search, based on planets currently attacking our alliance, ordered by size"""
    usage = " [alliance] [race] [<|>][size] [<|>][value] [bash] (must include at least one search criteria, order doesn't matter)"
    PrefError = "You must set your planet with !pref to use the bash option"
    alliancere=re.compile(r"(\S+)")
    rangere=re.compile(r"(<|>)?(\d+)")
    bashre=re.compile(r"(bash)",re.I)
    clusterre=re.compile(r"c(\d+)",re.I)
    
    @route(r"\s+(.+)", access = "member")
    def execute(self, message, user, params):
        
        alliance=Alliance()
        race=None
        size_mod=None
        size=None
        value_mod=None
        value=None
        bash=False
        attacker=None
        cluster=None

        params=params.group(1).split()

        for p in params:
            m=self.bashre.match(p)
            if m and not bash:
                bash=True
                attacker = self.get_user_planet(user)
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

        tick = Updates.current_tick()
        target = aliased(Planet)
        target_intel = aliased(Intel)
        owner = aliased(Planet)
        owner_intel = aliased(Intel)
        
        Q = session.query(owner, owner_intel).distinct()
        Q = Q.join((FleetScan.owner, owner))
        Q = Q.join((FleetScan.target, target))
        Q = Q.join((target.intel, target_intel))
        Q = Q.filter(target_intel.alliance == Alliance.load(Config.get("Alliance","name")))
        Q = Q.filter(FleetScan.landing_tick > tick)
        Q = Q.filter(FleetScan.mission == "Attack")
        if alliance.id:
            Q = Q.join((owner.intel, owner_intel))
            Q = Q.filter(owner_intel.alliance == alliance)
        else:
            Q = Q.outerjoin((owner.intel, owner_intel))
            if alliance.name:
                Q = Q.filter(owner_intel.alliance == None)
        Q = Q.filter(owner.active == True)
        if race:
            Q = Q.filter(owner.race.ilike(race))
        if size:
            Q = Q.filter(owner.size.op(size_mod)(size))
        if value:
            Q = Q.filter(owner.value.op(value_mod)(value))
        if bash:
            Q = Q.filter(or_(owner.value.op(">")(attacker.value*PA.getfloat("bash","value")),
                             owner.score.op(">")(attacker.score*PA.getfloat("bash","score"))))
        if cluster:
            Q = Q.filter(owner.x == cluster)
        Q = Q.order_by(desc(owner.size))
        Q = Q.order_by(desc(owner.value))
        result = Q[:6]
        
        if len(result) < 1:
            reply="No"
            if race:
                reply+=" %s"%(race,)
            reply+=" planets attacking %s" % (Config.get("Alliance","name"),)
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
        for planet, intel in result[:5]:
            reply="%s:%s:%s (%s)" % (planet.x,planet.y,planet.z,planet.race)
            reply+=" Value: %s Size: %s" % (planet.value,planet.size)
            if intel:
                if intel.nick:
                    reply+=" Nick: %s" % (intel.nick,)
                if not alliance.name and intel.alliance:
                    reply+=" Alliance: %s" % (intel.alliance.name,)
            Q = session.query(FleetScan, Intel.nick).distinct()
            Q = Q.join(FleetScan.target)
            Q = Q.outerjoin(Planet.intel)
            Q = Q.filter(FleetScan.owner == planet)
            Q = Q.filter(FleetScan.landing_tick > tick)
            Q = Q.filter(FleetScan.mission == "Attack")
            result2 = Q.all()
            if len(result2):
                reply+=" Hitting: "
                prev=[]
                for fleet, nick in result2:
                    prev.append((nick or 'Unknown') + " (%s, lands: %s)"% (fleet.fleet_size,fleet.landing_tick))
                reply+=', '.join(prev)
            replies.append(reply)
        if len(result) > 5:
            replies[-1]+=" (Too many results to list, please refine your search)"
        message.reply("\n".join(replies))
