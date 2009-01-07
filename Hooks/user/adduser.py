# Add a user

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
from .variables import admins, access
from .Core.exceptions_ import PNickParseError
from .Core.modules import M
loadable = M.loadable.loadable

class adduser(loadable):
	"""Used to add a new user with the specified pnick and multiple ranks, seperated by spaces"""
	
	def __init__(self):
		loadable.__init__(self)
		self.access = access['admin'] | access.get('hc',0)
		self.paramre = re.compile(r"\s([\w-]+)")
		self.usage += " pnick [access]*"
	
	def execute(self, message):
		user, params = loadable.execute(self, message) or (None,None)
		if not params:
			return
		
		pnick = params.group(1)
		
		member = M.DB.Maps.User.load(name=pnick, active=False)
		if member is not None:
			message.alert("A user with that pnick already exists!")
			return
		acc = 0
		perm = ""
		for lvl in message.get_msg().split()[2:]:
			lvl = lvl.lower()
			if access.has_key(lvl) and (message.get_pnick() in admins or user.access/2 >= access[lvl]):
				acc = acc | access[lvl]
				perm += " " + lvl
		session = M.DB.Session()
		session.add(M.DB.Maps.User(name=pnick, access=acc))
		session.commit()
		session.close()
		message.reply("Added user %s with permissions: %s" % (pnick, perm,))
	
	def has_access(self, message):
		try:
			if message.get_pnick() in admins:
				return 1
		except PNickParseError:
			pass
		return loadable.has_access(self,message)
	
callbacks = [("PRIVMSG", adduser())]