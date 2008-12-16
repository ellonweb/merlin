# Lookup a user's phone

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
from .variables import access
from .Core.modules import M
loadable = M.loadable.loadable

class phone(loadable):
	"""Used to view a user's phone number"""
	
	def __init__(self):
		loadable.__init__(self)
		self.access = access['hc'] | access['dc'] # "Traditional"
		#self.access = access['member'] # Asc <- pubphone settings need implementing
		self.paramre = re.compile(r"\s([\w-]+)")
		self.usage += " user"
	
	def execute(self, message):
		user, params = loadable.execute(self, message) or (None,None)
		if not params:
			return
		
		username = params.group(1)
		
		member = M.DB.Maps.User.load(name=username, exact=False)
		if member is None:
			message.alert("No such user '%s'" % (username,))
			return
		message.reply("User %s phone: %s" % (member.name, member.phone,))
	
callbacks = [("PRIVMSG", phone())]