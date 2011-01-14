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
 
from sqlalchemy.sql import asc
from Core.db import session
from Core.maps import Galaxy, Planet, Alliance, Intel
from Core.loadable import loadable, route

options = ['alliance', 'nick', 'fakenick', 'defwhore', 'covop', 'amps', 'dists', 'bg', 'gov', 'relay', 'reportchan', 'comment']

class intel(loadable):
    """View or set intel for a planet. Valid options: """
    __doc__ += ", ".join(options)
    usage = " <x.y[.z]> [option=value]+"
    
    @route(loadable.coord, access = "galmate")
    def view_intel(self, message, user, params):
        
        if params.group(5) is None:
            galaxy = Galaxy.load(*params.group(1,3))
            if galaxy is None:
                message.alert("No galaxy with coords %s:%s" % params.group(1,3))
                return
            
            Q = session.query(Planet)
            Q = Q.filter(Planet.active == True)
            Q = Q.filter(Planet.galaxy == galaxy)
            Q = Q.order_by(asc(Planet.z))
            prev = []
            for planet in Q:
                if planet.intel is not None and (planet.intel.nick or planet.alliance):
                    reply = "#%s"%(planet.z,)
                    if planet.intel.nick:
                        reply += " %s"%(planet.intel.nick,)
                    if planet.alliance and planet.alliance.alias:
                        reply += " [%s]"%(planet.alliance.alias[:3],)
                    elif planet.alliance:
                        reply += " [%s]"%(planet.alliance.name[:3],)
                    prev.append(reply)
            if len(prev):
                reply ="Intel %d:%d - "%(galaxy.x,galaxy.y,)
                reply+="Score (%d) Value (%d) Size (%d)"%(galaxy.score_rank,galaxy.value_rank,galaxy.size_rank)
                reply+=" - "
                reply+=" - ".join(prev)
                message.reply(reply)
            else:
                message.reply("No information stored for %s:%s" % (galaxy.x, galaxy.y,))
            return
        
        planet = Planet.load(*params.group(1,3,5))
        if planet is None:
            message.alert("No planet with coords %s:%s:%s" % params.group(1,3,5))
            return
        
        if planet.intel and str(planet.intel):
            message.reply("Information stored for %s:%s:%s -%s"% (planet.x, planet.y, planet.z, str(planet.intel),))
        else:
            message.reply("No information stored for %s:%s:%s"% (planet.x, planet.y, planet.z,))
    
    @route(loadable.planet_coord+r"\s+(\S.*)", access = "galmate")
    def set_intel(self, message, user, params):
        planet = Planet.load(*params.group(1,3,5))
        if planet is None:
            message.alert("No planet with coords %s:%s:%s" % params.group(1,3,5))
            return
        
        if planet.intel is None:
            planet.intel = Intel()
        
        params = self.split_opts(message.get_msg())
        for opt, val in params.items():
            if opt == "alliance":
                if val in self.nulls:
                    planet.intel.alliance = None
                    continue
                alliance = Alliance.load(val)
                if alliance is None:
                    message.alert("No alliances match %s" % (val,))
                    continue
                planet.intel.alliance = alliance
            if (opt in options) and (val in self.nulls):
                setattr(planet.intel, opt, None)
                continue
            if opt in ("nick","fakenick","bg","gov","reportchan"):
                setattr(planet.intel, opt, val)
            if opt in ("defwhore","covop","relay"):
                if val.lower() in self.true:
                    setattr(planet.intel, opt, True)
                if val.lower() in self.false:
                    setattr(planet.intel, opt, False)
            if opt in ("amps","dists"):
                if val.isdigit():
                    setattr(planet.intel, opt, int(val))
            if opt == "comment":
                planet.intel.comment = message.get_msg()[message.get_msg().lower().index("comment=")+len("comment="):]
        session.commit()
        if planet.intel and str(planet.intel):
            message.reply("Information stored for %s:%s:%s -%s"% (planet.x, planet.y, planet.z, str(planet.intel),))
        else:
            message.reply("No information stored for %s:%s:%s"% (planet.x, planet.y, planet.z,))
