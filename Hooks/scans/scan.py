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
 
from sqlalchemy.sql import desc
from Core.config import Config
from Core.paconf import PA
from Core.db import session
from Core.maps import Planet, Scan
from Core.loadable import loadable, route

class scan(object):
    usage = " (<x:y:z> [old] [link] | <id>)"
    access = "half"
    type = ""
    planetre = loadable.planet_coord+r"(?:\s+(o)\S*)?(?:\s+(l)\S*)?"
    idre = r"(\w+)"
    
    def planet(self, message, user, params):
        planet = Planet.load(*params.group(1,3,5))
        if planet is None:
            message.reply("No planet with coords %s:%s:%s found" % params.group(1,3,5))
            return
        
        # List of last 10 scans
        if params.group(6) == "o":
            scans = planet.scans.filter_by(scantype=self.type).order_by(desc(Scan.id))[:10]
            if len(scans) < 1:
                message.reply("No %s Scans of %s:%s:%s found"%(PA.get(self.type,"name"),planet.x,planet.y,planet.z))
                return
            prev = []
            for scan in scans:
                prev.append("(pt%s %s)" % (scan.tick, scan.pa_id,))
            reply = "Last 10 %s Scans on %s:%s:%s "%(PA.get(self.type,"name"),planet.x,planet.y,planet.z) + " ".join(prev)
            message.reply(reply)
            return
        
        # Latest scan
        scan = planet.scan(self.type)
        if scan is None:
            message.reply("No %s Scans of %s:%s:%s found"%(PA.get(self.type,"name"),planet.x,planet.y,planet.z))
            return
        
        # Link to scan
        if params.group(7) == "l":
            reply = "%s on %s:%s:%s " % (scan.type,planet.x,planet.y,planet.z,)
            reply+= scan.link
            message.reply(reply)
            return
        
        # Display the scan
        message.reply(str(scan))
    
    def id(self, message, user, params):
        Q = session.query(Scan)
        Q = Q.filter(Scan.pa_id.ilike("%"+params.group(1)+"%"))
        Q = Q.order_by(desc(Scan.id))
        scan = Q.first()
        if scan is None:
            message.reply("No Scans matching ID '%s'"%(params.group(1),))
            return
        # Display the scan
        message.reply(str(scan))

class planet(scan, loadable):
    type = "P"
    @route(scan.planetre)
    def planet(*args):
        scan.planet(*args)
    @route(scan.idre)
    def id(*args):
        scan.id(*args)
class dev(scan, loadable):
    type = "D"
    @route(scan.planetre)
    def planet(*args):
        scan.planet(*args)
    @route(scan.idre)
    def id(*args):
        scan.id(*args)
class unit(scan, loadable):
    type = "U"
    @route(scan.planetre)
    def planet(*args):
        scan.planet(*args)
    @route(scan.idre)
    def id(*args):
        scan.id(*args)
class au(scan, loadable):
    type = "A"
    @route(scan.planetre)
    def planet(*args):
        scan.planet(*args)
    @route(scan.idre)
    def id(*args):
        scan.id(*args)
class jgp(scan, loadable):
    type = "J"
    @route(scan.planetre)
    def planet(*args):
        scan.planet(*args)
    @route(scan.idre)
    def id(*args):
        scan.id(*args)
class news(scan, loadable):
    type = "N"
    @route(scan.planetre)
    def planet(*args):
        scan.planet(*args)
    @route(scan.idre)
    def id(*args):
        scan.id(*args)
