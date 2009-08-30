# The generic objects used to send messages to callbacks and such.

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

import re, time

from Core.exceptions_ import ChanParseError, MsgParseError, PNickParseError

pnickre = re.compile(r"^:.+!.+@(.+)\.users.netgamers.org")

class Message(object):
    # The message object will be passed around to callbacks for inspection and ability to write to the server
    
    def __init__(self, line):
        # A raw irc line
        self.line = line
        self._chanerror = False # Will be set to True on failure to parse.
        self._msgerror = False # Will be set to True on failure to parse.
        self.parse(line)
    
    def parse(self, line):
        # Parse the irc line
        self._nick = line.split("!")[0][1:]
        self._hostmask = line.split()[0][1:]
        self._command = line.split()[1]
        
        # Channel
        try:
            chan = ":"+line.split(":")[1] # The ":" is added after the split etc, just to make the .find()s return the right result
            hash = max(chan.find("#"),0) or len(line)
            amp = max(chan.find("&"),0) or len(line)
            if not hash == amp: # There's no # or &, ie both lines returned len(line)
                self._channel = line[min(hash,amp):].split()[0]
            else: # This should almost certainly give the bot's nick
                self._channel = line.split()[2]
        except IndexError:
            self._chanerror = True
        
        # Message
        try:
            self._msg = line[line.index(":",1)+1:]
        except ValueError:
            self._msgerror = True
    
    def get_nick(self):
        # Return a parsed nick
        return self._nick
    
    def get_hostmask(self):
        # Return a parsed hostmask
        return self._hostmask
    
    def get_command(self):
        # Return the command
        return self._command

    def get_chan(self):
        # Return a channel. Raises ParseError on failure
        if self._chanerror: # Raise a ParseError: Some RAWs do not containt a target
            raise ChanParseError("Could not parse target.")
        return self._channel
    
    def reply_target(self):
        # Return the proper target to reply to
        if self._chanerror:
            raise ChanParseError("Could not parse target.")
        return self._channel if (self._channel != self.bot.nick) else self.get_nick()
    
    def get_pnick(self):
        #Return the pnick. Raises ParseError on failure
        match = pnickre.search(self.line)
        if not match: # Raise a ParseError: User hasn't authed with P
            raise PNickParseError("Could not parse P-nick.")
        return match.group(1)
    
    def get_msg(self):
        # Return the message part of a line. Raises ParseError on failure        
        if self._msgerror: # Raise a ParseError: Some RAWs do not containt a target
            raise MsgParseError("Could not parse line.")
        return self._msg
    