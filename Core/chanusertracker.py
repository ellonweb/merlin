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
 
# System to implement channel, nick and user tracking
# There are circular references used very carefully here, be wary when editting

from Core import Merlin
from Core.exceptions_ import PNickParseError, UserError
from Core.config import Config
from Core.connection import Connection
from Core.db import session
from Core.maps import User

class ChanUserTracker(object):
    Channels = {}
    Nicks = {}
    Pusers = {}
    
    def attach(self, channels={}):
        # Attach the CUT state
        for chan, nicks in channels.items():
            self.new_chan(chan)
            for nick, puser in nicks.items():
                self.join(chan, nick)
                if puser:
                    self.auth_user(nick, chan, None, puser, None)
        return ()
    
    def detach(self):
        # Generate CUT state
        channels = {}
        for chan in self.Channels.keys():
            channels[chan] = {}
            for name in self.Channels[chan].nicks:
                channels[chan][name] = self.Nicks[name].puser
        return channels,
    
    def __del__(self):
        self.Channels.clear()
        self.Nicks.clear()
        self.Pusers.clear()
    
    def reset(self):
        self.Channels.clear()
        self.Nicks.clear()
        self.Pusers.clear()
        Connection.write("WHOIS %s" % (Merlin.nick,))
    
    def mode_is(self, *modes):
        return Config.get("Misc","usercache") in modes
    
    def new_chan(self, chan):
        self.del_chan(chan)
        self.Channels[chan] = Channel(chan)
    
    def valid_chan(f):
        def validate(self, chan, *args):
            if self.Channels.has_key(chan):
                return f(self, self.Channels[chan], *args)
        return validate
    
    def valid_nick(f):
        def validate(self, name, *args):
            if self.Nicks.has_key(name):
                return f(self, self.Nicks[name], *args)
        return validate
    
    def valid_nick_chan(f):
        def validate(self, name, chan, *args):
            if self.Nicks.has_key(name) and self.Channels.has_key(chan):
                nick = self.Nicks[name]
                chan = self.Channels[chan]
                if name in chan.nicks:
                    return f(self, nick, chan, *args)
        return validate
    
    @valid_chan
    def del_chan(self, chan):
        chan.part()
    
    @valid_nick
    def del_nick(self, nick):
        nick.quit()
    
    @valid_nick
    def nick_change(self, nick, new):
        nick.nick(new)
    
    @valid_chan
    def join(self, chan, nick):
        chan.addnick(nick)
    
    @valid_nick_chan
    def part(self, nick, chan):
        chan.remnick(nick)
    
    @valid_chan
    def topic(self, chan, topic):
        chan.topic = topic
    
    @valid_chan
    def opped(self, chan, status=None):
        if status is not None:
            chan.opped = status
        if chan.opped:
            return True
    
    @valid_nick_chan
    def nick_in_chan(self, nick, chan):
        return True
    
    def untrack_user(self, pnick):
        if self.Pusers.has_key(pnick):
            for name in self.Pusers[pnick].nicks:
                self.Nicks[name].puser = None
            del self.Pusers[pnick]
    
    def get_user_nicks(self, pnick):
        # Return a list of nicks that are currently logged in with the pnick
        if self.Pusers.has_key(pnick):
            return self.Pusers[pnick].nicks.copy()
        else:
            return set()
    
    def auth_user(self, name, channel, pnickf, username, password):
        # Trying to authenticate with !letmein or !auth
        nick = self.Nicks.get(name)
        if (nick is not None) and (nick.puser is not None):
            # They already have a user associated
            return None
        
        try:
            if pnickf is not None:
                pnick = pnickf()
            else:
                pnick = username
            # They have a pnick, so shouldn't need to auth, let's auth them anyway
            user = User.load(name=pnick)
            if user is None:
                return None
        except PNickParseError:
            # They don't have a pnick, expected
            user = User.load(name=username, passwd=password)
        
        if user is None:
            raise UserError
        
        if (nick is not None) and self.mode_is("rapid", "join"):
            if self.Pusers.get(user.name) is None:
                # Add the user to the tracker
                self.Pusers[user.name] = Puser(user.name)
            
            if nick.puser is None:
                # Associate the user and nick
                nick.puser = user.name
                self.Pusers[user.name].nicks.add(nick.name)
        
        # Return the SQLA User
        return user
    
    def get_user(self, name, channel, pnick=None, pnickf=None):
        # Regular user check
        if (pnick is None) and (pnickf is None):
            # This shouldn't happen
            return None
        
        nick = self.Nicks.get(name)
        
        if (nick and nick.puser) is not None:
            # They already have a user associated
            pnick = nick.puser
        elif pnickf is not None:
            # Call the pnick function, might raise PNickParseError
            try:
                pnick = pnickf()
            except PNickParseError:
                return None
        
        user = User.load(name=pnick)
        if user is None and Config.getboolean("Misc", "autoreg"):
            if nick and not nick.puser:
                if "galmate" in Config.options("Access"):
                    access = Config.getint("Access","galmate")
                else:
                    access = 0
                user = User.load(name=pnick, active=False)
                if user is None:
                    user = User(name=pnick, access=access)
                    session.add(user)
                else:
                    user.active = True
                    user.access = access
                session.commit()
        if user is None:
            return None
        
        if (nick is not None) and self.mode_is("rapid", "join"):
            if self.Pusers.get(user.name) is None:
                # Add the user to the tracker
                self.Pusers[user.name] = Puser(user.name)
            
            if nick.puser is None:
                # Associate the user and nick
                nick.puser = user.name
                self.Pusers[user.name].nicks.add(nick.name)
        
        # Return the SQLA User
        return user

CUT = ChanUserTracker()

class Channel(object):
    # The channel object provides a means for keeping track of a channel
    def __init__(self, chan):
        self.chan = chan
        self.nicks = set()
        self.topic = ""
        self.opped = False
    
    def addnick(self, name):
        # Add a new nick to the channel
        if name in self.nicks:
            return
        if CUT.Nicks.get(name) is None:
            CUT.Nicks[name] = Nick(name)
        self.nicks.add(name)
        CUT.Nicks[name].channels.add(self.chan)
    
    def remnick(self, nick):
        # Remove a nick from the list
        self.nicks.remove(nick.name)
        nick.channels.remove(self.chan)
        if len(nick.channels) == 0:
            nick.quit()
    
    def part(self):
        # We've parted or been kicked
        if self.chan in CUT.Channels.keys():
            del CUT.Channels[self.chan]
        
        # Update nicks
        for name in self.nicks.copy():
            self.remnick(CUT.Nicks[name])
    

class Nick(object):
    # Class used for storing nicks
    def __init__(self, nick):
        self.name = nick
        self.channels = set()
        self.puser = None
    
    def nick(self, name):
        # Update the nicks list
        del CUT.Nicks[self.name]
        CUT.Nicks[name] = self
        for chan in self.channels:
            CUT.Channels[chan].nicks.remove(self.name)
            CUT.Channels[chan].nicks.add(name)
        self.name = name
    
    def quit(self):
        # Quitting
        if self.name in CUT.Nicks.keys():
            del CUT.Nicks[self.name]
        
        # Remove puser
        if self.puser is not None:
            CUT.Pusers[self.puser].nicks.remove(self.name)
            if len(CUT.Pusers[self.puser].nicks) == 0:
                del CUT.Pusers[self.puser]
            self.puser = None
        
        # Remove from channels
        for chan in self.channels.copy():
            CUT.Channels[chan].nicks.remove(self.name)
            self.channels.remove(chan)
    

class Puser(object):
    # Class for storing user information for the tracker
    # Not to be confused with the SQLA class!
    def __init__(self, name):
        self.name = name
        self.nicks = set()
    
