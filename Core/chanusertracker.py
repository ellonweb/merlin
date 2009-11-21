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
 
# System to implement channel, nick and user tracking
# There are circular references used very carefully here, be wary when editting

from Core.exceptions_ import PNickParseError, UserError
from Core.config import Config
from Core.maps import User

class ChanUserTracker(object):
    Channels = {}
    Nicks = {}
    Pusers = {}
    
    def auth_user(self, name, pnickf, username, password):
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
        
        if (nick is not None) and (Config.get("Misc","usercache") in ("join", "command",)):
            if self.Pusers.get(user.name) is None:
                # Add the user to the tracker
                self.Pusers[user.name] = Puser(user.name)
            
            if nick.puser is None:
                # Associate the user and nick
                nick.puser = self.Pusers[user.name]
                nick.puser.nicks.add(nick)
        
        # Return the SQLA User
        return user
    
    def get_user(self, name, pnick=None, pnickf=None):
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
        
        if (nick is not None) and (Config.get("Misc","usercache") in ("join", "command",)):
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
    def __init__(self, CUT, chan):
        self.CUT = CUT
        self.chan = chan
        self.nicks = set()
        self.topic = ""
        self.opped = False
    
    def addnick(self, name):
        # Add a new nick to the channel
        nick = self.CUT.Nicks.get(name)
        if nick is None:
            nick = Nick(name)
            self.CUT.Nicks[name] = nick
        self.nicks.add(nick)
        nick.channels.add(self.chan)
    
    def remnick(self, name):
        # Remove a nick from the list
        if name not in self.CUT.Nicks.keys():
            return
        nick = self.CUT.Nicks[name]
        self.nicks.remove(nick)
        nick.channels.remove(self.chan)
        if len(nick.channels) == 0:
            del self.CUT.Nicks[nick.name]
    
    def __del__(self):
        # We've parted or been kicked, update nicks
        for nick in self.nicks:
            nick.channels.remove(self.chan)
            if len(nick.channels) == 0:
                try:
                    del self.CUT.Nicks[nick.name]
                # Might occur when the bot is quitting
                except (AttributeError, KeyError, TypeError):
                    pass
    

class Nick(object):
    # Class used for storing nicks
    def __init__(self, CUT, nick):
        self.CUT = CUT
        self.name = nick
        self.channels = set()
        self.puser = None
    
    def nick(self, name):
        # Update the nicks list
        del self.CUT.Nicks[self.name]
        self.CUT.Nicks[name] = self
        self.name = name
    
    def quit(self):
        # Quitting
        for channel in self.channels.copy():
            self.CUT.Channels[channel].remnick(self.name)
    
    def __del__(self):
        if self.user is not None:
            try:
                self.puser.nicks.remove(self)
                if len(self.puser.nicks) == 0:
                    del self.CUT.Pusers[self.puser.name]
            # Might occur when the bot is quitting
            except (AttributeError, KeyError, TypeError):
                pass
    

class Puser(object):
    # Class for storing user information for the tracker
    # Not to be confused with the SQLA class!
    def __init__(self, CUT, name):
        self.CUT = CUT
        self.name = name
        self.nicks = set()
    
