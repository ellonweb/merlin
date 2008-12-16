# This module interfaces with and updates the Core's tracker

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

from .variables import admins, channels, access, usercache
from .Core.exceptions_ import PNickParseError, UserError
from .Core.modules import M

# Callback functions
def join(message):
	# Someone is joining a channel
	if message.get_nick() == message.botnick:
		# Bot is joining the channel, so add a new object to the dict
		M.CUT.channels[message.get_chan()] = M.CUT.Channel(message.get_chan())
	else:
		# Someone is joining a channel we're in
		M.CUT.channels[message.get_chan()].addnick(message.get_nick())
		if usercache == "join":
			try:
				# Set the user's pnick
				M.CUT.get_user(message.get_nick(), pnickf=message.get_pnick)
			except PNickParseError:
				pass

def topic(message):
	# Topic of a channel is set
	M.CUT.channels[message.get_chan()].topic = message.get_msg()

def names(message):
	# List of users in a channel
	for nick in message.get_msg().split():
		if nick[0] in ("@","+"): nick = nick[1:]
		M.CUT.channels[message.get_chan()].addnick(nick)
		if usercache == "join":
			# Use whois to get the user's pnick
			message.write("WHOIS %s" % (nick,))

def part(message):
	# Someone is leaving a channel
	if message.get_nick() == message.botnick:
		# Bot is leaving the channel
		del M.CUT.channels[message.get_chan()]
	else:
		# Someone is leaving a channel we're in
		M.CUT.channels[message.get_chan()].remnick(message.get_nick())

def kick(message):
	# Someone is kicked
	kname = message.line.split()[3]
	if message.botnick == kname:
		# Bot is kicked from the channel
		del M.CUT.channels[message.get_chan()]
	else:
		# Someone is kicked from a channel we're in
		M.CUT.channels[message.get_chan()].remnick(kname)

def quit(message):
	# Someone is quitting
	if message.get_nick() != message.botnick:
		# It's not the bot that's quitting
		M.CUT.nicks[message.get_nick()].quit()

def nick(message):
	# Someone is changing their nick
	nnick = message.get_msg()
	if nnick() != message.botnick:
		M.CUT.nicks[message.get_nick()].nick(nnick)

def pnick(message):
	# Part of a WHOIS result
	if message.get_msg() == "is logged in as":
		nick = message.line.split()[3]
		pnick = message.line.split()[4]
		# Set the user's pnick
		M.CUT.get_user(nick, pnick=pnick)

def flush(message):
	"""Flush entire usercache"""
	
	if message.get_msg() == "!flush":
		try:
			if message.get_pnick() in admins:
				for chan in M.CUT.channels.values():
					for nick in chan.nicks[:]:
						chan.remnick(nick)
					message.write("NAMES %s" % (chan.chan,))
				message.reply("Usercache is now being rebuilt.")
			else:
				message.alert("You don't have access for that.")
		except PNickParseError:
			message.alert("You don't have access for that.")

def auth(message):
	"""Authenticates the user, if they provide their username and password"""
	# P redundancy
	
	msg = message.get_msg().split()
	if msg[0] == "!auth":
		if len(msg) != 3:
			message.alert("!auth user pass")
			return
		try:
			user = M.CUT.auth_user(message.get_nick(), message.get_pnick, username=msg[1], password=msg[2])
			if user is not None:
				message.reply("You have been authenticated as %s" % (user.name,))
		except UserError:
			message.alert("You don't have access to this command")

def inviteme(message):
	"""Invites the user to the private channel, if they provide their username and password"""
	# P redundancy
	
	msg = message.get_msg().split()
	if msg[0] == "!inviteme":
		if len(msg) != 3:
			message.alert("!inviteme user pass")
			return
		try:
			user = M.CUT.auth_user(message.get_nick(), message.get_pnick, username=msg[1], password=msg[2])
			if (user is not None) and (channels.get("private") is not None) \
							and (access.get("member") is not None) and user.is_member():
				message.invite(message.get_nick(), channels['private'])
		except UserError:
			message.alert("You don't have access to this command")

callbacks = [("JOIN", join), ("332", topic), ("353", names), ("PART", part), ("KICK", kick), ("QUIT", quit), ("NICK", nick), ("330", pnick), ("PRIVMSG", flush), ("PRIVMSG", inviteme), ("PRIVMSG", auth)]