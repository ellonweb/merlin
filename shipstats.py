#!/usr/local/bin/python

# Download the shipstats and update the DB

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

import Core.db as db, re, urllib2
session = db.Session()

stats = urllib2.urlopen("http://game.planetarion.com/manual.php?page=stats").read()
session.execute(db.Maps.Ship.__table__.delete())

regex = r'^<tr class="(Ter|Cath|Xan|Zik|Etd)">.+?(\w+)</td>' # race & name
regex += r'<td>(\w+)</td>' # class
regex += r'<td>(\w\w|\-)</td>'*3 # t1,t2,t3
regex += r'<td>(\w+)</td>' # type
regex += r'.+?(\d+|\-)</td>'*8 # some numbers
regex += r'.+?</tr>$' # end of the line
sre = re.compile(regex,re.I|re.M)

mapping = {	"Fi": "Fighter",
			"Co": "Corvette",
			"Fr": "Frigate",
			"De": "Destroyer",
			"Cr": "Cruiser",
			"Bs": "Battleship",
			"Ro": "Roids",
			"St": "Struct",
			"Ter": "Terran",
			"Etd": "Eitraides",
			"Cath": "Cathaar",
			"Zik": "Zikonian",
			"Xan": "Xandathrii"}

keys = ['race', 'name', 'class_', 't1', 't2', 't3', 'type', 'init',
		'guns', 'armor', 'damage', 'empres', 'metal', 'crystal', 'eonium']

for line in sre.findall(stats):
	ship = db.Maps.Ship()
	line = list(line)
	for index, key in enumerate(keys):
		if line[index] in mapping:
			line[index] = mapping[line[index]]
		elif line[index].isdigit():
			line[index] = int(line[index])
		if line[index] != '-':
			setattr(ship,key,line[index])
	ship.total_cost = ship.metal + ship.crystal + ship.eonium
	print "%12s%12s%12s%12s" % (ship.name, ship.class_, ship.race, ship.type,)
	
	session.add(ship)

session.commit()
session.close()
