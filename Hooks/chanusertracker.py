# This file is part of Merlin.
# Merlin is the Copyright (C)2008,2009,2010 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.

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

from Core import Merlin
from Core.exceptions_ import UserError
from Core.config import Config
from Core.chanusertracker import CUT
from Core.loadable import system

@system('JOIN')
def join(message):
    # Someone is joining a channel
    if message.get_nick() == Merlin.nick:
        # Bot is joining the channel, so add a new object to the dict
        CUT.new_chan(message.get_chan())
    else:
        # Someone is joining a channel we're in
        CUT.join(message.get_chan(), message.get_nick())
        if CUT.mode_is("rapid", "join"):
            # Set the user's pnick
            CUT.get_user(message.get_nick(), message.get_chan(), pnickf=message.get_pnick)

@system('332')
def topic_join(message):
    # Topic of a channel is set
    CUT.topic(message.get_chan(), message.get_msg())

@system('TOPIC')
def topic_change(message):
    # Topic of a channel is set
    CUT.topic(message.get_chan(), message.get_msg())

@system('353')
def names(message):
    # List of users in a channel
    for nick in message.get_msg().split():
        if nick == "@"+Merlin.nick:
            CUT.opped(message.get_chan(), True)
        elif nick == "+"+Merlin.nick or nick == Merlin.nick:
            CUT.opped(message.get_chan(), False)
        if nick[0] in ("@","+"): nick = nick[1:]
        CUT.join(message.get_chan(), nick)
        if CUT.mode_is("rapid"):
            # Use whois to get the user's pnick
            message.write("WHOIS %s" % (nick,))

@system('PART')
def part(message):
    # Someone is leaving a channel
    if message.get_nick() == Merlin.nick:
        # Bot is leaving the channel
        CUT.del_chan(message.get_chan())
    else:
        # Someone is leaving a channel we're in
        CUT.part(message.get_nick(), message.get_chan())

@system('KICK')
def kick(message):
    # Someone is kicked
    kname = message.line.split()[3]
    if Merlin.nick == kname:
        # Bot is kicked from the channel
        CUT.del_chan(message.get_chan())
    else:
        # Someone is kicked from a channel we're in
        CUT.part(kname, message.get_chan())

@system('QUIT')
def quit(message):
    # Someone is quitting
    if message.get_nick() != Merlin.nick:
        # It's not the bot that's quitting
        CUT.del_nick(message.get_nick())

@system('NICK')
def nick(message):
    # Someone is changing their nick
    if message.get_nick() != Merlin.nick:
        CUT.nick_change(message.get_nick(), message.get_msg())

@system('330')
def pnick(message):
    # Part of a WHOIS result
    if message.get_msg() == "is logged in as":
        nick = message.line.split()[3]
        pnick = message.line.split()[4]
        # Set the user's pnick
        CUT.get_user(nick, None, pnick=pnick)

@system('319')
def channels(message):
    # Part of a WHOIS result
    if message.get_chan() == Merlin.nick:
        # Cycle through the list of channels
        for chan in message.get_msg().split():
            opped = chan[0] == "@"
            if chan[0] in ("@","+"): chan = chan[1:]
            # Reset the channel and get a list of nicks
            CUT.new_chan(chan)
            CUT.opped(chan, opped)
            if CUT.mode_is("rapid"):
                message.write("NAMES %s\nTOPIC %s" % (chan,chan,))

@system('MODE')
def op(message):
    # Used for tracking whether or not we're opped in channels
    if not CUT.Channels.has_key(message.get_chan()):
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
                        CUT.opped(message.get_chan(), set)
                elif require_args.get(mode, (False, False))[set] is True:
                    # some other mode that requires an argument
                    target = args.pop(0)

@system('PRIVMSG', command=True)
def auth(message):
    """Authenticates the user, if they provide their username and password"""
    # P redundancy
    msg = message.get_msg().split()
    if len(msg) != 3:
        message.alert("!auth user pass")
        return
    try:
        chan = message.get_chan() if message.in_chan() else None
        user = CUT.auth_user(message.get_nick(), chan, message.get_pnick, username=msg[1], password=msg[2])
        if user is not None:
            message.reply("You have been authenticated as %s" % (user.name,))
    except UserError:
        message.alert("You don't have access to this command")

@system('PRIVMSG', command=True)
def letmein(message):
    """Invites the user to the private channel, if they provide their username and password"""
    # P redundancy
    msg = message.get_msg().split()
    if len(msg) != 3:
        message.alert("!letmein user pass")
        return
    try:
        chan = message.get_chan() if message.in_chan() else None
        user = CUT.auth_user(message.get_nick(), chan, message.get_pnick, username=msg[1], password=msg[2])
        if (user is not None) and user.is_member():
            message.invite(message.get_nick(), Config.get("Channels","home"))
    except UserError:
        message.alert("You don't have access to this command")
