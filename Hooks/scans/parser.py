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
        
        pdunjascan = getattr(self, "parse_"+scantype)(page)
        pdunjascan.scan_id = id
        pdunjascan.planet_id = planet.id
        session.add(pdunjascan)
        session.commit()
        session.close()
    
    def parse_P(page):
        planetscan = M.DB.Maps.PlanetScan()

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

        return planetscan

