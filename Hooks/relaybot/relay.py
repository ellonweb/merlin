# Relays everything it sees to Robocop

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

import socket
from .variables import robocop as addr
from Hooks.relaybot import channels

addr = "../RoBoCoP"

def relay(message):
	if message.get_chan() in channels:
		send(message.get_nick(), message.get_msg())

def send(nick, msg):
	try:
		s=socket.socket(socket.AF_UNIX)
		s.connect((addr))
		s.send("!relay %s %s" % (nick, msg,) + "\n")
		s.close()
	except socket.error:
		pass

callbacks = [("PRIVMSG", relay)]