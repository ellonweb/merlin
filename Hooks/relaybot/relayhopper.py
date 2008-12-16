# This module reconnects the bot every now and then

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

import threading
from time import sleep
from .variables import nick, admins
from .Core.exceptions_ import PNickParseError
from Hooks.relaybot import channels
import relay

class RepeatTimer(threading._Timer):
	def run(self):
		while 1:
			self.finished.wait(self.interval)
			if self.finished.isSet():
				break
			self.function(*self.args, **self.kwargs)

def hop(message = None):
	if message is None:
		message = threading.currentThread().message
	relay.send(nick, "Performing Relay Hop")
	for channel in channels:
		message.write("MODE %s -i" % (channel,))
		message.part(channel)
		message.join(channel)
		sleep(5)

def relayhopper(message):
	"Start the RelayHopper"
	if message.get_msg() == "!relayhopper":
		try:
			if message.get_pnick() in admins:
				starthopper(message)
			else:
				message.alert("You don't have access for that.")
		except PNickParseError:
			message.alert("You don't have access for that.")

def starthopper(message):
	if message.get_msg() in ("is now your hidden host", "!relayhopper"):
		for thread in threading.enumerate():
			if thread.getName() == "RelayHopper":
				message.alert("RelayHopper is already running.")
				return
		if message.get_msg() == "!relayhopper":
			hop(message)
		thread = RepeatTimer(86100, hop)
		thread.setName("RelayHopper")
		thread.setDaemon(1)
		thread.message = message
		thread.start()

def stophopper(message):
	"Stop the RelayHopper"
	if message.get_msg() == "!stophopper":
		try:
			if message.get_pnick() in admins:
				for thread in threading.enumerate():
					if thread.getName() == "RelayHopper":
						thread.cancel()
						message.alert("RelayHopper has been cancelled.")
						return
				message.alert("RelayHopper isn't running.")
			else:
				message.alert("You don't have access for that.")
		except PNickParseError:
			message.alert("You don't have access for that.")

def secchan(message):
	channel = None
	if (message.get_command() == "MODE" \
	 and message.get_hostmask() == "P!cservice@netgamers.org" \
	 and message.line.split()[3:5] == ["+o", message.botnick]):
		channel = message.line.split()[2]
	if (message.get_command() == "366" \
	 and message.line.split()[2] == message.botnick):
		channel = message.line.split()[3]
	if channel:
		if channel in channels:
			message.write("MODE %s +is" % (channel,))

callbacks = [("396", starthopper), ("MODE", secchan), ("366", secchan), ("PRIVMSG", relayhopper), ("PRIVMSG", stophopper)]