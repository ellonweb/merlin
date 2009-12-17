# This file is part of Merlin.
# Merlin is the Copyright (C)2008-2009 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.

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
 
# This module add functionality to authenticate with P

import re
from merlin import Merlin
from Core.exceptions_ import PNickParseError
from Core.db import session
from Core.maps import Channel
from Core.config import Config
from Core.loadable import system

@system('433')
def altnick(message):
    # Need to register with an alternate nick
    if Merlin.nick == Config.get("Connection", "nick"):
        message.nick(Config.get("Connection", "nick")+"2")
    else:
        message.nick(Config.get("Connection", "nick"))

@system('NICK')
def nick(message):
    # Changing nick
    if message.get_nick() == Merlin.nick:
        Merlin.nick = message.get_msg()

@system('001')
def connected(message):
    # Successfully registered on the IRC server, check what nick
    Merlin.nick = message.get_chan()
    # Hide ourself
    message.write("MODE %s +ix" % Merlin.nick)
    # Kill the ghost
    nick = Config.get("Connection", "nick")
    if Merlin.nick != nick:
        message.privmsg("RECOVER %s %s %s" % (nick, nick, Config.get("Connection", "passwd")), "P@cservice.netgamers.org")
    else: login(message)

@system('NOTICE')
def PNS(message):
    # Message from P or NickServ
    if message.get_hostmask() in ("P!cservice@netgamers.org","NS!NickServ@netgamers.org"):
        if re.match(r"^(Recover Successful For|Unable to find)", message.get_msg()):
            # Ghosted
            message.nick(Config.get("Connection", "nick"))
            login(message)
        if re.match(r"^Your nickname is registered", message.get_msg()):
            # Login
            login(message)

def login(message):
    # Login
    message.privmsg("LOGIN %s %s" % (Config.get("Connection", "nick"), Config.get("Connection", "passwd")), "P@cservice.netgamers.org")

@system('396')
def loggedin(message):
    # Authentication complete
    if "is now your hidden host" == message.get_msg():
        return # This is now deprecated in favour of
               #  setting autoinvite when adding the chan
        for channel in session.query(Channel):
            message.privmsg("INVITE %s" % (channel.name,), "P")

@system('INVITE')
def pinvite(message):
    # P invites us to a channel
    if message.get_hostmask() == "P!cservice@netgamers.org" and Channel.load(message.get_msg()) is not None:
        message.join(message.get_msg())

@system('PRIVMSG', admin=True)
def secure(message):
    """Secures the PNick of the bot."""
    message.privmsg("SET MAXLOGINS 2\nSET INVISIBLE ON\nSET AUTOKILL ON", "P")
    message.reply("Secured the PNick")
