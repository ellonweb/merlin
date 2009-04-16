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
from urllib2 import urlopen
from .Core.modules import M
callback = M.loadable.callback
from Hooks.scans import scans

scanre=re.compile("http://[^/]+/showscan.pl\?scan_id=([0-9a-zA-Z]+)")
scangrpre=re.compile("http://[^/]+/showscan.pl\?scan_grp=([0-9a-zA-Z]+)")

@callback('PRIVMSG')
def catcher(message):
    try:
        user = message.get_pnick()
    except PNickParseError:
        user = ""
    for m in scanre.finditer(message.get_msg()):
        scan(user, "scan", m.group(1))
        pass
    for m in scangrpre.finditer(message.get_msg()):
        scan(user, "group", m.group(1))
        pass

def scan(user, type, id):
    Popen(map(str,["python", "morganleparser.py", user, type, id,]))

class parse(object):
    def __init__(user, type, id):
        try:
            if type == "scan":
                self.scan(user, id)
            elif type == "group":
                self.group(user, id)
        except Exception, e:
            print "Exception in scan: "+e.__str__()
            traceback.print_exc()
    
    def group(user, id):
        page = urlopen('http://game.planetarion.com/showscan.pl?scan_grp='+ id).read()
        for m in re.finditer('scan_id=([0-9a-zA-Z]+)',page):
            try:
                self.scan(user, m.group(1))
            except Exception, e:
                print "Exception in scan: "+e.__str__()
                traceback.print_exc()
    
    def scan(user, id):
        page = urlopen('http://game.planetarion.com/showscan.pl?scan_id='+ id).read()
        
        m = re.search('>([^>]+) on (\d+)\:(\d+)\:(\d+) in tick (\d+)', page)
        if not m:
            print "Expired/non-matchinng scan (id: %s)" %(id,)
            return
        
        scan = m.group(1)[0].upper()
        x = m.group(2)
        y = m.group(3)
        z = m.group(4)
        tick = m.group(5)

