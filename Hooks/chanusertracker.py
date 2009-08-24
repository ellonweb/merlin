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

from Core.exceptions_ import PNickParseError, UserError
from Core.config import Config
from Core.chanusertracker import Channels, Channel, Nicks, get_user, auth_user
from Core.loadable import callback

@callback('JOIN')
def join(message):
    # Someone is joining a channel
    if message.get_nick() == message.botnick:
        # Bot is joining the channel, so add a new object to the dict
        Channels[message.get_chan()] = Channel(message.get_chan())
    else:
        # Someone is joining a channel we're in
        Channels[message.get_chan()].addnick(message.get_nick())
        if Config.get("Misc","usercache") == "join":
            try:
                # Set the user's pnick
                get_user(message.get_nick(), pnickf=message.get_pnick)
            except PNickParseError:
                pass

@callback('332')
def topic(message):
    # Topic of a channel is set
    Channels[message.get_chan()].topic = message.get_msg()

@callback('353')
def names(message):
    # List of users in a channel
    for nick in message.get_msg().split():
        if nick[0] in ("@","+"): nick = nick[1:]
        Channels[message.get_chan()].addnick(nick)
        if Config.get("Misc","usercache") == "join":
            # Use whois to get the user's pnick
            message.write("WHOIS %s" % (nick,))

@callback('PART')
def part(message):
    # Someone is leaving a channel
    if message.get_nick() == message.botnick:
        # Bot is leaving the channel
        del Channels[message.get_chan()]
    else:
        # Someone is leaving a channel we're in
        Channels[message.get_chan()].remnick(message.get_nick())

@callback('KICK')
def kick(message):
    # Someone is kicked
    kname = message.line.split()[3]
    if message.botnick == kname:
        # Bot is kicked from the channel
        del Channels[message.get_chan()]
    else:
        # Someone is kicked from a channel we're in
        Channels[message.get_chan()].remnick(kname)

@callback('QUIT')
def quit(message):
    # Someone is quitting
    if message.get_nick() != message.botnick:
        # It's not the bot that's quitting
        Nicks[message.get_nick()].quit()

@callback('NICK')
def nick(message):
    # Someone is changing their nick
    if message.get_nick() != message.bot.nick:
        Nicks[message.get_nick()].nick(message.get_msg())

@callback('330')
def pnick(message):
    # Part of a WHOIS result
    if message.get_msg() == "is logged in as":
        nick = message.line.split()[3]
        pnick = message.line.split()[4]
        # Set the user's pnick
        get_user(nick, pnick=pnick)

@callback('319')
def channels(message):
    # Part of a WHOIS result
    if message.get_chan() == message.line.split()[2] == message.line.split()[3]:
        # Cycle through the list of channels
        for chan in message.get_msg().split():
            # Reset the channel and get a list of nicks
            Channels[chan] = Channel(chan)
            message.write("NAMES %s" % (chan,))

@callback('PRIVMSG', admin=True)
def flush(message):
    """Flush entire usercache"""
    for chan in Channels.values():
        for nick in chan.nicks[:]:
            chan.remnick(nick)
        message.write("NAMES %s" % (chan.chan,))
    message.reply("Usercache is now being rebuilt.")

@callback('PRIVMSG', command=True)
def auth(message):
    """Authenticates the user, if they provide their username and password"""
    # P redundancy
    msg = message.get_msg().split()
    if len(msg) != 3:
        message.alert("!auth user pass")
        return
    try:
        user = auth_user(message.get_nick(), message.get_pnick, username=msg[1], password=msg[2])
        if user is not None:
            message.reply("You have been authenticated as %s" % (user.name,))
    except UserError:
        message.alert("You don't have access to this command")

@callback('PRIVMSG', command=True)
def letmein(message):
    """Invites the user to the private channel, if they provide their username and password"""
    # P redundancy
    msg = message.get_msg().split()
    if len(msg) != 3:
        message.alert("!letmein user pass")
        return
    try:
        user = auth_user(message.get_nick(), message.get_pnick, username=msg[1], password=msg[2])
        if (user is not None) and user.is_member():
            message.invite(message.get_nick(), Config.get("Misc","home"))
    except UserError:
        message.alert("You don't have access to this command")
