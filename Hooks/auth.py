# This module add functionality to authenticate with P

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
from .variables import nick, passw, admins, channels
from .Core.exceptions_ import PNickParseError

def altnick(message):
	# Need to register with an alternate nick
	message.nick(message.botnick+"2")

def connected(message):
	# Successfully connected to the IRC server
	message.write("MODE %s +ix" % message.botnick)
	# Kill the ghost
	if message.botnick[-1] == "2":
		message.privmsg("RECOVER %s %s %s" % (nick, nick, passw), "P@cservice.netgamers.org")
	else: login(message)

def PNS(message):
	# Message from P or NickServ
	if message.get_hostmask() in ("P!cservice@netgamers.org","NS!NickServ@netgamers.org"):
		if re.match(r"^(Recover Successful For|Unable to find)", message.get_msg()):
			# Ghosted
			message.nick(nick)
			login(message)
		if re.match(r"^Your nickname is registered", message.get_msg()):
			# Login
			login(message)

def login(message):
	# Login
	message.privmsg("LOGIN %s %s" % (nick, passw), "P@cservice.netgamers.org")

def loggedin(message):
	# Authentication complete
	if "is now your hidden host" == message.get_msg():
		for chan in channels.values():
			message.privmsg("INVITE %s" % (chan,), "P")

def pinvite(message):
	# P invites us to a channel
	if message.get_hostmask() == "P!cservice@netgamers.org":
		message.join(message.get_msg())

def secure(message):
	"""Secures the PNick of the bot."""
	if not message.get_msg() == "!secure":
		return
	try:
		if message.get_pnick() in admins:
			message.privmsg("SET MAXLOGINS 2\nSET INVISIBLE ON\nSET AUTOKILL ON", "P")
			message.reply("Secured the PNick")
		else:
			message.alert("You don't have access for that.")
	except PNickParseError:
		message.alert("You don't have access for that.")

callbacks = [("433", altnick), ("376", connected), ("NOTICE", PNS), ("396", loggedin), ("INVITE", pinvite), ("PRIVMSG", secure)]