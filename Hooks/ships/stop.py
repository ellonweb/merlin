# Calc ship efficiencies

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

import math, re
from .Core.modules import M
loadable = M.loadable.loadable
from Hooks.ships import feud, effs

class stop(loadable):
	"""Calculates the required defence to the specified number of ships"""
	
	def __init__(self):
		loadable.__init__(self)
		self.paramre = re.compile(r"\s(\d+[km]?)\s(\w+)(?:\s(t1|t2|t3))?",re.I)
		self.usage += " number ship [t1|t2|t3]"
	
	def execute(self, message):
		user, params = loadable.execute(self, message) or (None,None)
		if not params:
			return
		
		num, name, attacker = params.groups()
		
		num = self.short2num(num)
		ship = M.DB.Maps.Ship.load(name=name)
		if "asteroids".rfind(name.lower()) > -1:
			total_armor = 50 * num
		elif "constructions".rfind(name.lower()) > -1:
			total_armor = 500 * num
		elif ship is not None:
			total_armor = ship.armor * num
		else:
			message.alert("No Ship called: %s" % (name,))
			return
		efficiency = effs[attacker or "t1"]
		attacker_class = getattr(message.db.Maps.Ship, attacker or "t1")
		session = message.db.Session()
		attackers = session.query(message.db.Maps.Ship).filter(attacker_class == ship.class_)
		if attackers.count() == 0:
			message.reply("%s is not hit by anything as category (%s)" % (ship.name,attacker))
			return
		if ship.class_ == "Roids":
			reply="Capturing"
		elif ship.class_ == "Struct":
			reply="Destroying"
		else:
			reply="Stopping"
		reply+=" %s %s (%s) as %s requires " % (num, ship.name,self.num2short(num*ship.total_cost/100),attacker)
		for attacker in attackers:
			if attacker.type.lower() == "emp" :
				needed=int((math.ceil(num/(float(100-ship.empres)/100)/attacker.guns))/efficiency)
			else:
				needed=int((math.ceil(float(total_armor)/attacker.damage))/efficiency)
			reply+="%s: %s (%s) " % (attacker.name,needed,self.num2short(attacker.total_cost*needed/100))
		session.close()
		message.reply(reply)

callbacks = [("PRIVMSG", stop())]