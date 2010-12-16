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
import sys
import urllib2
from sqlalchemy.sql import text
from Core.config import Config
from Core.db import true, false, session
from Core.maps import Ship

regex = r'^<tr class="(Good|Bad|Prty)">.+?>([^<]+)</td>' # race & name
regex += r'<td>(\w+)</td>' # class
regex += r'(?:<td>(\w\w|\-)</td>)?'*3 # t1,t2,t3
regex += r'<td>(\w+)</td>' # type
regex += r'.+?(\d+|\-)</td>'*8 # some numbers
regex += r'.+?</tr>$' # end of the line
sre = re.compile(regex,re.I|re.M)

mapping = { "Fi": "Fighter",
            "Co": "Corvette",
            "Fr": "Frigate",
            "De": "Destroyer",
            "Cr": "Cruiser",
            "Bs": "Battleship",
            "Ro": "Roids",
            "St": "Struct",
            "Prty": "Cathaar",
            "Bad": "Zikonian",
            "Good": "Xandathrii"}

keys = ['race', 'name', 'class_', 't1', 't2', 't3', 'type', 'init',
        'guns', 'armor', 'damage', 'empres', 'metal', 'crystal', 'eonium']

def main(url = Config.get("URL", "ships"), debug=False):
    stats = urllib2.urlopen(url).read()
    session.execute(Ship.__table__.delete())
    session.execute(text("SELECT setval('ships_id_seq', 1, :false);", bindparams=[false]))
    
    for line in sre.findall(stats):
        ship = Ship()
        line = list(line)
        for index, key in enumerate(keys):
            if line[index] in mapping:
                line[index] = mapping[line[index]]
            elif line[index].isdigit():
                line[index] = int(line[index])
            if line[index] not in ('-', '',):
                setattr(ship,key,line[index])
        ship.total_cost = ship.metal + ship.crystal + ship.eonium
        if debug: print "%12s%12s%12s%12s" % (ship.name, ship.class_, ship.race, ship.type,)
        
        session.add(ship)
    
    session.commit()
    session.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        sys.exit(main(url=sys.argv[1],debug=True))
    else:
        sys.exit(main(debug=True))
