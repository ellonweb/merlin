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

from Core.exceptions_ import PNickParseError, UserError
from Core.config import Config
from Core.maps import User

class ChanUserTracker(object):
    Channels = {}
    Nicks = {}
    Pusers = {}
    
    def __del__(self):
        self.Channels.clear()
        self.Nicks.clear()
        self.Pusers.clear()
    
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
        def validate(self, nick, *args):
            if self.Nicks.has_key(nick):
                return f(self, self.Nicks[nick], *args)
        return validate
    
    def valid_nick_chan(f):
        def validate(self, nick, chan, *args):
            if self.Nicks.has_key(nick) and self.Channels.has_key(chan):
                nick = self.Nicks[nick]
                chan = self.Channels[chan]
                if nick in chan.nicks:
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
            for nick in self.Pusers[pnick].nicks:
                nick.puser = None
            del self.Pusers[pnick]
    
    def list_user_nicks(self, pnick):
        # Return a list of nicks that are currently logged in with the pnick
        if self.Pusers.has_key(pnick):
            return map(lambda nick: nick.name, self.Pusers[pnick].nicks)
        else:
            return []
    
    def auth_user(self, name, channel, pnickf, username, password):
        # Update CUT with new nicks
        if channel is not None and self.mode_is("rapid", "join", "command"):
            self.join(channel, name)
        
        # Trying to authenticate with !letmein or !auth
        nick = self.Nicks.get(name)
        if (nick is not None) and (nick.puser is not None):
            # They already have a user associated
            return None
        
        try:
            pnick = pnickf()
            # They have a pnick, so shouldn't need to auth, let's auth them anyway
            user = User.load(name=pnick)
        except PNickParseError:
            # They don't have a pnick, expected
            user = User.load(name=username, passwd=password)
        
        if user is None:
            raise UserError
        
        if (nick is not None) and self.mode_is("rapid", "join", "command"):
            if self.Pusers.get(user.name) is None:
                # Add the user to the tracker
                self.Pusers[user.name] = Puser(user.name)
            
            if nick.puser is None:
                # Associate the user and nick
                nick.puser = self.Pusers[user.name]
                nick.puser.nicks.add(nick)
        
        # Return the SQLA User
        return user
    
    def get_user(self, name, channel, pnick=None, pnickf=None):
        # Update CUT with new nicks
        if channel is not None and self.mode_is("rapid", "join", "command"):
            self.join(channel, name)
        
        # Regular user check
        if (pnick is None) and (pnickf is None):
            # This shouldn't happen
            return None
        
        nick = self.Nicks.get(name)
        
        if (nick and nick.puser) is not None:
            # They already have a user associated
            pnick = nick.puser.name
        elif pnickf is not None:
            # Call the pnick function, might raise PNickParseError
            try:
                pnick = pnickf()
            except PNickParseError:
                return None
        
        user = User.load(name=pnick)
        if user is None:
            return None
        
        if (nick is not None) and self.mode_is("rapid", "join", "command"):
            if self.Pusers.get(user.name) is None:
                # Add the user to the tracker
                self.Pusers[user.name] = Puser(user.name)
            
            if nick.puser is None:
                # Associate the user and nick
                nick.puser = self.Pusers[user.name]
                nick.puser.nicks.add(nick)
        
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
        nick = CUT.Nicks.get(name)
        if nick in self.nicks:
            return
        if nick is None:
            nick = Nick(name)
            CUT.Nicks[name] = nick
        self.nicks.add(nick)
        nick.channels.add(self.chan)
    
    def remnick(self, nick):
        # Remove a nick from the list
        self.nicks.remove(nick)
        nick.channels.remove(self.chan)
        if len(nick.channels) == 0:
            nick.quit()
    
    def part(self):
        # We've parted or been kicked
        if self.chan in CUT.Channels:
            del CUT.Channels[self.chan]
        
        # Update nicks
        for nick in self.nicks.copy():
            self.remnick(nick)
    

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
        self.name = name
    
    def quit(self):
        # Quitting
        if self.name in CUT.Nicks:
            del CUT.Nicks[self.name]
        
        # Remove puser
        if self.puser is not None:
            self.puser.nicks.remove(self)
            if len(self.puser.nicks) == 0:
                del CUT.Pusers[self.puser.name]
            self.puser = None
        
        # Remove from channels
        for channel in self.channels.copy():
            CUT.Channels[channel].remnick(self)
    

class Puser(object):
    # Class for storing user information for the tracker
    # Not to be confused with the SQLA class!
    def __init__(self, name):
        self.name = name
        self.nicks = set()
    
