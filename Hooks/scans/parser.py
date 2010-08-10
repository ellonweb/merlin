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
from threading import Thread
from time import time
from urllib2 import urlopen
from sqlalchemy.exc import IntegrityError
from Core.exceptions_ import PNickParseError
from Core.config import Config
from Core.paconf import PA
from Core.string import decode, scanlog
from Core.db import session
from Core.maps import Updates, Planet, User, Intel, Ship, Scan, Request
from Core.maps import PlanetScan, DevScan, UnitScan, FleetScan, CovOp
from Core.loadable import system
from Core.robocop import push

scanre=re.compile("http://[^/]+/showscan.pl\?scan_id=([0-9a-zA-Z]+)")
scangrpre=re.compile("http://[^/]+/showscan.pl\?scan_grp=([0-9a-zA-Z]+)")

@system('PRIVMSG')
def catcher(message):
    try:
        user = User.load(name=message.get_pnick())
        uid = user.id if user else None
    except PNickParseError:
        uid = None
    for m in scanre.finditer(message.get_msg()):
        parse(uid, "scan", m.group(1)).start()
    for m in scangrpre.finditer(message.get_msg()):
        parse(uid, "group", m.group(1)).start()

class parse(Thread):
    def __init__(self, uid, type, id):
        self.uid = uid
        self.type = type
        self.id = id
        Thread.__init__(self)
    
    def run(self):
        scanlog(str(time()))
        uid = self.uid
        type = self.type
        id = self.id
        try:
            if type == "scan":
                self.scan(uid, id)
            elif type == "group":
                self.group(uid, id)
        except Exception, e:
            scanlog("Exception in scan: %s"%(str(e),), True)
        scanlog(str(time()))
        session.remove()
    
    def group(self, uid, gid):
        page = urlopen(Config.get("URL","viewgroup")%(gid,)).read()
        for m in re.finditer('scan_id=([0-9a-zA-Z]+)',page):
            try:
                self.scan(uid, m.group(1), gid)
            except Exception, e:
                scanlog("Exception in scan: %s"%(str(e),), True)
    
    def scan(self, uid, pa_id, gid=None):
        page = urlopen(Config.get("URL","viewscan")%(pa_id,)).read()
        page = decode(page)
        
        m = re.search('>([^>]+) on (\d+)\:(\d+)\:(\d+) in tick (\d+)', page)
        if not m:
            scanlog("Expired/non-matchinng scan (id: %s)" %(pa_id,))
            return
        
        scantype = m.group(1)[0].upper()
        x = int(m.group(2))
        y = int(m.group(3))
        z = int(m.group(4))
        tick = int(m.group(5))
        
        planet = Planet.load(x,y,z)
        if planet is None:
            return
        try:
            scan = Scan(pa_id=pa_id, scantype=scantype, tick=tick, group_id=gid, scanner_id=uid)
            planet.scans.append(scan)
            session.commit()
            scan_id = scan.id
        except IntegrityError, e:
            session.rollback()
            scanlog("Scan %s may already exist: %s" %(pa_id,str(e),))
            return
        
        parser = {
                  "P": self.parse_P,
                  "D": self.parse_D,
                  "U": self.parse_U,
                  "A": self.parse_U,
                  "J": self.parse_J,
                  "N": self.parse_N,
                 }.get(scantype)
        if parser is not None:
            parser(scan_id, scan, page)
        
        scanlog(PA.get(scantype,"name"), "%s:%s:%s" % (x,y,z,))
        
        Q = session.query(Request)
        Q = Q.filter(Request.scantype==scantype)
        Q = Q.filter(Request.target==planet)
        Q = Q.filter(Request.scan==None)
        Q = Q.filter(Request.active==True)
        result = Q.all()
        
        users = []
        for request in result:
            request.scan_id = scan_id
            request.active = False
            users.append(request.user.name)
        session.commit()
        
        if len(users) > 0:
            push("scans", scantype=scantype, pa_id=pa_id, x=planet.x, y=planet.y, z=planet.z, names=",".join(users))
    
    def parse_P(self, scan_id, scan, page):
        planetscan = scan.planetscan = PlanetScan()

        #m = re.search('<tr><td class="left">Asteroids</td><td>(\d+)</td><td>(\d+)</td><td>(\d+)</td></tr><tr><td class="left">Resources</td><td>(\d+)</td><td>(\d+)</td><td>(\d+)</td></tr><tr><th>Score</th><td>(\d+)</td><th>Value</th><td>(\d+)</td></tr>', page)
        #m = re.search(r"""<tr><td class="left">Asteroids</td><td>(\d+)</td><td>(\d+)</td><td>(\d+)</td></tr><tr><td class="left">Resources</td><td>(\d+)</td><td>(\d+)</td><td>(\d+)</td></tr><tr><th>Score</th><td>(\d+)</td><th>Value</th><td>(\d+)</td></tr>""", page)

        page=re.sub(',','',page)
        m=re.search(r"""
            <tr><td[^>]*>Metal</td><td[^>]*>(\d+)</td><td[^>]*>(\d+)</td></tr>\s*
            <tr><td[^>]*>Crystal</td><td[^>]*>(\d+)</td><td[^>]*>(\d+)</td></tr>\s*
            <tr><td[^>]*>Eonium</td><td[^>]*>(\d+)</td><td[^>]*>(\d+)</td></tr>\s*
        """,page,re.VERBOSE)

        planetscan.roid_metal = m.group(1)
        planetscan.res_metal = m.group(2)
        planetscan.roid_crystal = m.group(3)
        planetscan.res_crystal = m.group(4)
        planetscan.roid_eonium = m.group(5)
        planetscan.res_eonium = m.group(6)

        m=re.search(r"""
            <tr><th[^>]*>Value</th><th[^>]*>Score</th></tr>\s*
            <tr><td[^>]*>(\d+)</td><td[^>]*>(\d+)</td></tr>\s*
        """,page,re.VERBOSE)

        value = m.group(1)
        score = m.group(2)

        m=re.search(r"""
            <tr><th[^>]*>Agents</th><th[^>]*>Security\s+Guards</th></tr>\s*
            <tr><td[^>]*>([^<]+)</td><td[^>]*>([^<]+)</td></tr>\s*
        """,page,re.VERBOSE)

        planetscan.agents=m.group(1)
        planetscan.guards=m.group(2)

        m=re.search(r"""
            <tr><th[^>]*>Light</th><th[^>]*>Medium</th><th[^>]*>Heavy</th></tr>\s*
            <tr><td[^>]*>([^<]+)</td><td[^>]*>([^<]+)</td><td[^>]*>([^<]+)</td></tr>
        """,page,re.VERBOSE)

        planetscan.factory_usage_light=m.group(1)
        planetscan.factory_usage_medium=m.group(2)
        planetscan.factory_usage_heavy=m.group(3)

        #atm the only span tag is the one around the hidden res.
        m=re.search(r"""<span[^>]*>(\d+)</span>""",page,re.VERBOSE)

        planetscan.prod_res=m.group(1)

        session.commit()

    def parse_D(self, scan_id, scan, page):
        devscan = scan.devscan = DevScan()

        m=re.search("""
            <tr><td[^>]*>Light\s+Factory</td><td[^>]*>(\d*)</td></tr>\s*
            <tr><td[^>]*>Medium\s+Factory</td><td[^>]*>(\d*)</td></tr>\s*
            <tr><td[^>]*>Heavy\s+Factory</td><td[^>]*>(\d*)</td></tr>\s*
            <tr><td[^>]*>Wave\s+Amplifier</td><td[^>]*>(\d*)</td></tr>\s*
            <tr><td[^>]*>Wave\s+Distorter</td><td[^>]*>(\d*)</td></tr>\s*
            <tr><td[^>]*>Metal\s+Refinery</td><td[^>]*>(\d*)</td></tr>\s*
            <tr><td[^>]*>Crystal\s+Refinery</td><td[^>]*>(\d*)</td></tr>\s*
            <tr><td[^>]*>Eonium\s+Refinery</td><td[^>]*>(\d*)</td></tr>\s*
            <tr><td[^>]*>Research\s+Laboratory</td><td[^>]*>(\d*)</td></tr>\s*
            <tr><td[^>]*>Finance\s+Centre</td><td[^>]*>(\d*)</td></tr>\s*
            <tr><td[^>]*>Security\s+Centre</td><td[^>]*>(\d*)</td></tr>
        """, page,re.VERBOSE)

        devscan.light_factory = m.group(1)
        devscan.medium_factory = m.group(2)
        devscan.heavy_factory = m.group(3)
        devscan.wave_amplifier = m.group(4)
        devscan.wave_distorter = m.group(5)
        devscan.metal_refinery = m.group(6)
        devscan.crystal_refinery = m.group(7)
        devscan.eonium_refinery = m.group(8)
        devscan.research_lab = m.group(9)
        devscan.finance_centre = m.group(10)
        devscan.security_centre = m.group(11)

        m = re.search("""
            <tr><td[^>]*>Space\s+Travel</td><td[^>]*>(\d+)</td></tr>\s*
            <tr><td[^>]*>Infrastructure</td><td[^>]*>(\d+)</td></tr>\s*
            <tr><td[^>]*>Hulls</td><td[^>]*>(\d+)</td></tr>\s*
            <tr><td[^>]*>Waves</td><td[^>]*>(\d+)</td></tr>\s*
            <tr><td[^>]*>Core\s+Extraction</td><td[^>]*>(\d+)</td></tr>\s*
            <tr><td[^>]*>Covert\s+Ops</td><td[^>]*>(\d+)</td></tr>\s*
            <tr><td[^>]*>Asteroid\s+Mining</td><td[^>]*>(\d+)</td></tr>
        """, page,re.VERBOSE)

        devscan.travel = m.group(1)
        devscan.infrastructure = m.group(2)
        devscan.hulls = m.group(3)
        devscan.waves = m.group(4)
        devscan.core = m.group(5)
        devscan.covert_op = m.group(6)
        devscan.mining = m.group(7)

        session.commit()

        if scan.planet.intel is None:
            scan.planet.intel = Intel()
        if (scan.planet.intel.dists < devscan.wave_distorter) or (scan.tick == Updates.current_tick()):
            scan.planet.intel.dists = devscan.wave_distorter
            session.commit()
            scanlog("Updating planet-intel-dists")

    def parse_U(self, scan_id, scan, page):
        for m in re.finditer('(\w+\s?\w*\s?\w*)</td><td[^>]*>(\d+(?:,\d{3})*)</td>', page):
            scanlog(m.groups())

            ship = Ship.load(name=m.group(1))
            if ship is None:
                scanlog("No such unit %s" % (m.group(1),))
                continue
            scan.units.append(UnitScan(ship=ship, amount=m.group(2).replace(',', '')))

        session.commit()

    def parse_J(self, scan_id, scan, page):
        # <td class=left>Origin</td><td class=left>Mission</td><td>Fleet</td><td>ETA</td><td>Fleetsize</td>
        # <td class=left>13:10:5</td><td class=left>Attack</td><td>Gamma</td><td>5</td><td>265</td>

        #                     <td class="left">15:7:11            </td><td class="left">Defend </td><td>Ad infinitum</td><td>9</td><td>0</td>
        #<tr><td class="left">10:4:9</td><td class="left">Return</td><td>They look thirsty</td><td>5</td><td>3000</td></tr>
        #        <tr><td class="left">4:1:10</td><td class="left">Return</td><td>Or Is It?</td><td>9</td><td>3000</td></tr>

        #<tr><td class="left">10:1:10</td><td class="left">Defend</td><td class="left">Pesticide IV</td><td class="right">1</td><td class="right">0</td></tr>

        for m in re.finditer('<td[^>]*>(\d+)\:(\d+)\:(\d+)</td><td[^>]*>([^<]+)</td><td[^>]*>([^<]+)</td><td[^>]*>(\d+)</td><td[^>]*>(\d+(?:,\d{3})*)</td>', page):
            fleetscan = FleetScan()

            originx = m.group(1)
            originy = m.group(2)
            originz = m.group(3)
            mission = m.group(4)
            fleet = m.group(5)
            eta = int(m.group(6))
            fleetsize = m.group(7).replace(',', '')

            fleetscan.mission = mission
            fleetscan.fleet_name = fleet
            fleetscan.landing_tick = eta + scan.tick
            fleetscan.fleet_size = fleetsize

            scanlog("JGP fleet ")

            attacker=Planet.load(originx,originy,originz)
            if attacker is None:
                scanlog("Can't find attacker in db: %s:%s:%s"%(originx,originy,originz))
                continue
            fleetscan.owner = attacker
            fleetscan.target = scan.planet

            try:
                scan.fleets.append(fleetscan)
                session.commit()
            except IntegrityError, e:
                session.rollback()
                scanlog("Caught integrity exception in jgp: %s"%(str(e),))
                scanlog("Trying to update instead")
                query = session.query(FleetScan).filter_by(owner=attacker, target=scan.planet, fleet_size=fleetsize, fleet_name=fleet, landing_tick=eta+scan.tick, mission=mission)
                try:
                    query.update({"scan_id": scan_id})
                    session.commit()
                except Exception, e:
                    session.rollback()
                    scanlog("Exception trying to update jgp: %s"%(str(e),), True)
                    continue
            except Exception, e:
                session.rollback()
                scanlog("Exception in jgp: %s"%(str(e),), True)
                continue

    def parse_N(self, scan_id, scan, page):
        #incoming fleets
        #<td class=left valign=top>Incoming</td><td valign=top>851</td><td class=left valign=top>We have detected an open jumpgate from Tertiary, located at 18:5:11. The fleet will approach our system in tick 855 and appears to have roughly 95 ships.</td>
        for m in re.finditer('<td class="left" valign="top">Incoming</td><td valign="top">(\d+)</td><td class="left" valign="top">We have detected an open jumpgate from ([^<]+), located at (\d+):(\d+):(\d+). The fleet will approach our system in tick (\d+) and appears to have roughly (\d+) ships.</td>', page):
            fleetscan = FleetScan()

            newstick = m.group(1)
            fleetname = m.group(2)
            originx = m.group(3)
            originy = m.group(4)
            originz = m.group(5)
            arrivaltick = int(m.group(6))
            numships = m.group(7)

            fleetscan.mission = "Unknown"
            fleetscan.fleet_name = fleetname
            fleetscan.launch_tick = newstick
            fleetscan.landing_tick = arrivaltick
            fleetscan.fleet_size = numships

            owner=Planet.load(originx,originy,originz)
            if owner is None:
                continue
            fleetscan.owner = owner
            fleetscan.target = scan.planet
            try:
                scan.fleets.append(fleetscan)
                session.commit()
            except Exception, e:
                session.rollback()
                scanlog("Exception in news: %s"%(str(e),), True)
                continue

            scanlog('Incoming: ' + newstick + ':' + fleetname + '-' + originx + ':' + originy + ':' + originz + '-' + arrivaltick + '|' + numships)

        #launched attacking fleets
        #<td class=left valign=top>Launch</td><td valign=top>848</td><td class=left valign=top>The Disposable Heroes fleet has been launched, heading for 15:9:8, on a mission to Attack. Arrival tick: 857</td>
        for m in re.finditer('<td class="left" valign="top">Launch</td><td valign="top">(\d+)</td><td class="left" valign="top">The ([^,]+) fleet has been launched, heading for (\d+):(\d+):(\d+), on a mission to Attack. Arrival tick: (\d+)</td>', page):
            fleetscan = FleetScan()

            newstick = m.group(1)
            fleetname = m.group(2)
            originx = m.group(3)
            originy = m.group(4)
            originz = m.group(5)
            arrivaltick = m.group(6)

            fleetscan.mission = "Attack"
            fleetscan.fleet_name = fleetname
            fleetscan.launch_tick = newstick
            fleetscan.landing_tick = arrivaltick

            target=Planet.load(originx,originy,originz)
            if target is None:
                continue
            fleetscan.owner = scan.planet
            fleetscan.target = target

            try:
                scan.fleets.append(fleetscan)
                session.commit()
            except Exception, e:
                session.rollback()
                scanlog("Exception in news: %s"%(str(e),), True)
                continue

            scanlog('Attack:' + newstick + ':' + fleetname + ':' + originx + ':' + originy + ':' + originz + ':' + arrivaltick)

        #launched defending fleets
        #<td class=left valign=top>Launch</td><td valign=top>847</td><td class=left valign=top>The Ship Collection fleet has been launched, heading for 2:9:14, on a mission to Defend. Arrival tick: 853</td>
        for m in re.finditer('<td class="left" valign="top">Launch</td><td valign="top">(\d+)</td><td class="left" valign="top">The ([^<]+) fleet has been launched, heading for (\d+):(\d+):(\d+), on a mission to Defend. Arrival tick: (\d+)</td>', page):
            fleetscan = FleetScan()

            newstick = m.group(1)
            fleetname = m.group(2)
            originx = m.group(3)
            originy = m.group(4)
            originz = m.group(5)
            arrivaltick = m.group(6)

            fleetscan.mission = "Defend"
            fleetscan.fleet_name = fleetname
            fleetscan.launch_tick = newstick
            fleetscan.landing_tick = arrivaltick

            target=Planet.load(originx,originy,originz)
            if target is None:
                continue
            fleetscan.owner = scan.planet
            fleetscan.target = target

            try:
                scan.fleets.append(fleetscan)
                session.commit()
            except Exception, e:
                session.rollback()
                scanlog("Exception in news: %s"%(str(e),), True)
                continue

            scanlog('Defend:' + newstick + ':' + fleetname + ':' + originx + ':' + originy + ':' + originz + ':' + arrivaltick)

        #tech report
        #<td class=left valign=top>Tech</td><td valign=top>838</td><td class=left valign=top>Our scientists report that Portable EMP emitters has been finished. Please drop by the Research area and choose the next area of interest.</td>
        for m in re.finditer('<td class="left" valign="top">Tech</td><td valign="top">(\d+)</td><td class="left" valign="top">Our scientists report that ([^<]+) has been finished. Please drop by the Research area and choose the next area of interest.</td>', page):
            newstick = m.group(1)
            research = m.group(2)

            scanlog('Tech:' + newstick + ':' + research)

        #failed security report
        #<td class=left valign=top>Security</td><td valign=top>873</td><td class=left valign=top>A covert operation was attempted by Ikaris (2:5:5), but our agents were able to stop them from doing any harm.</td>
        for m in re.finditer('<td class="left" valign="top">Security</td><td valign="top">(\d+)</td><td class="left" valign="top">A covert operation was attempted by ([^<]+) \\((\d+):(\d+):(\d+)\\), but our agents were able to stop them from doing any harm.</td>', page):
            covop = CovOp()

            newstick = m.group(1)
            ruler = m.group(2)
            originx = m.group(3)
            originy = m.group(4)
            originz = m.group(5)

            covopper=Planet.load(originx,originy,originz)
            if covopper is None:
                continue
            fleetscan.covopper = covopper
            fleetscan.target = scan.planet

            try:
                scan.covops.append(covop)
                session.commit()
            except Exception, e:
                session.rollback()
                scanlog("Exception in unit: %s"%(str(e),), True)
                continue

            scanlog('Security:' + newstick + ':' + ruler + ':' + originx + ':' + originy + ':' + originz)

        #fleet report
        #<tr bgcolor=#2d2d2d><td class=left valign=top>Fleet</td><td valign=top>881</td><td class=left valign=top><table width=500><tr><th class=left colspan=3>Report of Losses from the Disposable Heroes fighting at 13:10:3</th></tr>
        #<tr><th class=left width=33%>Ship</th><th class=left width=33%>Arrived</th><th class=left width=33%>Lost</th></tr>
        #
        #<tr><td class=left>Syren</td><td class=left>15</td><td class=left>13</td></tr>
        #<tr><td class=left>Behemoth</td><td class=left>13</td><td class=left>13</td></tr>
        #<tr><td class=left>Roach</td><td class=left>6</td><td class=left>6</td></tr>
        #<tr><td class=left>Thief</td><td class=left>1400</td><td class=left>1400</td></tr>
        #<tr><td class=left>Clipper</td><td class=left>300</td><td class=left>181</td></tr>
        #
        #<tr><td class=left>Buccaneer</td><td class=left>220</td><td class=left>102</td></tr>
        #<tr><td class=left>Rogue</td><td class=left>105</td><td class=left>105</td></tr>
        #<tr><td class=left>Marauder</td><td class=left>110</td><td class=left>110</td></tr>
        #<tr><td class=left>Ironclad</td><td class=left>225</td><td class=left>90</td></tr>
        #</table>
        #
        #<table width=500><tr><th class=left colspan=3>Report of Ships Stolen by the Disposable Heroes fighting at 13:10:3</th></tr>
        #<tr><th class=left width=50%>Ship</th><th class=left width=50%>Stolen</th></tr>
        #<tr><td class=left>Roach</td><td class=left>5</td></tr>
        #<tr><td class=left>Hornet</td><td class=left>1</td></tr>
        #<tr><td class=left>Wraith</td><td class=left>36</td></tr>
        #</table>
        #<table width=500><tr><th class=left>Asteroids Captured</th><th class=left>Metal : 37</th><th class=left>Crystal : 36</th><th class=left>Eonium : 34</th></tr></table>
        #
        #</td></tr>
