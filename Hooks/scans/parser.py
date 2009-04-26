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

# Parse a scan

import re
from subprocess import Popen
from traceback import print_exc
from urllib2 import urlopen
from .Core.modules import M
callback = M.loadable.callback
from Hooks.scans import scans

scanre=re.compile("http://[^/]+/showscan.pl\?scan_id=([0-9a-zA-Z]+)")
scangrpre=re.compile("http://[^/]+/showscan.pl\?scan_grp=([0-9a-zA-Z]+)")

@callback('PRIVMSG')
def catcher(message):
    try:
        user = M.DB.Maps.User.load(name=message.get_pnick())
        uid = user.id if user else 0
    except PNickParseError:
        uid = 0
    for m in scanre.finditer(message.get_msg()):
        scan(uid, "scan", m.group(1))
        pass
    for m in scangrpre.finditer(message.get_msg()):
        scan(uid, "group", m.group(1))
        pass

def scan(user, type, id):
    Popen(map(str,["python", "morganleparser.py", uid, type, id,]))

class parse(object):
    def __init__(uid, type, id):
        try:
            if type == "scan":
                self.scan(uid, id)
            elif type == "group":
                self.group(uid, id)
        except Exception, e:
            print "Exception in scan: "+e.__str__()
            print_exc()
    
    def group(uid, gid):
        page = urlopen('http://game.planetarion.com/showscan.pl?scan_grp='+ id).read()
        for m in re.finditer('scan_id=([0-9a-zA-Z]+)',page):
            try:
                self.scan(uid, m.group(1), gid)
            except Exception, e:
                print "Exception in scan: "+e.__str__()
                print_exc()
    
    def scan(uid, id, gid=None):
        page = urlopen('http://game.planetarion.com/showscan.pl?scan_id='+ id).read()
        
        m = re.search('>([^>]+) on (\d+)\:(\d+)\:(\d+) in tick (\d+)', page)
        if not m:
            print "Expired/non-matchinng scan (id: %s)" %(id,)
            return
        
        scantype = m.group(1)[0].upper()
        x = int(m.group(2))
        y = int(m.group(3))
        z = int(m.group(4))
        tick = int(m.group(5))
        
        planet = M.DB.Maps.Planet.load(x,y,z)
        if planet is None:
            return
        session = M.DB.Session()
        try:
            scan = M.DB.Maps.Scan(scan_id=id, planet_id=planet.id, scantype=scantype, tick=tick, group_id=gid, scanner_id=uid)
            session.add(scan)
            session.commit()
        except M.DB.sqlalchemy.exceptions.IntegrityError:
            session.rollback()
            print "Scan %s may already exist" %(id,)
            print e.__str__()
            return
        
        session.close()
        if hasattr(self,"parse_"+scantype):
            getattr(self, "parse_"+scantype)(id, scan, page)
        print scans[scantype]['name'], "%s:%s:%s" % (x,y,z,)
    
    def parse_P(id, scan, page):
        session = M.DB.Session()

        planetscan = M.DB.Maps.PlanetScan(scan_id=id)
        session.add(planetscan)

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

    def parse_D(id, scan, page):
        session = M.DB.Session()

        devscan = M.DB.Maps.DevScan(scan_id=id)
        session.add(devscan)

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

    def parse_U(id, scan, page):
        session = M.DB.Session()

        for m in re.finditer('(\w+\s?\w*\s?\w*)</td><td[^>]*>(\d+)</td>', page):
            print m.groups()

            unitscan = M.DB.Maps.UnitScan(scan_id=id)
            session.add(unitscan)

            try:
                unitscan.ship_id = M.DB.Maps.Ship.load(name=m.group(1)).id
            except AttributeError:
                print "No such unit %s" % (m.group(1),)
                session.rollback()
                continue
            unitscan.amount = m.group(2)

            session.commit()

    def parse_A(id, scan, page):
        session = M.DB.Session()

        for m in re.finditer('(\w+\s?\w*\s?\w*)</td><td[^>]*>(\d+)</td>', page):
            print m.groups()

            unitscan = M.DB.Maps.UnitScan(scan_id=id)
            session.add(unitscan)

            try:
                unitscan.ship_id = M.DB.Maps.Ship.load(name=m.group(1)).id
            except AttributeError:
                print "No such unit %s" % (m.group(1),)
                session.rollback()
                continue
            unitscan.amount = m.group(2)

            session.commit()

    def parse_J(id, scan, page):
        session = M.DB.Session()
        session.add(scan)

        # <td class=left>Origin</td><td class=left>Mission</td><td>Fleet</td><td>ETA</td><td>Fleetsize</td>
        # <td class=left>13:10:5</td><td class=left>Attack</td><td>Gamma</td><td>5</td><td>265</td>

        #                     <td class="left">15:7:11            </td><td class="left">Defend </td><td>Ad infinitum</td><td>9</td><td>0</td>
        #<tr><td class="left">10:4:9</td><td class="left">Return</td><td>They look thirsty</td><td>5</td><td>3000</td></tr>
        #        <tr><td class="left">4:1:10</td><td class="left">Return</td><td>Or Is It?</td><td>9</td><td>3000</td></tr>

        #<tr><td class="left">10:1:10</td><td class="left">Defend</td><td class="left">Pesticide IV</td><td class="right">1</td><td class="right">0</td></tr>

        for m in re.finditer('<td[^>]*>(\d+)\:(\d+)\:(\d+)</td><td[^>]*>([^<]+)</td><td[^>]*>([^<]+)</td><td[^>]*>(\d+)</td><td[^>]*>(\d+)</td>', page):
            fleetscan = M.DB.Maps.FleetScan(scan_id=id)
            session.add(fleetscan)

            originx = m.group(1)
            originy = m.group(2)
            originz = m.group(3)
            mission = m.group(4)
            fleet_name = m.group(5)
            landing_tick = int(m.group(6)) + scan.tick
            fleet_size = m.group(7)
            fleetscan.mission = mission
            fleetscan.fleet_name = fleet_name
            fleetscan.landing_tick = landing_tick
            fleetscan.fleet_size = fleet_size

            print "JGP fleet "

            attacker=M.DB.Maps.Planet.load(originx,originy,originz)
            if attacker is None:
                print "Can't find attacker in db: %s:%s:%s"%(originx,originy,originz)
                session.rollback()
                continue
            fleetscan.owner_id = attacker.id
            fleetscan.target_id = scan.planet_id

            try:
                session.commit()
            except M.DB.sqlalchemy.exceptions.IntegrityError:
                session.rollback()
                print "Caught exception in jgp: "+e.__str__()
                print_exc()
                print "Trying to update instead"
                query = session.query(M.DB.Maps.FleetScan).filter_by(owner_id=attacker.id, target_id=scan.planet_id, fleet_size=fleet_size, fleet_name=fleet_name, landing_tick=landing_tick, mission=mission)
                try:
                    query.update({"scan_id": id})
                    session.commit()
                except:
                    session.rollback()
                    print "Exception trying to update jgp: "+e.__str__()
                    print_exc()
                    continue
            except Exception, e:
                session.rollback()
                print "Exception in jgp: "+e.__str__()
                print_exc()
                continue
