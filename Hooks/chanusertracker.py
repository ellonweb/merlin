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
 
# This module interfaces with and updates the Core's tracker

from merlin import Merlin
from Core.exceptions_ import Reload, PNickParseError, UserError
from Core.config import Config
from Core.chanusertracker import Channels, Channel, Nicks, get_user, auth_user
from Core.loadable import loadable

@loadable.system('JOIN')
def join(message):
    # Someone is joining a channel
    if message.get_nick() == Merlin.nick:
        # Bot is joining the channel, so add a new object to the dict
        Channels[message.get_chan()] = Channel(message.get_chan())
    else:
        # Someone is joining a channel we're in
        Channels[message.get_chan()].addnick(message.get_nick())
        if Config.get("Misc","usercache") == "join":
            # Set the user's pnick
            get_user(message.get_nick(), pnickf=message.get_pnick)

@loadable.system('332')
def topic_join(message):
    # Topic of a channel is set
    Channels[message.get_chan()].topic = message.get_msg()

@loadable.system('TOPIC')
def topic_change(message):
    # Topic of a channel is set
    Channels[message.get_chan()].topic = message.get_msg()

@loadable.system('353')
def names(message):
    # List of users in a channel
    for nick in message.get_msg().split():
        if nick == "@"+Merlin.nick:
            Channels[message.get_chan()].opped = True
        if nick[0] in ("@","+"): nick = nick[1:]
        Channels[message.get_chan()].addnick(nick)
        if Config.get("Misc","usercache") == "join":
            # Use whois to get the user's pnick
            message.write("WHOIS %s" % (nick,))

@loadable.system('PART')
def part(message):
    # Someone is leaving a channel
    if message.get_nick() == Merlin.nick:
        # Bot is leaving the channel
        del Channels[message.get_chan()]
    else:
        # Someone is leaving a channel we're in
        Channels[message.get_chan()].remnick(message.get_nick())

@loadable.system('KICK')
def kick(message):
    # Someone is kicked
    kname = message.line.split()[3]
    if Merlin.nick == kname:
        # Bot is kicked from the channel
        del Channels[message.get_chan()]
    else:
        # Someone is kicked from a channel we're in
        Channels[message.get_chan()].remnick(kname)

@loadable.system('QUIT')
def quit(message):
    # Someone is quitting
    if message.get_nick() != Merlin.nick:
        # It's not the bot that's quitting
        if message.get_nick() not in Nicks:
            message.privmsg("Hi there, a nick lookup error has just occurred, the old nick was %s and the new nick is %s!"%(message.get_nick(),message.get_msg(),),Config.options("Admins")[0])
            raise Reload
        Nicks[message.get_nick()].quit()

@loadable.system('NICK')
def nick(message):
    # Someone is changing their nick
    if message.get_nick() != Merlin.nick:
        if message.get_nick() not in Nicks:
            message.privmsg("Hi there, a nick lookup error has just occurred, the old nick was %s and the new nick is %s!"%(message.get_nick(),message.get_msg(),),Config.options("Admins")[0])
            raise Reload
        Nicks[message.get_nick()].nick(message.get_msg())

@loadable.system('330')
def pnick(message):
    # Part of a WHOIS result
    if message.get_msg() == "is logged in as":
        nick = message.line.split()[3]
        pnick = message.line.split()[4]
        # Set the user's pnick
        get_user(nick, pnick=pnick)

@loadable.system('319')
def channels(message):
    # Part of a WHOIS result
    if message.get_chan() == Merlin.nick:
        # Cycle through the list of channels
        for chan in message.get_msg().split():
            if chan[0] in ("@","+"): chan = chan[1:]
            # Reset the channel and get a list of nicks
            Channels[chan] = Channel(chan)
            message.write("NAMES %s\nTOPIC %s" % (chan,chan,))

@loadable.system('MODE')
def op(message):
    # Used for tracking whether or not we're opped in channels
    if message.get_chan() not in Channels.keys():
        # Probably a user mode change, not a channel
        return
    modes = message.line.split(None,4)[3:]
    if "o" in modes[0] and Merlin.nick in modes[1].split():
        # The change in mode involves ops, and the ops might involve us
        modes, args = modes[0], modes[1].split()
        if modes[0] not in "+-":
            # add a '+' before the modes if it isn't specified (e.g. MODE s)
            modes = "+" + modes
        # modes that require args, [0] for -, [1] for +
        require_args = {
            'o': (True, True),
            'v': (True, True),
            'b': (True, True),
            'l': (False, True),
            'k': (False, True),
        }
        for mode in modes:
            # cycle through modes changed
            if mode == "+":
                set = True
            elif mode == "-":
                set = False
            else:
                if mode == "o":
                    # ops changing, pop out the target being changed
                    target = args.pop(0)
                    if target == Merlin.nick:
                        # update our op status
                        Channels[message.get_chan()].opped = set
                elif require_args.get(mode, (False, False))[set] is True:
                    # some other mode that requires an argument
                    target = args.pop(0)

@loadable.system('PRIVMSG', command=True)
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

@loadable.system('PRIVMSG', command=True)
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
            message.invite(message.get_nick(), Config.get("Channels","home"))
    except UserError:
        message.alert("You don't have access to this command")
