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
 
from sqlalchemy.orm import aliased
from sqlalchemy.sql import desc
from sqlalchemy.sql.functions import count
from Core.db import session
from Core.maps import Updates, Galaxy, Planet, Alliance, User, Intel, FleetScan
from Core.loadable import loadable, route, require_planet
from Core.config import Config
from Core.paconf import PA

class topcunts(loadable):
    """Top planets attacking the specified target"""
    usage = " [x:y[:z]|alliance|user]"
    access = "member"
    
    @route(loadable.coord)
    def planet_galaxy(self, message, user, params):
        # Planet
        if params.group(5) is not None:
            planet = Planet.load(*params.group(1,3,5))
            if planet is None:
                message.reply("No planet with coords %s:%s:%s found" % params.group(1,3,5))
            else:
                self.execute(message, planet=planet)

        # Galaxy
        else:
            galaxy = Galaxy.load(*params.group(1,3))
            if galaxy is None:
                message.reply("No galaxy with coords %s:%s" % params.group(1,3))
            else:
                self.execute(message, galaxy=galaxy)
    
    @route(r"\s+(\S+)")
    def user_alliance(self, message, user, params):
        alliance = Alliance.load(params.group(1))
        if alliance is None:
            u = User.load(name=params.group(1), exact=False, access="member")
            if u is None:
                message.reply("No alliance or user matching '%s' found" % (params.group(1),))
            elif u.planet is None:
                message.reply("User %s has not entered their planet details" % (u.name,))
            else:
                planet = u.planet
                self.execute(message, planet=planet)
        else:
            self.execute(message, alliance=alliance)
    
    @route(r"\s*$")
    @require_planet
    def me(self, message, user, params):
        self.execute(message, planet=user.planet)
    
    def execute(self, message, planet=None, galaxy=None, alliance=None):
        tick = Updates.current_tick()
        target = aliased(Planet)
        target_intel = aliased(Intel)
        owner = aliased(Planet)
        owner_intel = aliased(Intel)
        
        Q = session.query(owner.x, owner.y, owner.z, count())
        Q = Q.join((FleetScan.owner, owner))
        Q = Q.join((FleetScan.target, target))
        Q = Q.filter(FleetScan.mission == "Attack")
        if planet:
            Q = Q.filter(FleetScan.target == planet)
        if galaxy:
            Q = Q.filter(target.galaxy == galaxy)
        if alliance:
            Q = Q.join((target.intel, target_intel))
            Q = Q.filter(target_intel.alliance == alliance)
        Q = Q.group_by(owner.x, owner.y, owner.z)
        Q = Q.order_by(desc(count()))
        result = Q.all()
        
        if len(result) < 1:
            reply="No fleets found targetting"
            if planet:
                reply+=" coords %s:%s:%s"%(planet.x,planet.y,planet.z)
            if galaxy:
                reply+=" coords %s:%s"%(galaxy.x,galaxy.y)
            if alliance:
                reply+=" alliance %s"%(alliance.name,)
            message.reply(reply)
            return
        
        reply = "Top attackers on"
        if planet:
            reply+=" coords %s:%s:%s"%(planet.x,planet.y,planet.z)
        if galaxy:
            reply+=" coords %s:%s"%(galaxy.x,galaxy.y)
        if alliance:
            reply+=" alliance %s"%(alliance.name,)
        reply+=" are (total: %s) "%(sum([attacks for x,y,z, attacks in result]),)
        prev = []
        for x, y, z, attacks in result[:5]:
            prev.append("%s:%s:%s - %s"%(x,y,z,attacks))
        message.reply(reply+" | ".join(prev))
