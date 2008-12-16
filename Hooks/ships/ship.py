# Ship info

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

import re
from .Core.modules import M
loadable = M.loadable.loadable
from Hooks.ships import feud, effs

class ship(loadable):
	"""Returns the stats of the specified ship"""
	
	def __init__(self):
		loadable.__init__(self)
		self.paramre = re.compile(r"\s(\w+)")
		self.usage += " name"
	
	def execute(self, message):
		user, params = loadable.execute(self, message) or (None,None)
		if not params:
			return
		
		name = params.group(1)
		
		ship = M.DB.Maps.Ship.load(name)
		if ship is None:
			message.alert("No Ship called: %s" % (name,))
			return
		
		reply="%s is class %s | Target 1: %s |"%(ship.name,ship.class_,ship.t1)
		if ship.t2:
			reply+=" Target 2: %s |"%(ship.t2,)
		if ship.t3:
			reply+=" Target 3: %s |"%(ship.t3,)
		reply+=" Type: %s | Init: %s |"%(ship.type,ship.init)
		reply+=" EMPres: %s |"%(ship.empres,)
		if ship.type=='Emp':
			reply+=" Guns: %s |"%(ship.guns,)
		else:
			reply+=" D/C: %s |"%((ship.damage*10000)/ship.total_cost,)
		reply+=" A/C: %s"%((ship.armor*10000)/ship.total_cost,)
		message.reply(reply)

callbacks = [("PRIVMSG", ship())]